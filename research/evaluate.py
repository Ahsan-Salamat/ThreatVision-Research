"""Compare supplied static features and frozen scores using fixed manifest splits."""
import argparse
import csv
import hashlib
import json
import platform
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--features", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    from .validate import validate
    rows = validate(args.manifest, args.data_root)
    import numpy as np
    import sklearn
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, RocCurveDisplay
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    with open(args.features, newline="") as handle:
        reader = csv.DictReader(handle)
        columns = [k for k in reader.fieldnames if k.startswith("static_")]
        features = list(reader)
    ids = [r["sample_id"] for r in features]
    if not columns or len(ids) != len(set(ids)) or set(ids) != {r["sample_id"] for r in rows}:
        raise ValueError("Supply unique matching IDs, static_* numeric columns, and neural_score")
    mapping = {r["sample_id"]: r for r in features}
    x = np.array([[float(mapping[r["sample_id"]][c]) for c in columns] for r in rows])
    neural = np.array([float(mapping[r["sample_id"]]["neural_score"]) for r in rows])
    if not np.isfinite(x).all() or not np.isfinite(neural).all() or ((neural < 0) | (neural > 1)).any():
        raise ValueError("Features must be finite; neural scores must lie in [0,1]")
    y = np.array([r["ground_truth_label"] == "malicious" for r in rows], dtype=int)
    train = np.array([r["split"] == "train" for r in rows])
    test = np.array([r["split"] == "test" for r in rows])
    scores = {"neural": neural[test]}
    for name, values in (("static", x), ("combined", np.column_stack([x, neural]))):
        estimator = make_pipeline(StandardScaler(), LogisticRegression(random_state=17, max_iter=2000))
        estimator.fit(values[train], y[train])
        scores[name] = estimator.predict_proba(values[test])[:, 1]
    results = {}
    fig, ax = plt.subplots()
    for name, score in scores.items():
        pred = score >= 0.5
        tn, fp, fn, tp = confusion_matrix(y[test], pred, labels=[0, 1]).ravel()
        results[name] = {
            "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
            "precision": precision_score(y[test], pred, zero_division=0),
            "recall": recall_score(y[test], pred, zero_division=0),
            "f1": f1_score(y[test], pred, zero_division=0),
            "roc_auc": roc_auc_score(y[test], score),
            "average_precision": average_precision_score(y[test], score),
            "false_positive_rate": fp / (fp + tn),
            "false_negative_rate": fn / (fn + tp),
            "class_counts": {"benign": int(tn + fp), "malicious": int(tp + fn)}}
        RocCurveDisplay.from_predictions(y[test], score, name=name, ax=ax)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    report = {"metrics": results, "threshold": 0.5, "threshold_method": "fixed in advance",
              "seed": 17, "dataset_version": rows[0]["dataset_version"], "model_id": args.model_id,
              "split_strategy": "owner-supplied fixed group-validated manifest",
              "python": platform.python_version(), "sklearn": sklearn.__version__,
              "revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
              "manifest_sha256": hashlib.sha256(Path(args.manifest).read_bytes()).hexdigest(),
              "features_sha256": hashlib.sha256(Path(args.features).read_bytes()).hexdigest()}
    (output / "metrics.json").write_text(json.dumps(report, indent=2))
    fig.savefig(output / "roc.svg", bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()

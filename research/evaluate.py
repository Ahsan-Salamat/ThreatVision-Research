"""Compare supplied static features and frozen scores using fixed manifest splits."""
import argparse
import csv
import os
import hashlib
import json
import platform
import subprocess
from pathlib import Path

def source_revision(source_root):
    explicit = os.environ.get("THREATVISION_SOURCE_REVISION")
    if explicit:
        return explicit
    try:
        top = Path(subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=source_root,
            text=True, stderr=subprocess.DEVNULL).strip()).resolve()
        source_root = Path(source_root).resolve()
        source_root.relative_to(top)
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=source_root,
            text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return "unknown"


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
    feature_path = Path(args.features)
    sidecar_path = feature_path.with_suffix(".metadata.json")
    if not sidecar_path.is_file():
        raise ValueError("Missing extraction provenance sidecar")
    sidecar = json.loads(sidecar_path.read_text())
    expected = {
        "manifest_sha256": hashlib.sha256(Path(args.manifest).read_bytes()).hexdigest(),
        "checkpoint_sha256": args.model_id.lower(),
        "features_sha256": hashlib.sha256(feature_path.read_bytes()).hexdigest(),
    }
    for key, value in expected.items():
        if sidecar.get(key) != value:
            raise ValueError(f"Feature provenance mismatch: {key}")
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
    if sidecar.get("samples") != len(features):
        raise ValueError("Feature provenance mismatch: sample count")
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
    from .uncertainty import intervals
    test_rows = [row for row in rows if row["split"] == "test"]
    # Family groups are conservatively combined; lineage is used when family is unknown.
    groups = [row.get("malware_family") or row["lineage_id"] for row in test_rows]
    revision = source_revision(Path(__file__).parent)
    source_files = sorted(Path(__file__).parent.glob("*.py"))
    snapshot_hash = hashlib.sha256()
    for source_file in source_files:
        snapshot_hash.update(source_file.name.encode())
        snapshot_hash.update(source_file.read_bytes())
    report = {"source_snapshot_sha256": snapshot_hash.hexdigest(),
              "uncertainty": intervals(y[test], scores, groups),
              "source_counts": {source: sum(row["source"] == source for row in test_rows)
                                for source in sorted({row["source"] for row in test_rows})},
              "metrics": results, "threshold": 0.5, "threshold_method": "fixed in advance",
              "seed": 17, "dataset_version": rows[0]["dataset_version"], "model_id": args.model_id,
              "split_strategy": "owner-supplied fixed group-validated manifest",
              "python": platform.python_version(), "sklearn": sklearn.__version__,
              "revision": revision,
              "manifest_sha256": hashlib.sha256(Path(args.manifest).read_bytes()).hexdigest(),
              "features_sha256": hashlib.sha256(Path(args.features).read_bytes()).hexdigest()}
    (output / "metrics.json").write_text(json.dumps(report, indent=2))
    fig.savefig(output / "roc.svg", bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()

"""Strict reader of OWNER-SUPPLIED out-of-sample prediction records.

This program does not manufacture predictions, run model training, or verify
whether a dataset label/evidence is externally trustworthy. It only computes
traceable descriptive metrics from independently supplied CSV records.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

REQUIRED = (
    "sample_id", "sha256", "ground_truth_label", "label_evidence",
    "source", "dataset_version", "lineage_id", "split",
    "checkpoint_sha256", "prediction_score",
)
SPLITS = {"train", "val", "test"}
LABELS = {"benign": 0, "malicious": 1}


def is_sha256(value):
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())


def summarize_predictions(csv_path, expected_model_sha256, checkpoint_path=None, *, threshold=0.5):
    csv_path = Path(csv_path)
    model_sha256 = expected_model_sha256.lower()
    if not is_sha256(model_sha256):
        raise ValueError("Checkpoint identifier must be a 64-character SHA-256 digest")
    if not 0 < threshold < 1:
        raise ValueError("Threshold must be specified in (0, 1)")
    checkpoint_hash_verified = False
    if checkpoint_path is not None:
        h = hashlib.sha256()
        with open(checkpoint_path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                h.update(chunk)
        if h.hexdigest() != model_sha256:
            raise ValueError("Checkpoint bytes do not match expected SHA-256")
        checkpoint_hash_verified = True
    raw_bytes = csv_path.read_bytes()
    with csv_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or any(column not in reader.fieldnames for column in REQUIRED):
            raise ValueError("Prediction CSV is missing one or more required headers: " + ", ".join(REQUIRED))
        records = list(reader)
    if not records:
        raise ValueError("Prediction CSV contains no rows")
    seen_ids, seen_hashes = set(), set()
    lineage_splits = {}
    versions = set()
    classes_per_split = {s: set() for s in SPLITS}
    scores = {s: [] for s in SPLITS}
    for index, record in enumerate(records, start=2):
        if any(not (record.get(field) or "").strip() for field in REQUIRED):
            raise ValueError(f"Missing required value at CSV row {index}")
        if record["sample_id"] in seen_ids:
            raise ValueError(f"Duplicate sample ID at row {index}")
        seen_ids.add(record["sample_id"])
        file_hash = record["sha256"].lower()
        if not is_sha256(file_hash) or file_hash in seen_hashes:
            raise ValueError(f"Invalid or duplicate sample SHA-256 at row {index}")
        seen_hashes.add(file_hash)
        label = record["ground_truth_label"].strip().lower()
        if label not in LABELS:
            raise ValueError(f"Invalid label at row {index}")
        split = record["split"].strip().lower()
        if split not in SPLITS:
            raise ValueError(f"Invalid split at row {index}")
        if record["checkpoint_sha256"].lower() != model_sha256:
            raise ValueError(f"Mismatched checkpoint at row {index}")
        lineage_id = record["lineage_id"]
        if lineage_id in lineage_splits and lineage_splits[lineage_id] != split:
            raise ValueError(f"Cross-split lineage overlap for {lineage_id}")
        lineage_splits[lineage_id] = split
        try:
            score = float(record["prediction_score"])
        except ValueError:
            raise ValueError(f"Invalid score at row {index}") from None
        if not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError(f"Score must be finite and between 0 and 1 at row {index}")
        classes_per_split[split].add(label)
        scores[split].append((LABELS[label], int(score >= threshold)))
        versions.add(record["dataset_version"])
    if len(versions) != 1:
        raise ValueError("Mixed dataset versions are not allowed")
    # We do not require train or val rows, since an immutable held-out test-only
    # prediction export may be the entire available audit record.
    if classes_per_split["test"] != set(LABELS):
        raise ValueError("Test split must contain both benign and malicious cases")
    ys = scores["test"]
    tn = sum(y == 0 and p == 0 for y, p in ys)
    fp = sum(y == 0 and p == 1 for y, p in ys)
    fn = sum(y == 1 and p == 0 for y, p in ys)
    tp = sum(y == 1 and p == 1 for y, p in ys)
    n = len(ys)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "purpose": "historical_prediction_audit_not_independently_validated_benchmark",
        "dataset_version": next(iter(versions)),
        "checkpoint_sha256": model_sha256,
        "checkpoint_bytes_hash_verified": checkpoint_hash_verified,
        "prediction_csv_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "threshold": threshold,
        "threshold_origin": "user_supplied_confirm_predeclared_outside_test_data",
        "counts_per_split": {split: len(values) for split, values in scores.items()},
        "test_samples": n,
        "test_class_counts": {"benign": tn + fp, "malicious": tp + fn},
        "test_confusion_matrix_tn_fp_fn_tp": [tn, fp, fn, tp],
        "test_accuracy": (tp + tn) / n,
        "test_precision": precision,
        "test_recall": recall,
        "test_f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "independent_ground_truth_verification": False,
        "checkpoint_to_training_lineage_verified": False,
        "independent_heldout_status": "not_established_by_this_csv_alone",
        "warning": "These descriptive metrics do NOT verify labels, split authenticity, sample independence beyond supplied lineage, or whether threshold/model were selected using test data."
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--predictions", required=True)
    p.add_argument("--checkpoint-sha256", required=True)
    p.add_argument("--checkpoint", help="Optional actual checkpoint to hash before computing report")
    p.add_argument("--output", required=True)
    p.add_argument("--threshold", type=float, default=0.5)
    a = p.parse_args()
    metrics = summarize_predictions(a.predictions, a.checkpoint_sha256, a.checkpoint, threshold=a.threshold)
    dest = Path(a.output)
    if dest.exists():
        raise FileExistsError("Refusing to overwrite an existing evidence report")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(metrics, indent=2) + "\n")
    print("Audit metrics written to", dest, "— independent validation not established")


if __name__ == "__main__":
    main()

"""Validate owner-supplied manifests without executing files."""
import csv
import hashlib
import struct
from pathlib import Path

FIELDS = {"sample_id", "sha256", "ground_truth_label", "source", "label_evidence",
          "file_format", "split", "dataset_version", "lineage_id", "path"}


def validate(path, data_root):
    root = Path(data_root).resolve()
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not FIELDS <= set(reader.fieldnames or []):
            raise ValueError("Missing manifest columns: " + ", ".join(sorted(FIELDS - set(reader.fieldnames or []))))
        rows = list(reader)
    if not rows:
        raise ValueError("Supply independently labeled PE samples; empty manifest")
    seen_ids, seen_hashes, groups = set(), set(), {}
    for row in rows:
        if any(not row[key].strip() for key in FIELDS):
            raise ValueError("Required manifest fields must be populated")
        if row["sample_id"] in seen_ids or row["sha256"] in seen_hashes:
            raise ValueError("Duplicate ID or hash; resolve duplicates and label conflicts")
        seen_ids.add(row["sample_id"])
        seen_hashes.add(row["sha256"])
        if row["ground_truth_label"] not in {"benign", "malicious"}:
            raise ValueError("Labels must be independently evidenced benign or malicious")
        if row["split"] not in {"train", "validation", "test"} or row["file_format"] != "PE":
            raise ValueError("Expected PE and train/validation/test split")
        for group in [("lineage", row["lineage_id"]), ("family", row.get("malware_family", ""))]:
            if group[1]:
                previous = groups.setdefault(group, row["split"])
                if previous != row["split"]:
                    raise ValueError("Related samples cross splits")
        sample = (root / row["path"]).resolve()
        if not sample.is_relative_to(root) or not sample.is_file():
            raise ValueError("Sample path must resolve inside data root")
        if sample.stat().st_size > 32 * 1024 * 1024:
            raise ValueError("Sample exceeds 32 MiB")
        data = sample.read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("SHA-256 mismatch")
        if len(data) < 64 or data[:2] != b"MZ":
            raise ValueError("Missing DOS header")
        offset = struct.unpack_from("<I", data, 60)[0]
        if offset < 64 or offset + 24 > len(data) or data[offset:offset + 4] != b"PE\0\0":
            raise ValueError("Missing PE signature or COFF header")
    if len({r["dataset_version"] for r in rows}) != 1:
        raise ValueError("Mixed dataset versions")
    for split in ("train", "validation", "test"):
        if {r["ground_truth_label"] for r in rows if r["split"] == split} != {"benign", "malicious"}:
            raise ValueError(f"{split} requires both independently labeled classes")
    return rows

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("data_root")
    args = parser.parse_args()
    try:
        print(f"Validated {len(validate(args.manifest, args.data_root))} records; label evidence still requires human review")
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + "\n")

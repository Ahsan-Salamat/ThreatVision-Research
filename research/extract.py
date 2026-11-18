"""Batch extraction through the actual application static analyzer and checkpoint."""
import argparse
import csv
import hashlib
import importlib.util
import json
import os
import tempfile
from pathlib import Path

from .validate import validate
from .preprocessing import tensor


def load_source(path):
    spec = importlib.util.spec_from_file_location("threatvision_static", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_checkpoint(path, expected_sha256):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected_sha256:
        raise ValueError("Checkpoint checksum mismatch")
    import tensorflow as tf
    tf.keras.utils.set_random_seed(17)
    tf.config.experimental.enable_op_determinism()
    model = tf.keras.models.load_model(path, compile=False, safe_mode=True)
    if model.input_shape != (None, 224, 224, 1) or model.output_shape != (None, 1):
        raise ValueError("Unsupported checkpoint dimensions")
    return model


def extract_sample(path, static, model):
    import numpy as np
    raw = Path(path).read_bytes()
    report = static.run_static_analysis(str(path))
    if not report.get("is_pe") or report["pe"].get("error"):
        raise ValueError("Static PE parsing failed")
    image = tensor(raw)
    scores = np.array([float(model(image, training=False).numpy()[0, 0]) for _ in range(3)])
    if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
        raise ValueError("Invalid neural output")
    if not np.allclose(scores, scores[0], atol=1e-7, rtol=0):
        raise ValueError("Nonrepeatable checkpoint output; investigate augmentation before extraction")
    return {"static_size": len(raw), "static_entropy": report["global_entropy"],
            "static_sections": report["section_count"],
            "static_signature": int(bool(report["has_signature"])), "neural_score": float(scores[0])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--checkpoint-sha256", required=True)
    parser.add_argument("--static-source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if len(args.checkpoint_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in args.checkpoint_sha256):
        parser.error("--checkpoint-sha256 must be a SHA-256 hex digest")
    rows = validate(args.manifest, args.data_root)
    model = load_checkpoint(args.checkpoint, args.checkpoint_sha256)
    static = load_source(args.static_source)
    results = []
    for row in rows:
        try:
            values = extract_sample(Path(args.data_root) / row["path"], static, model)
        except Exception as error:
            raise ValueError(f"Extraction failed for sample {row['sample_id']}: {error}") from error
        results.append({"sample_id": row["sample_id"], **values})
    destination = Path(args.output)
    if destination.exists():
        raise ValueError("Output already exists")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=destination.parent, delete=False, newline="") as handle:
        temporary = handle.name
        writer = csv.DictWriter(handle, fieldnames=results[0])
        writer.writeheader()
        writer.writerows(results)
    os.replace(temporary, destination)
    metadata = {"checkpoint_sha256": args.checkpoint_sha256.lower(),
                "preprocessing_sha256": hashlib.sha256(Path(__file__).with_name("preprocessing.py").read_bytes()).hexdigest(),
                "static_source_sha256": hashlib.sha256(Path(args.static_source).read_bytes()).hexdigest(),
                "manifest_sha256": hashlib.sha256(Path(args.manifest).read_bytes()).hexdigest(),
                "features_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                "repeatability_tolerance": 1e-7, "samples": len(results)}
    destination.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()

"""Engineering smoke test only, with invented labels and minimal PE headers."""
import csv
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import hashlib
import os

class EvaluationSmoke(unittest.TestCase):
    def test_runner(self):
        from research.validate import FIELDS
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            records, features = [], []
            for i in range(12):
                raw = bytearray(128)
                raw[:2] = b"MZ"
                struct.pack_into("<I", raw, 60, 64)
                raw[64:68] = b"PE\0\0"
                raw[-1] = i
                filename = f"{i}.dat"
                (root / filename).write_bytes(raw)
                records.append(dict(sample_id=str(i), sha256=hashlib.sha256(raw).hexdigest(),
                                    ground_truth_label=["benign","malicious"][i%2],
                                    source="synthetic", label_evidence="invented-smoke-label",
                                    file_format="PE", split=["train","validation","test"][i//4],
                                    dataset_version="synthetic-smoke-only", lineage_id=str(i), path=filename))
                features.append(dict(sample_id=str(i), static_size=128, static_marker=i%3, neural_score=(i%5)/5))
            for filename, rows, fields in [("manifest.csv", records, sorted(FIELDS)),
                                            ("features.csv", features, list(features[0]))]:
                with (root / filename).open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
            feature_path = root / "features.csv"
            manifest_path = root / "manifest.csv"
            static_source = root / "static.py"
            static_source.write_text("# synthetic static provenance fixture\n")
            preprocessing_source = Path(__file__).parents[1] / "research" / "preprocessing.py"
            sidecar = {"preprocessing_sha256": hashlib.sha256(preprocessing_source.read_bytes()).hexdigest(),
                       "static_source_sha256": hashlib.sha256(static_source.read_bytes()).hexdigest(),
                       "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                       "checkpoint_sha256": "a"*64,
                       "features_sha256": hashlib.sha256(feature_path.read_bytes()).hexdigest(),
                       "samples": len(features)}
            (root / "features.metadata.json").write_text(json.dumps(sidecar))
            environment = os.environ.copy()
            environment["THREATVISION_SOURCE_REVISION"] = "unknown"
            subprocess.run([sys.executable, "-m", "research.evaluate", "--manifest", str(manifest_path),
                            "--data-root", str(root), "--features", str(feature_path),
                            "--model-id", "a"*64, "--static-source", str(static_source), "--output", str(root/"results")], check=True, env=environment)
            report = json.loads((root/"results/metrics.json").read_text())
            self.assertEqual(set(report["metrics"]), {"static","neural","combined"})
            self.assertEqual(report["dataset_version"], "synthetic-smoke-only")
            self.assertTrue((root/"results/roc.svg").is_file())
            self.assertEqual(report["revision"], "unknown")
            self.assertEqual(len(report["source_snapshot_sha256"]), 64)
            sidecar["checkpoint_sha256"] = "wrong"
            (root / "features.metadata.json").write_text(json.dumps(sidecar))
            failed = subprocess.run([sys.executable, "-m", "research.evaluate",
                "--manifest", str(manifest_path), "--data-root", str(root),
                "--features", str(feature_path), "--model-id", "a"*64, "--static-source", str(static_source),
                "--output", str(root/"bad-results")], capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("provenance mismatch", failed.stderr)
            sidecar["checkpoint_sha256"] = "a"*64
            sidecar.pop("preprocessing_sha256")
            (root / "features.metadata.json").write_text(json.dumps(sidecar))
            missing = subprocess.run([sys.executable, "-m", "research.evaluate",
                "--manifest", str(manifest_path), "--data-root", str(root),
                "--features", str(feature_path), "--model-id", "a"*64,
                "--static-source", str(static_source), "--output", str(root/"missing-results")],
                capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("preprocessing_sha256", missing.stderr)
            sidecar["preprocessing_sha256"] = "0"*64
            (root / "features.metadata.json").write_text(json.dumps(sidecar))
            mismatch = subprocess.run([sys.executable, "-m", "research.evaluate",
                "--manifest", str(manifest_path), "--data-root", str(root),
                "--features", str(feature_path), "--model-id", "a"*64,
                "--static-source", str(static_source), "--output", str(root/"mismatch-results")],
                capture_output=True, text=True)
            self.assertNotEqual(mismatch.returncode, 0)
            self.assertIn("preprocessing_sha256", mismatch.stderr)

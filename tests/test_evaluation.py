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
            subprocess.run([sys.executable, "-m", "research.evaluate", "--manifest", str(root/"manifest.csv"),
                            "--data-root", str(root), "--features", str(root/"features.csv"),
                            "--model-id", "synthetic-scores-no-model", "--output", str(root/"results")], check=True)
            report = json.loads((root/"results/metrics.json").read_text())
            self.assertEqual(set(report["metrics"]), {"static","neural","combined"})
            self.assertEqual(report["dataset_version"], "synthetic-smoke-only")
            self.assertTrue((root/"results/roc.svg").is_file())

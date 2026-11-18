import unittest
import tempfile
from pathlib import Path
from research.splits import assign
from research.extract import load_checkpoint

class PhaseTwoTests(unittest.TestCase):
    def test_checksum_rejected_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"invalid.keras"
            path.write_bytes(b"invalid")
            with self.assertRaisesRegex(ValueError, "checksum"):
                load_checkpoint(path, "0"*64)

    def test_source_holdout(self):
        rows = [dict(sample_id=str(i), sha256=str(i), lineage_id=str(i),
                     ground_truth_label=["benign","malicious"][i%2],
                     source=["a","b","c"][i//2], collection_date=["2020-01-01","2021-01-01","2022-01-01"][i//2])
                for i in range(6)]
        split = assign(rows, "source", test_source="c", validation_source="b")
        self.assertEqual([r["split"] for r in split],["train"]*2+["validation"]*2+["test"]*2)
        self.assertEqual(split, assign(rows, "temporal", validation_date="2021-01-01", test_date="2022-01-01"))
        rows[4]["lineage_id"] = rows[0]["lineage_id"]
        with self.assertRaisesRegex(ValueError, "boundaries"):
            assign(rows, "source", test_source="c", validation_source="b")

    def test_insufficient_uncertainty(self):
        from research.uncertainty import intervals
        self.assertIn("insufficient", intervals([0,1],{},["a","b"])["status"])

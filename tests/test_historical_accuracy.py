"""Synthetic fixture tests only; not empirical malware evidence."""
import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from research.historical_accuracy import summarize_predictions, REQUIRED

CHECKPOINT = 'c' * 64


def rows():
    # 4 distinct synthetic examples: deliberately NOT a research dataset.
    cases = [('benign', '.10'), ('malicious', '.90'), ('malicious', '.20'), ('benign', '.10')]
    return [{"sample_id": str(i), "sha256": hashlib.sha256(f"synthetic-case-{i}".encode()).hexdigest(),
             "ground_truth_label": label, "label_evidence": "synthetic-test-only", "source": "synthetic",
             "dataset_version": "fixture-v1", "lineage_id": str(i), "split": "test",
             "checkpoint_sha256": CHECKPOINT, "prediction_score": score}
            for i,(label, score) in enumerate(cases)]


class HistoricalPredictionAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/"predictions.csv"

    def write(self, cases):
        with self.path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED)
            writer.writeheader()
            writer.writerows(cases)

    def test_synthetic_predictions_recalculate_without_claiming_validation(self):
        self.write(rows())
        report = summarize_predictions(self.path, CHECKPOINT)
        self.assertAlmostEqual(report['test_accuracy'], 0.75)
        self.assertEqual(report['test_confusion_matrix_tn_fp_fn_tp'], [2,0,1,1])
        self.assertFalse(report['independent_ground_truth_verification'])
        self.assertFalse(report['checkpoint_bytes_hash_verified'])

    def test_rejects_duplicate_hash(self):
        r=rows();r[1]['sha256']=r[0]['sha256'];self.write(r)
        with self.assertRaisesRegex(ValueError,"duplicate"):
            summarize_predictions(self.path,CHECKPOINT)

    def test_rejects_wrong_checkpoint(self):
        r=rows();r[1]['checkpoint_sha256']='d'*64;self.write(r)
        with self.assertRaisesRegex(ValueError,"Mismatched checkpoint"):
            summarize_predictions(self.path,CHECKPOINT)

    def test_rejects_cross_split_lineage(self):
        r=rows();r[1]['lineage_id']=r[0]['lineage_id'];r[1]['split']='train';self.write(r)
        with self.assertRaisesRegex(ValueError,"lineage overlap"):
            summarize_predictions(self.path,CHECKPOINT)

    def test_rejects_one_class_test_split(self):
        r=rows();r=[x for x in r if x['ground_truth_label']=='benign'];self.write(r)
        with self.assertRaisesRegex(ValueError,"both benign and malicious"):
            summarize_predictions(self.path,CHECKPOINT)

    def test_rejects_invalid_scores(self):
        r=rows();r[0]['prediction_score']='nan';self.write(r)
        with self.assertRaisesRegex(ValueError,"finite"):
            summarize_predictions(self.path,CHECKPOINT)

    def test_rejects_invalid_checkpoint_bytes(self):
        self.write(rows());ckpt=Path(self.tmp.name)/'wrong.keras';ckpt.write_bytes(b'not the checkpoint')
        with self.assertRaisesRegex(ValueError,"Checkpoint bytes"):
            summarize_predictions(self.path,CHECKPOINT,ckpt)

if __name__ == '__main__':
    unittest.main()

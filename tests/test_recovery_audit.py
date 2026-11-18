import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from research.recovery_audit import audit, summarize_manifest, summarize_log


class RecoveryAuditTests(unittest.TestCase):
    def test_summary_rejects_implied_continuous_training(self):
        raw = b'epoch,val_auc,val_precision\n0,0.0,1.0\n1,0.0,1.0\n0,0.0,1.0\n'
        info = summarize_log(raw)
        self.assertEqual(info['rows'], 3)
        self.assertEqual(info['epochs_reset'], 1)
        self.assertEqual(info['epoch_zero_count'], 2)

    def test_manifest_counts_hash_strings_not_verified_files(self):
        raw = ('filename,sha256,folder,label\na.png,'+'a'*64+',malware,1\n'
               +'b.png,'+'b'*64+',benign,0\n').encode()
        info = summarize_manifest(raw)
        self.assertEqual(info['distinct_hash_strings'], 2)
        self.assertEqual(info['label_counts'], {'0': 1, '1': 1})
        self.assertTrue(info['hash_format_valid'])

    def test_archives_can_be_audited_without_model_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            m = Path(temp) / 'model.zip'
            n = Path(temp) / 'notebooks.zip'
            payload = io.BytesIO()
            with zipfile.ZipFile(payload, 'w') as z:
                z.writestr('metadata.json', json.dumps({'keras_version': 'test'}))
                z.writestr('config.json', json.dumps({'config': {'name': 'demo', 'layers': [
                    {'class_name': 'InputLayer','config': {'name': 'input', 'batch_shape': [None, 8, 8, 1]}}]}}))
                z.writestr('model.weights.h5', b'mock nonexecutable test content')
            with zipfile.ZipFile(m, 'w') as z:
                z.writestr('ThreatVision/best_model.keras', payload.getvalue())
                z.writestr('ThreatVision/training_log.csv', 'epoch,val_auc\n0,0.0\n')
            with zipfile.ZipFile(n, 'w') as z:
                z.writestr('Colab Notebooks/A.ipynb', json.dumps({'cells': []}))
            result = audit(m, n)
            self.assertEqual(result['input_shape'], [None, 8, 8, 1])
            self.assertEqual(result['training_log']['rows'], 1)
            self.assertEqual(len(result['notebooks']), 1)

if __name__ == '__main__':
    unittest.main()

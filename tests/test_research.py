import unittest
import tempfile
from pathlib import Path
from research.validate import validate

class ManifestTests(unittest.TestCase):
    def test_empty_manifest(self):
        from research.validate import FIELDS
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "manifest.csv"
            manifest.write_text(",".join(sorted(FIELDS)) + "\n")
            with self.assertRaisesRegex(ValueError, "empty manifest"):
                validate(manifest, folder)

    def test_missing_columns(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "manifest.csv"
            manifest.write_text("sample_id\na\n")
            with self.assertRaisesRegex(ValueError, "Missing manifest columns"):
                validate(manifest, folder)

class PreprocessingTests(unittest.TestCase):
    def test_transform(self):
        import numpy as np
        from research.preprocessing import tensor, build_bigram_matrix, bytes_to_stream, preprocess_matrix
        matrix = build_bigram_matrix(bytes_to_stream(bytes([0,0,1,2,1,2])))
        self.assertEqual(matrix[1,2], 2)
        self.assertEqual(preprocess_matrix(matrix)[0,0], 0)
        for raw in (b"ab", bytes(range(256)), b"\0"*256):
            output = tensor(raw)
            self.assertEqual(output.shape, (1,224,224,1))
            self.assertTrue(np.array_equal(output, tensor(raw)))
            self.assertTrue(np.isfinite(output).all())
            self.assertGreaterEqual(output.min(), 0)
            self.assertLessEqual(output.max(), 1)

    def test_invalid_input(self):
        import numpy as np
        from research.preprocessing import tensor, prepare_tensor
        for raw in (b"", b"a", "abc"):
            with self.assertRaises(ValueError):
                tensor(raw)
        with self.assertRaises(ValueError):
            prepare_tensor(np.zeros((10,10)))


class LeakageTests(unittest.TestCase):
    def test_valid_and_rejected_manifests(self):
        import csv
        import hashlib
        import struct
        from research.validate import FIELDS
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rows = []
            for index in range(6):
                data = bytearray(128)
                data[:2] = b"MZ"
                struct.pack_into("<I", data, 60, 64)
                data[64:68] = b"PE\0\0"
                data[-1] = index
                name = f"fixture-{index}.dat"
                (root / name).write_bytes(data)
                rows.append(dict(sample_id=str(index), sha256=hashlib.sha256(data).hexdigest(),
                                 ground_truth_label=["benign","malicious"][index%2],
                                 source="synthetic-test-only", label_evidence="synthetic-validator-test",
                                 file_format="PE", split=["train","validation","test"][index//2],
                                 dataset_version="synthetic", lineage_id=str(index), path=name))
            manifest = root / "manifest.csv"
            def write():
                with manifest.open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=sorted(FIELDS))
                    writer.writeheader()
                    writer.writerows(rows)
            write()
            self.assertEqual(len(validate(manifest, root)),6)
            rows[2]["lineage_id"] = "0"
            write()
            with self.assertRaisesRegex(ValueError, "Related"):
                validate(manifest, root)
            rows[2]["lineage_id"] = "2"
            rows[2]["sha256"] = rows[0]["sha256"]
            write()
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                validate(manifest, root)
            rows[2]["sha256"] = "0"*64
            write()
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                validate(manifest, root)

class NumericalStageTests(unittest.TestCase):
    def test_quantization_and_dct(self):
        import numpy as np
        from research.preprocessing import matrix_to_gray, apply_2d_dct, resize_to_cnn
        self.assertEqual(matrix_to_gray(np.array([[0.0,0.5,1.0]])).tolist(), [[0,127,255]])
        image = np.full((256,256), 255, dtype=np.uint8)
        coefficients = apply_2d_dct(image)
        self.assertEqual(coefficients[0,0],255)
        self.assertEqual(np.count_nonzero(coefficients),1)
        self.assertEqual(resize_to_cnn(coefficients).shape,(224,224))

if __name__ == "__main__":
    unittest.main()

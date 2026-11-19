import hashlib
import importlib.util
import unittest
from pathlib import Path

from research.fixtures import harmless_pe
from research.preprocessing import tensor
from research.preprocessing_parity import compare


APP_ROOT = Path(__file__).resolve().parents[2] / "ThreatVision Final"
CONVERTER_PATH = APP_ROOT / "backend/python_scripts/convert_to_bigram_dct.py"
EXPECTED_IMAGE_HASHES = {
    "minimal_pe": "84d3834641d71b01ef8c62a8e68fc38b13fdfd27ba91c1308f59e5f0c6251535",
    "repeated": "63e2a19d3f7aeef9b1b8ecc4f58601277dfb355ed6c296f04bb91a67c2f55693",
    "boundary": "8639d58fc6b9c0f40711cf78141ab2990410f9bcbe099d29e34b57b3ad454cbb",
}


@unittest.skipUnless(CONVERTER_PATH.is_file(), "companion application source is not available")
class ProductionPreprocessingParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("threatvision_production_converter", CONVERTER_PATH)
        cls.production = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.production)

    def test_production_and_research_tensors_match_expected_fixtures(self):
        fixtures = {
            "minimal_pe": harmless_pe(),
            "repeated": bytes(range(256)) * 8,
            "boundary": bytes([0, 0, 255, 0, 255, 255, 1, 0, 1, 1]) * 30,
        }
        for name, raw in fixtures.items():
            with self.subTest(fixture=name):
                production = self.production
                matrix = production.build_bigram_matrix(production.bytes_to_stream(raw))
                image = production.resize_to_cnn(
                    production.apply_2d_dct(
                        production.matrix_to_gray(production.preprocess_matrix(matrix))
                    )
                )
                self.assertEqual(image.shape, (224, 224))
                self.assertEqual(str(image.dtype), "uint8")
                self.assertEqual(hashlib.sha256(image.tobytes()).hexdigest(), EXPECTED_IMAGE_HASHES[name])
                app_input = image.astype("float32")[None, :, :, None] / 255.0
                research_input = tensor(raw)
                self.assertEqual(research_input.shape, (1, 224, 224, 1))
                self.assertEqual(str(research_input.dtype), "float32")
                self.assertTrue((app_input == research_input).all())

    def test_every_preprocessing_stage_has_identical_hashes_and_zero_delta(self):
        if not CONVERTER_PATH.is_file():
            self.skipTest("companion application source is not available")
        report = compare(CONVERTER_PATH)
        self.assertEqual(report["status"], "PASS")
        for fixture in report["fixtures"].values():
            self.assertEqual(len(fixture["comparisons"]), 8)
            for stage in fixture["comparisons"].values():
                self.assertTrue(stage["exact_match"])
                self.assertEqual(stage["max_abs_delta"], 0.0)
                self.assertEqual(stage["application_sha256"], stage["research_sha256"])


if __name__ == "__main__":
    unittest.main()

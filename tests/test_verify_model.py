import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from research.verify_model import (
    inspect_configuration, select_input_profile, sha256_file, verify_checkpoint,
)


def make_archive(path, shape, activation="sigmoid", extra_layer=None):
    config = {
        "class_name": "Functional",
        "config": {
            "name": "test",
            "input_layers": ["input", 0, 0],
            "output_layers": ["output", 0, 0],
            "layers": [
                {"class_name": "InputLayer", "config": {"name": "input", "batch_shape": [None, *shape]}},
                {"class_name": "Dense", "config": {"name": "output", "activation": activation, "units": 1}},
            ],
        },
    }
    if extra_layer:
        config["config"]["layers"].append({"class_name": extra_layer, "config": {"name": "unknown"}})
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("config.json", json.dumps(config))
        archive.writestr("metadata.json", json.dumps({"keras_version": "test"}))


class VerifyModelTests(unittest.TestCase):
    def test_inspects_both_supported_shapes(self):
        with tempfile.TemporaryDirectory() as directory:
            for size in (224, 256):
                path = Path(directory) / f"{size}.keras"
                make_archive(path, (size, size, 1))
                result = inspect_configuration(path)
                self.assertEqual(result["input_shape"], (None, size, size, 1))
                self.assertTrue(result["sigmoid_output"])

    def test_rejects_unsupported_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsupported.keras"
            make_archive(path, (128, 128, 1))
            with self.assertRaisesRegex(ValueError, "Unsupported"):
                inspect_configuration(path)

    def test_rejects_non_sigmoid_model(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "linear.keras"
            make_archive(path, (224, 224, 1), activation="linear")
            with self.assertRaisesRegex(ValueError, "sigmoid"):
                inspect_configuration(path)

    def test_rejects_intermediate_sigmoid_when_output_is_linear(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "intermediate-sigmoid.keras"
            make_archive(path, (224, 224, 1), activation="linear")
            with zipfile.ZipFile(path) as source:
                config = json.loads(source.read("config.json"))
            output = config["config"]["layers"][1]
            intermediate = dict(output)
            intermediate["config"] = dict(output["config"], name="intermediate", activation="sigmoid")
            config["config"]["layers"].insert(1, intermediate)
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("config.json", json.dumps(config))
                archive.writestr("metadata.json", json.dumps({"keras_version": "test"}))
            with self.assertRaisesRegex(ValueError, "model output layer"):
                inspect_configuration(path)

    def test_rejects_unsupported_serialized_layers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "custom.keras"
            make_archive(path, (224, 224, 1), extra_layer="Lambda")
            with self.assertRaisesRegex(ValueError, "Unsupported serialized layer"):
                inspect_configuration(path)

    def test_hash_is_streamed_and_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weights"
            path.write_bytes(b"harmless test bytes")
            self.assertEqual(sha256_file(path), sha256_file(path))

    def test_hash_mismatch_rejected_before_runtime_import(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "224.keras"
            make_archive(path, (224, 224, 1))
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                verify_checkpoint(path, "0" * 64)

    def test_profiles_keep_224_and_256_value_contracts_distinct(self):
        p224, c224 = select_input_profile((None, 224, 224, 1))
        p256, c256 = select_input_profile((None, 256, 256, 1))
        self.assertEqual(p224, "production-224-v1")
        self.assertEqual((c224["minimum"], c224["maximum"]), (0.0, 1.0))
        self.assertEqual(p256, "recovered-256-v1")
        self.assertEqual((c256["minimum"], c256["maximum"]), (0.0, 255.0))

    def test_rejects_profile_for_wrong_model_shape(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            select_input_profile((None, 224, 224, 1), "recovered-256-v1")

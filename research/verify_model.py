"""Safe synthetic forward-pass verification for an identified Keras checkpoint."""
import argparse
import hashlib
import os
import json
import platform
import sys
import time
from pathlib import Path

# Match the application's TensorFlow runtime by default. Callers may explicitly
# select another Keras 3 backend before importing this module.
os.environ.setdefault("KERAS_BACKEND", "tensorflow")


INPUT_PROFILES = {
    "production-224-v1": {
        "shape": (224, 224, 1), "minimum": 0.0, "maximum": 1.0,
        "contract": "float32 grayscale pixels divided by 255 by production inference",
        "cases": ("zeros", "constant_half", "ones", "gradient_0_to_1", "random_0_to_1_seed42"),
    },
    "recovered-256-v1": {
        "shape": (256, 256, 1), "minimum": 0.0, "maximum": 255.0,
        "contract": "float32 grayscale pixel values in [0,255], matching the separate recovered-checkpoint probe",
        "cases": ("zeros", "constant_127", "constant_255", "gradient_0_to_255", "random_0_to_255_seed42"),
    },
}
SUPPORTED_LAYER_CLASSES = {
    "InputLayer", "RandomFlip", "RandomRotation", "Conv2D", "Rescaling",
    "Functional", "GlobalAveragePooling2D", "Dropout", "Dense",
}


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_configuration(path):
    """Read the Keras config without importing a model runtime."""
    import zipfile
    with zipfile.ZipFile(path) as archive:
        config = json.loads(archive.read("config.json"))
        metadata = json.loads(archive.read("metadata.json"))
    model_config = config.get("config", {})
    layers = model_config.get("layers", [])
    input_layers = [layer for layer in layers if layer.get("class_name") == "InputLayer"]
    if len(input_layers) != 1:
        raise ValueError("Expected exactly one serialized InputLayer")
    shape = tuple(input_layers[0]["config"].get("batch_shape", ()))
    if len(shape) != 4 or shape[0] is not None or shape[1:] not in {p["shape"] for p in INPUT_PROFILES.values()}:
        raise ValueError(f"Unsupported model input shape: {shape}")
    unsupported = sorted({layer.get("class_name") for layer in layers} - SUPPORTED_LAYER_CLASSES)
    if unsupported:
        raise ValueError(f"Unsupported serialized layer classes: {unsupported}")
    output_ref = model_config.get("output_layers")
    output_name = output_ref[0] if isinstance(output_ref, (list, tuple)) and output_ref else None
    output_layers = [layer for layer in layers
                     if layer.get("config", {}).get("name") == output_name]
    if len(output_layers) != 1:
        raise ValueError("Expected one identifiable serialized model output layer")
    output_layer = output_layers[0]
    output_config = output_layer.get("config", {})
    sigmoid = (output_layer.get("class_name") == "Dense"
               and output_config.get("activation") == "sigmoid"
               and output_config.get("units") == 1)
    if not sigmoid:
        raise ValueError("Expected the model output layer to be a one-unit Dense sigmoid")
    def summarize_layer(layer):
        values = layer.get("config", {})
        summary = {"class": layer.get("class_name"), "name": values.get("name")}
        for key in ("activation", "units", "filters", "kernel_size", "strides",
                    "padding", "scale", "offset", "mode", "factor"):
            if key in values:
                summary[key] = values[key]
        return summary

    return {"name": model_config.get("name"), "input_shape": shape,
            "sigmoid_output": sigmoid,
            "output_layer": summarize_layer(output_layer),
            "layers": [summarize_layer(layer) for layer in layers],
            "saved_keras_version": metadata.get("keras_version"),
            "saved_at": metadata.get("date_saved")}


def select_input_profile(input_shape, requested=None):
    shape = tuple(input_shape[1:])
    matching = [name for name, profile in INPUT_PROFILES.items() if profile["shape"] == shape]
    profile_id = requested or (matching[0] if len(matching) == 1 else None)
    if profile_id not in INPUT_PROFILES or profile_id not in matching:
        raise ValueError(f"Profile {profile_id!r} does not match model input {tuple(input_shape)}")
    return profile_id, INPUT_PROFILES[profile_id]


def verify_checkpoint(path, expected_sha256, atol=1e-7, display_path=None, profile_id=None):
    path = Path(path)
    actual_sha256 = sha256_file(path)
    if actual_sha256.lower() != expected_sha256.lower():
        raise ValueError("Checkpoint SHA-256 does not match the expected value")
    config = inspect_configuration(path)
    profile_id, profile = select_input_profile(config["input_shape"], profile_id)
    import numpy as np
    import keras

    keras.backend.clear_session()
    model = keras.saving.load_model(path, compile=False, safe_mode=True)
    model_shape = tuple(model.input_shape)
    if model_shape != (None,) + config["input_shape"][1:]:
        raise ValueError(f"Loaded model shape differs from archive config: {model_shape}")
    if tuple(model.output_shape) != (None, 1):
        raise ValueError(f"Expected one scalar output, got {model.output_shape}")

    height, width, channels = config["input_shape"][1:]
    rng = np.random.default_rng(42)
    if profile_id == "production-224-v1":
        ramp = np.linspace(0, 1, height * width, dtype=np.float32).reshape(1, height, width, channels)
        cases = {
            "zeros": np.zeros((1, height, width, channels), dtype=np.float32),
            "constant_half": np.full((1, height, width, channels), 0.5, dtype=np.float32),
            "ones": np.ones((1, height, width, channels), dtype=np.float32),
            "gradient_0_to_1": ramp,
            "random_0_to_1_seed42": rng.random((1, height, width, channels), dtype=np.float32),
        }
    else:
        ramp = np.linspace(0, 255, height * width, dtype=np.float32).reshape(1, height, width, channels)
        cases = {
            "zeros": np.zeros((1, height, width, channels), dtype=np.float32),
            "constant_127": np.full((1, height, width, channels), 127, dtype=np.float32),
            "constant_255": np.full((1, height, width, channels), 255, dtype=np.float32),
            "gradient_0_to_255": ramp,
            "random_0_to_255_seed42": (rng.random((1, height, width, channels)) * 255).astype(np.float32),
        }
    results = {}
    for name, tensor in cases.items():
        if tensor.shape != (1, height, width, channels) or tensor.dtype != np.float32:
            raise ValueError("Synthetic input violates the inferred model input contract")
        if not np.isfinite(tensor).all() or tensor.min() < profile["minimum"] or tensor.max() > profile["maximum"]:
            raise ValueError(f"Synthetic input violates the {profile_id} value range")
        start = time.perf_counter()
        first = keras.ops.convert_to_numpy(model(tensor, training=False))
        elapsed_ms = (time.perf_counter() - start) * 1000
        second = keras.ops.convert_to_numpy(model(tensor, training=False))
        delta = float(np.max(np.abs(first - second)))
        if first.shape != (1, 1):
            raise ValueError(f"Unexpected output shape for {name}: {first.shape}")
        if not np.isfinite(first).all():
            raise ValueError(f"Non-finite model output for {name}")
        if config["sigmoid_output"] and ((first < 0).any() or (first > 1).any()):
            raise ValueError(f"Sigmoid output outside [0,1] for {name}")
        results[name] = {"output": float(first[0, 0]), "repeat_max_abs_delta": delta,
                         "first_call_ms": round(elapsed_ms, 3), "finite": True,
                         "repeatable_within_tolerance": delta <= atol}
    repeatable = all(case["repeatable_within_tolerance"] for case in results.values())
    runtime = {"python": platform.python_version(), "keras": keras.__version__,
               "backend": keras.backend.backend(), "numpy": np.__version__,
               "system": platform.system(), "machine": platform.machine()}
    if runtime["backend"] == "tensorflow":
        import tensorflow as tf
        runtime["tensorflow"] = tf.__version__
        runtime["devices"] = [device.name for device in tf.config.list_physical_devices()]
    elif runtime["backend"] == "torch":
        import torch
        runtime["torch"] = torch.__version__

    return {
        "status": "PASS" if repeatable else "PASS_WITH_NONDETERMINISM",
        "scope": "synthetic forward-pass verification only; no classification accuracy claim",
        "checkpoint_path": display_path or str(path.resolve()),
        "checkpoint_sha256": actual_sha256,
        "model": config,
        "loaded_input_shape": list(model.input_shape),
        "loaded_output_shape": list(model.output_shape),
        "parameter_count": int(model.count_params()),
        "input_profile": {"id": profile_id, "minimum": profile["minimum"],
                          "maximum": profile["maximum"], "contract": profile["contract"]},
        "runtime": runtime,
        "repeatability_tolerance": atol,
        "all_cases_repeatable": repeatable,
        "cases": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--display-path", help="safe path label recorded in JSON evidence")
    parser.add_argument("--profile", choices=tuple(INPUT_PROFILES),
                        help="explicit model/input profile; inferred from input shape when omitted")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verify_checkpoint(args.checkpoint, args.sha256, display_path=args.display_path,
                               profile_id=args.profile)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n")
    print(rendered)
    if report["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()

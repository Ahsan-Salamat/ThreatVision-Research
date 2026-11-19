"""Compare application and research preprocessing at each observable stage."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

from .fixtures import harmless_pe
from . import preprocessing as research


def load_production(path):
    spec = importlib.util.spec_from_file_location("threatvision_production_converter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value):
    return hashlib.sha256(np.ascontiguousarray(value).tobytes()).hexdigest()


def stages(module, raw):
    stream = module.bytes_to_stream(raw)
    pairs = module.build_bigram_matrix(stream)
    suppressed = pairs.copy()
    suppressed[0, 0] = 0.0
    normalized = module.preprocess_matrix(pairs.copy())
    quantized = module.matrix_to_gray(normalized.copy())
    dct_image = module.apply_2d_dct(quantized)
    resized = module.resize_to_cnn(dct_image)
    if hasattr(module, "tensor"):
        final_tensor = module.tensor(raw)
    else:
        final_tensor = resized.astype(np.float32)[None, :, :, None] / 255.0
    return {
        "byte_stream": stream,
        "bigram_counts": pairs,
        "zero_pair_suppressed": suppressed,
        "normalized_matrix": normalized,
        "quantized_grayscale": quantized,
        "dct_output": dct_image,
        "resized_image": resized,
        "final_model_input": final_tensor,
    }


def compare(production_path, checkpoint_path=None, checkpoint_sha256=None):
    production_path = Path(production_path).resolve()
    app = load_production(production_path)
    model = None
    model_sha256 = None
    runtime = None
    if checkpoint_path is not None:
        checkpoint_path = Path(checkpoint_path).resolve()
        model_sha256 = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
        if not checkpoint_sha256 or model_sha256.lower() != checkpoint_sha256.lower():
            raise ValueError("Checkpoint SHA-256 does not match the requested preprocessing parity identity")
        import tensorflow as tf
        model = tf.keras.models.load_model(checkpoint_path, compile=False, safe_mode=True)
        if model.input_shape != (None, 224, 224, 1) or model.output_shape != (None, 1):
            raise ValueError("Preprocessing parity requires the production 224x224 checkpoint")
        runtime = {"tensorflow": tf.__version__, "keras": tf.keras.__version__}
    fixtures = {
        "minimal_pe": harmless_pe(),
        "repeated_byte_range": bytes(range(256)) * 8,
        "boundary_pairs": bytes([0, 0, 255, 0, 255, 255, 1, 0, 1, 1]) * 30,
    }
    fixture_reports = {}
    for name, raw in fixtures.items():
        app_stages = stages(app, raw)
        research_stages = stages(research, raw)
        comparisons = {}
        for stage, app_value in app_stages.items():
            research_value = research_stages[stage]
            if app_value.shape != research_value.shape or app_value.dtype != research_value.dtype:
                raise ValueError(f"{name}/{stage}: shape or dtype mismatch")
            delta = float(np.max(np.abs(app_value.astype(np.float64) - research_value.astype(np.float64)))) if app_value.size else 0.0
            same = bool(np.array_equal(app_value, research_value))
            comparisons[stage] = {
                "shape": list(app_value.shape),
                "dtype": str(app_value.dtype),
                "application_sha256": digest(app_value),
                "research_sha256": digest(research_value),
                "max_abs_delta": delta,
                "exact_match": same,
            }
            if not same:
                raise ValueError(f"{name}/{stage}: application and research results differ (max_abs_delta={delta})")
        if model is not None:
            app_score = np.asarray(model(app_stages["final_model_input"], training=False))
            research_score = np.asarray(model(research_stages["final_model_input"], training=False))
            if app_score.shape != (1, 1) or not np.isfinite(app_score).all() or not np.isfinite(research_score).all():
                raise ValueError(f"{name}/neural_output: invalid model result")
            output_delta = float(np.max(np.abs(app_score - research_score)))
            if output_delta > 1e-7 or (app_score < 0).any() or (app_score > 1).any():
                raise ValueError(f"{name}/neural_output: application and research outputs differ")
            comparisons["neural_output"] = {
                "shape": list(app_score.shape), "dtype": str(app_score.dtype),
                "application_sha256": digest(app_score), "research_sha256": digest(research_score),
                "max_abs_delta": output_delta, "exact_match": bool(np.array_equal(app_score, research_score)),
                "score": float(app_score[0, 0]), "semantics": "uncalibrated_sigmoid_score",
            }
        fixture_reports[name] = {
            "input_sha256": hashlib.sha256(raw).hexdigest(),
            "input_bytes": len(raw),
            "comparisons": comparisons,
        }
    return {
        "status": "PASS",
        "scope": "implementation parity on deterministic harmless fixtures; not historical training parity or classification evidence",
        "application_converter_sha256": hashlib.sha256(production_path.read_bytes()).hexdigest(),
        "research_preprocessing_sha256": hashlib.sha256(Path(research.__file__).read_bytes()).hexdigest(),
        "checkpoint_sha256": model_sha256,
        "runtime": runtime,
        "fixtures": fixture_reports,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--converter", type=Path, default=(
        Path(__file__).resolve().parents[2] / "ThreatVision Final/backend/python_scripts/convert_to_bigram_dct.py"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-sha256")
    args = parser.parse_args()
    if bool(args.checkpoint) != bool(args.checkpoint_sha256):
        parser.error("--checkpoint and --checkpoint-sha256 must be supplied together")
    report = compare(args.converter, args.checkpoint, args.checkpoint_sha256)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()

"""Explicit runtime probe of an owner-supplied Keras archive."""
import argparse
import hashlib
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint")
    args = parser.parse_args()
    import numpy as np
    import tensorflow as tf
    from .preprocessing import tensor
    tf.keras.utils.set_random_seed(17)
    from .fixtures import harmless_pe
    from .extract import load_checkpoint
    expected = json.loads((Path(__file__).parents[1] / "docs/audits/checkpoint-metadata.json").read_text())["sha256"]
    model = load_checkpoint(args.checkpoint, expected)
    probe = tensor(harmless_pe())
    scores = [float(model.predict(probe, verbose=0)[0,0]) for _ in range(5)]
    print(json.dumps({"checkpoint_sha256": hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
                      "synthetic_probe_only": True, "scores": scores,
                      "exact_repeatability": len(set(scores)) == 1,
                      "finite": bool(np.isfinite(scores).all()),
                      "input_shape": model.input_shape, "output_shape": model.output_shape,
                      "tensorflow": tf.__version__, "fixture_sha256": hashlib.sha256(harmless_pe()).hexdigest()}, indent=2))

if __name__ == "__main__":
    main()

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
    model = tf.keras.models.load_model(args.checkpoint, compile=False, safe_mode=True)
    if model.input_shape != (None, 224, 224, 1) or model.output_shape != (None, 1):
        raise ValueError("Unsupported checkpoint dimensions")
    probe = tensor(bytes(range(256)) * 4)
    scores = [float(model.predict(probe, verbose=0)[0,0]) for _ in range(5)]
    print(json.dumps({"checkpoint_sha256": hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
                      "synthetic_probe_only": True, "scores": scores,
                      "exact_repeatability": len(set(scores)) == 1,
                      "finite": bool(np.isfinite(scores).all())}, indent=2))

if __name__ == "__main__":
    main()

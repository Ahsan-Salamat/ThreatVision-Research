"""New training pipeline. Does not reproduce the checkpoint's historical training."""
import argparse
import hashlib
import json
import platform
import zipfile
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--data-root", required=True)
    p.add_argument("--architecture-archive", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--learning-rate", type=float, default=5e-6)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--cpu", action="store_true")
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.learning_rate <= 0:
        p.error("Epochs, batch size and learning rate must be positive")
    from .validate import validate
    rows = validate(args.manifest, args.data_root)
    import numpy as np
    import tensorflow as tf
    from .preprocessing import tensor
    if args.cpu:
        tf.config.set_visible_devices([], "GPU")
    tf.keras.utils.set_random_seed(args.seed)
    tf.config.experimental.enable_op_determinism()
    with zipfile.ZipFile(args.architecture_archive) as archive:
        config = json.loads(archive.read("config.json"))
    # Deserialize topology only. Original checkpoint weights are never loaded here.
    model = tf.keras.models.model_from_json(json.dumps(config))
    model.trainable = True
    model.compile(optimizer=tf.keras.optimizers.Adam(args.learning_rate),
                  loss="binary_crossentropy", metrics=[tf.keras.metrics.AUC(name="auc")])
    selected = {}
    for split in ("train","validation"):
        subset = [r for r in rows if r["split"] == split]
        if args.smoke:
            subset = [next(r for r in subset if r["ground_truth_label"] == label)
                      for label in ("benign","malicious")]
        images = np.concatenate([tensor((Path(args.data_root)/r["path"]).read_bytes()) for r in subset])
        labels = np.array([r["ground_truth_label"] == "malicious" for r in subset], dtype=np.float32)
        selected[split] = (images, labels)
    destination = Path(args.output)
    destination.mkdir(parents=True, exist_ok=False)
    labels = selected["train"][1]
    weights = {i: len(labels)/(2*int((labels == i).sum())) for i in (0,1)}
    model.fit(*selected["train"], validation_data=selected["validation"],
              epochs=1 if args.smoke else args.epochs, batch_size=args.batch_size,
              class_weight=weights,
              callbacks=[tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                         tf.keras.callbacks.ModelCheckpoint(str(destination/"best.keras"), save_best_only=True),
                         tf.keras.callbacks.CSVLogger(str(destination/"history.csv"))])
    model.save(destination/"final.keras")
    metadata = vars(args).copy()
    metadata.update({"initialization": "fresh random weights from supplied topology",
                     "historical_training_reproduction": False, "tensorflow": tf.__version__,
                     "python": platform.python_version(),
                     "architecture_archive_sha256": hashlib.sha256(Path(args.architecture_archive).read_bytes()).hexdigest(),
                     "manifest_sha256": hashlib.sha256(Path(args.manifest).read_bytes()).hexdigest()})
    # Keep private paths out of logs.
    for key in ("manifest","data_root","architecture_archive","output"):
        metadata.pop(key)
    (destination/"training.json").write_text(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    main()

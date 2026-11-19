# Model Architecture

## Deployed artifact

The deployed inference artifact is `threatvision_v01.keras`. Its actual bytes in the companion application tree were inspected on 18 November 2026: SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`; ZIP CRC validation passed. The serialized configuration identifies a MobileNetV2 backbone (`mobilenetv2_1.00_224`), a 224 × 224 × 1 float input, and one sigmoid output interpreted by the application as a neural score. The application normalizes grayscale pixels to `[0,1]` before inference. Archive metadata records Keras 3.14.1 and save time `2026-05-15@10:37:36`. Counts recomputed from serialized layer shapes and trainability flags are 2,422,084 total parameters, 1,512,580 trainable, and 909,504 non-trainable. Seventeen of the backbone's 154 nested layers are marked trainable. The earlier 2,424,196 total is unsupported; the reason for the discrepancy is not established. The checkpoint remains excluded from this public research repository.

## Recovered earlier model — a different checkpoint

The original Drive export includes `best_model.keras` (SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`). Its serialized Keras 3.13.2 configuration has a **256 × 256 × 1** input and a top-level sequence `Input → grayscale_to_rgb Conv2D → preprocess Rescaling → MobileNetV2 → GAP → dropout → Dense(128) → dropout → sigmoid`. It contains **no top-level saved augmentation layers**. This is distinct both from the following documented 224 × 224 deployed topology and from the later `ThreatVisionFInal.ipynb` training script, which places Rescaling **before** the channel adapter and includes augmentation. Neither model can be silently substituted for the other; the earlier checkpoint has since passed safe runtime load and synthetic forward-pass checks, recorded in [the checkpoint audit](audits/PRODUCTION_CHECKPOINT_VERIFICATION.md). [Full reconciliation](audits/RECOVERY_CROSSCHECK_2026-11-18.md).

## Layer sequence

1. Input spectrogram: `(224,224,1)`.
2. Horizontal random flip and random rotation with factor bounds ±0.014 of a full turn (±5.04°, approximately ±0.088 rad).
3. A learned 1 × 1 convolution maps one channel to three channels.
4. Rescaling applies `2x − 1` after the learned adapter. Because the adapter is a linear convolution, its output is not guaranteed to remain in `[0,1]`; the backbone input is therefore not guaranteed to lie in `[-1,1]`.
5. MobileNetV2 inverted-residual backbone. ImageNet initialization is reported in project materials, but the saved topology alone cannot verify the origin of its weights.
6. Global average pooling to 1,280 features.
7. Dropout (0.4), dense 128-unit ReLU layer, dropout (0.2), and dense sigmoid output.

The checkpoint's top-level `compile_config` records Adam with a learning rate near `5 × 10⁻⁶`, binary cross-entropy, and accuracy, ROC AUC, precision, and recall metrics. These saved settings do not provide epoch histories, dataset provenance, or the complete training process. A debugging script references `phase2_best.keras`, but that file is unavailable; no artifact hash or export record establishes it as the source of `threatvision_v01.keras`.

The rotation factor follows the [Keras RandomRotation definition](https://keras.io/api/layers/preprocessing_layers/image_augmentation/random_rotation/). Both augmentation nodes serialize `training=True` in their functional graph calls. The actual model was safely loaded and called with `training=False` under Keras 3.14.1 / TensorFlow 2.16.1 on Apple Silicon; all five synthetic probes were exactly repeatable at `1e-7` tolerance. A previous TensorFlow 2.21.0 run produced different values, so only within-runtime repeatability is established. The production caller's `model.predict` path also ran successfully on a harmless locally generated PE fixture. See the [production checkpoint verification record](audits/PRODUCTION_CHECKPOINT_VERIFICATION.md). This does not establish predictive accuracy or score calibration.

## Intended use and decision authority

The model was developed as an advisory signal for Windows PE triage. The local training distribution is undocumented, so its actual input coverage cannot be established. The application transform also accepts arbitrary bytes, but this does not make arbitrary file types part of the validated model domain. Static criteria control the final malware/benign label; the CNN may adjust the numeric threat score by no more than five points.

Selected CPU inference observations of approximately 350–500 ms are not a controlled latency benchmark.

## Prior architecture and explainability

SE-ResNet appears in the cited study and project documentation as a literature model; no SE-ResNet checkpoint or implementation is part of the deployed ThreatVision artifact. The deployed model is MobileNetV2-based. Literature results are not measurements of this checkpoint.

The interface includes a radial-gradient overlay styled as a Grad-CAM visualization, but it is a CSS illustration. The backend does not compute gradients or produce a saliency map. Validated explanation methods remain future work.

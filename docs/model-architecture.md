# Model Architecture

## Deployed artifact

The deployed inference artifact is `threatvision_v01.keras`. Its serialized configuration identifies a MobileNetV2 backbone (`mobilenetv2_1.00_224`), a 224 × 224 × 1 float input normalized to `[0,1]`, and one sigmoid output interpreted by the application as a neural score. The archive metadata records Keras 3.14.1 and a save time of 2026-05-15. Counts recomputed from serialized layer shapes and trainability flags are 2,422,084 total parameters, 1,512,580 trainable, and 909,504 non-trainable. Seventeen of the backbone's 154 nested layers are marked trainable. The earlier 2,424,196 total is unsupported; the reason for the discrepancy is not established.

## Layer sequence

1. Input spectrogram: `(224,224,1)`.
2. Training-time augmentation layers: horizontal random flip and random rotation (±0.014 rad).
3. A learned 1 × 1 convolution maps one channel to three channels.
4. Rescaling maps `[0,1]` to `[-1,1]` for the pretrained backbone.
5. ImageNet-pretrained MobileNetV2 inverted-residual backbone.
6. Global average pooling to 1,280 features.
7. Dropout (0.4), dense 128-unit ReLU layer, dropout (0.2), and dense sigmoid output.

The checkpoint is not included in this repository. Its top-level `compile_config` records Adam with a learning rate near `5 × 10⁻⁶`, binary cross-entropy, and accuracy, ROC AUC, precision, and recall metrics. These saved settings do not provide epoch histories, dataset provenance, or the complete training process. A debugging script references `phase2_best.keras`, but that file is unavailable; no artifact hash or export record establishes it as the source of `threatvision_v01.keras`.

## Intended use and decision authority

The model was developed as an advisory signal for Windows PE triage. The local training distribution is undocumented, so its actual input coverage cannot be established. The application transform also accepts arbitrary bytes, but this does not make arbitrary file types part of the validated model domain. Static criteria control the final malware/benign label; the CNN may adjust the numeric threat score by no more than five points.

Selected CPU inference observations of approximately 350–500 ms are not a controlled latency benchmark.

## Prior architecture and explainability

SE-ResNet appears in the cited study and project documentation as a literature model; no SE-ResNet checkpoint or implementation is part of the deployed ThreatVision artifact. The deployed model is MobileNetV2-based. Literature results are not measurements of this checkpoint.

The interface includes a radial-gradient overlay styled as a Grad-CAM visualization, but it is a CSS illustration. The backend does not compute gradients or produce a saliency map. Validated explanation methods remain future work.

# Model Architecture

## Deployed artifact

The deployed inference artifact is `threatvision_v01.keras`. Its recorded topology uses a MobileNetV2 backbone (`mobilenetv2_1.00_224`), a 224 × 224 × 1 float input normalized to `[0,1]`, and one sigmoid output interpreted by the application as a malware score. The artifact has 2,424,196 total parameters; approximately 1.51 million were reported trainable during phase-two fine-tuning.

## Layer sequence

1. Input spectrogram: `(224,224,1)`.
2. Training-time augmentation layers: horizontal random flip and random rotation (±0.014 rad).
3. A learned 1 × 1 convolution maps one channel to three channels.
4. Rescaling maps `[0,1]` to `[-1,1]` for the pretrained backbone.
5. ImageNet-pretrained MobileNetV2 inverted-residual backbone.
6. Global average pooling to 1,280 features.
7. Dropout (0.4), dense 128-unit ReLU layer, dropout (0.2), and dense sigmoid output.

The checkpoint is not included in this repository. This topology does not provide its weights or training data and is not sufficient to reproduce the model's training or evaluation.

## Intended use and decision authority

The model was developed as an advisory signal for Windows PE triage. The local training distribution is undocumented, so its actual input coverage cannot be established. The application transform also accepts arbitrary bytes, but this does not make arbitrary file types part of the validated model domain. Static criteria control the final malware/benign label; the CNN may adjust the numeric threat score by no more than five points.

Selected CPU inference observations of approximately 350–500 ms are not a controlled latency benchmark.

## Prior architecture and explainability

SE-ResNet appears in the cited study and project documentation as a literature model; no SE-ResNet checkpoint or implementation is part of the deployed ThreatVision artifact. The deployed model is MobileNetV2-based. Literature results are not measurements of this checkpoint.

The interface includes a radial-gradient overlay styled as a Grad-CAM visualization, but it is a CSS illustration. The backend does not compute gradients or produce a saliency map. Validated explanation methods remain future work.

# Model Architecture

## Deployed artifact

The verified inference artifact is `threatvision_v01.keras`. The handoff records a MobileNetV2 backbone (`mobilenetv2_1.00_224`) with a 224 × 224 × 1 float input normalized to `[0,1]` and a single sigmoid output interpreted as `P(malware)`. The artifact has 2,424,196 total parameters; approximately 1.51 million were reported trainable during phase-two fine-tuning.

## Layer sequence

1. Input spectrogram: `(224,224,1)`.
2. Training-time augmentation layers: horizontal random flip and random rotation (±0.014 rad).
3. A learned 1 × 1 convolution maps one channel to three channels.
4. Rescaling maps `[0,1]` to `[-1,1]` for the pretrained backbone.
5. ImageNet-pretrained MobileNetV2 inverted-residual backbone.
6. Global average pooling to 1,280 features.
7. Dropout (0.4), dense 128-unit ReLU layer, dropout (0.2), and dense sigmoid output.

The local checkpoint is not included in this documentation portfolio. The topology above is descriptive and does not enable exact reproduction of model weights or training.

## Inference and decision authority

The available observations record roughly 350–500 ms of CPU inference for selected inputs. This is not a controlled latency benchmark. The model score influences the numerical threat score by no more than ±5 points. Static rules retain full authority over the final binary label.

## Distinguishing prior work from deployed implementation

An SE-ResNet architecture and associated MaleX results appear in project-facing materials as a literature baseline. The handoff confirms that there is no SE-ResNet checkpoint or implementation in the audited project. The deployed artifact is MobileNetV2. Reported MaleX results, including ROC-AUC 0.970, recall 94.0%, precision 84.7%, and F1 0.891, belong to Mohammed et al. (2021), not to this deployed model.

## Explainability status

The interface contains a radial-gradient overlay presented as a Grad-CAM-style visualization. It is a CSS simulation. The backend does not compute gradients or produce a live saliency map. True gradient-based explanation of the DCT representation remains proposed work.

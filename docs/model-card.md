# ThreatVision production model card

## Model identity

- **Artifact:** `threatvision_v01.keras`, kept in the companion application checkout and excluded here.
- **SHA-256:** `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`.
- **Architecture:** random flip and rotation layers; learned grayscale-to-RGB convolution; MobileNetV2 backbone; global average pooling; dropout; 128-unit dense layer; dropout; one-unit sigmoid output.
- **Input:** float32 grayscale tensor, `(batch, 224, 224, 1)`, normalized by the caller to `[0,1]`.
- **Output:** one sigmoid score per input. It is an uncalibrated neural score, not an estimated malware probability.
- **Parameters:** 2,422,084 total.
- **Saved metadata:** Keras 3.14.1; archive date 15 May 2026. These do not establish the training environment or history.

The saved graph places its learned one-channel-to-three-channel adapter before an internal `Rescaling(2x−1)` layer. No additional external normalization is applied after the caller's `[0,1]` conversion. The archive reports ImageNet initialization for MobileNetV2, but the weight origin is not independently established. Inference was called with `training=False`, so the augmentation layers were not applied in the verified prediction path. The production and research implementations were compared on three deterministic harmless fixtures at eight preprocessing stages; all arrays and model outputs matched exactly. See the [parity record](audits/PRODUCTION_PREPROCESSING_PARITY.md).

## Verification evidence

The exact archive was checked against the registered SHA-256 and safely loaded with `compile=False, safe_mode=True` using Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1 and NumPy 1.26.4. It declared `(None,224,224,1)` input and `(None,1)` output. Five deterministic synthetic tensors and one harmless PE-derived tensor produced finite scores in `[0,1]`, with identical repeated outputs at absolute tolerance `1e-7`. The exact scores and runtime record are in the [verification report](audits/PRODUCTION_CHECKPOINT_VERIFICATION.md) and its JSON result.

This confirms archive identity, deserialization and tested forward-pass behavior. It does not establish training data, label validity, model lineage, accuracy, calibration, robustness or generalization. A previous TensorFlow 2.21.0 execution yielded different probe scores; cross-version numerical equivalence is not claimed.

## Intended use and limitations

The model is an advisory component in a Windows PE triage prototype. Static-analysis rules determine the application's final benign/malicious label; the neural score can adjust only the numerical threat score, by at most five points. Static-rule weights and thresholds are not calibrated against an independently labeled cohort. The model's training domain is undocumented. Accepting arbitrary bytes in the preprocessing function does not validate non-PE inputs.

The application does not execute uploaded files. Its UI's radial-gradient heatmap is illustrative and is not a computed saliency map. Family labels are static-rule profiles, not learned multiclass outputs. The model weights, raw samples and original training dataset are not distributed in this repository.

## Separate recovered checkpoint

`best_model.keras` is a different 256×256×1 artifact with SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`. It has its own registered verifier profile and `[0,255]` probe range. It is not a substitute for the production model. Its training lineage and historical preprocessing remain unverified; see the [experiment lineage register](experiment-lineage.md).

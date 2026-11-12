# Experimental Record

This record distinguishes the artifacts and observations in the audit from literature results. It is not a substitute for the missing training and evaluation logs.

## Model iterations and artifacts

| Model reference | Status in project evidence | Available evidence |
| --- | --- | --- |
| SE-ResNet literature model | Reported in project-facing material; not deployed | Architecture and metrics attributed to Mohammed et al. (2021); no local implementation or weights |
| `phase2_best.keras` | Referenced but missing | A script contains an external local path; file and directory are absent |
| `threatvision_v01.keras` | Verified deployed checkpoint | Keras artifact present in audited application repository; MobileNetV2-based topology; about 2.42M total parameters |

The documentation-only portfolio contains no model weights or training scripts.

## Training configuration evidence

The deployed artifact configuration records Adam with a learning rate near `5 × 10⁻⁶`, binary cross-entropy, a MobileNetV2 backbone, horizontal flips and small random rotations during training, and dropout in the classification head. The artifact configuration is not a training history. Epoch logs, loss curves, model-selection records, class weighting, dataset manifest, and split membership are unavailable. These details are insufficient to reconstruct training or identify the checkpoint's complete lineage.

## Validation and test metrics for the deployed model

No independent held-out evaluation report or prediction table for `threatvision_v01.keras` is available. Therefore this portfolio reports no local accuracy, ROC-AUC, precision, recall, F1, false-positive rate, calibrated operating point, or confusion matrix. The project-facing confusion matrix identified by the audit sums to the entire MaleX corpus rather than its described 15% holdout; it is not reproduced as a ThreatVision result.

## Literature benchmark results

The values ROC-AUC 0.970, recall 94.0%, precision 84.7%, F1 0.891, and a 0.380 operating threshold are reported in the project audit as results from Mohammed et al. (2021) on MaleX. They describe prior literature, not evaluation of the local deployed checkpoint. The foundational paper's full metric context should be checked against the final publisher record before quoting those values in any formal academic submission. The current portfolio attributes them explicitly and records this verification task in the publication review.

## Local observations recorded by the audit

- A 2 MB pseudo-random byte input reportedly produced `P(malware)=0.9878`, with an inference time of about 474 ms.
- A compressed PDF reportedly received a score above 0.95.
- A structured text PDF reportedly received a score around 0.041.
- A constant-byte stream reportedly received a score below 0.05.
- Selected CPU inference observations were around 350–500 ms.

These are reported probes, not independently reproduced results. The supplied record does not provide a complete sample list, repeat counts, a pre-registered protocol, uncertainty estimates, or a representative population. They cannot establish an error rate, causal feature, or contemporary-malware performance.

## Comparability limits

The local checkpoint, missing phase-two checkpoint, and literature SE-ResNet are not comparable based on the available records. Training data, partitions, preprocessing parity, checkpoint selection, and evaluation protocols are not jointly documented. Do not compare the local observations numerically against published benchmark metrics.

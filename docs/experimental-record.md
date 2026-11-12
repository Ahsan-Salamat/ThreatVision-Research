# Experimental Record

This record separates the deployed artifact, selected diagnostic probes, and results reported in prior literature. The training and evaluation records needed to reproduce the local checkpoint are unavailable.

## Model artifacts

| Model reference | Status | Available evidence |
| --- | --- | --- |
| SE-ResNet | Literature model; not deployed in ThreatVision | Discussed in prior work; no local checkpoint or implementation is documented |
| `phase2_best.keras` | Referenced but unavailable | A local path is mentioned in project materials, but the file is not present in the public repository |
| `threatvision_v01.keras` | Deployed inference artifact | MobileNetV2-based topology; 2,424,196 total parameters reported in the project record |

The public repository contains no model weights or training scripts.

## Training evidence for the deployed artifact

The artifact configuration records Adam with a learning rate near `5 × 10⁻⁶`, binary cross-entropy, a MobileNetV2 backbone, horizontal flips and small random rotations during training, and dropout in the classification head. This configuration is not a training history. Epoch logs, loss curves, model-selection records, class weighting, dataset manifest, and split membership are unavailable. The configuration cannot reconstruct training or establish the checkpoint's lineage.

## Local evaluation evidence

No independent held-out evaluation report or prediction table for `threatvision_v01.keras` is available. This repository therefore reports no local accuracy, ROC-AUC, precision, recall, F1, false-positive rate, calibrated operating point, or confusion matrix.

## Diagnostic probes

Selected probes recorded a high neural score for pseudo-random bytes and compressed PDF content, and lower scores for a structured text PDF and a constant-byte stream. These inputs probe model response beyond the intended Windows PE triage domain. The available record does not include a complete sample list, repeat counts, controlled comparisons, or uncertainty estimates. The scores cannot establish a false-positive rate, causal feature, or performance on representative malware and benign PE files.

CPU inference observations around 350–500 ms are selected timings, not a controlled latency benchmark.

## Results from the byte-bigram/DCT study

Mohammed et al. (2021) introduced the MaleX corpus with 1,044,394 PE files: 864,669 labeled malicious and 179,725 benign. For balanced CNN experiments, the paper describes 70% training, 20% validation, and 10% test partitions; it also evaluates a much larger left-out set consisting only of malicious files. The paper reports a mean binary accuracy of 96% across its balanced MaleX experiments and 83.60% accuracy on the larger all-malicious test subset. Since that subset contains only malicious files, the result cannot estimate benign false positives. Its ROC figure reports AUC 0.9706473 for a curve built over training, validation, and test scores because the larger test subset contains only one class; it is not a held-out test AUC. These results describe the published study and its protocol, not ThreatVision.

Several values previously repeated in project materials—94% recall, 84.7% precision, F1 0.891, and a 0.380 threshold—could not be verified in the cited paper. The paper describes a 0.5 decision threshold. Those unverified values are omitted here rather than attributed to the source. See [References](references.md) for the corrected HICSS citation.

## Comparability limits

The local MobileNetV2 checkpoint and the paper's CNN/ResNet experiments are not directly comparable. Training data, preprocessing parity, checkpoint selection, and evaluation protocols are not jointly documented. Do not interpret the local probes as performance measurements or compare them numerically with MaleX results.

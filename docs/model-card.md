# ThreatVision Model Card

This model card describes the deployed MobileNetV2-based inference artifact as far as the available project evidence permits. It follows the reporting principles proposed by Mitchell et al. (2019). Important training and evaluation fields remain unavailable and are left explicit rather than inferred.

## Model details

- **Artifact:** `threatvision_v01.keras` (not included in this documentation-only portfolio)
- **Architecture:** grayscale input adapter, ImageNet MobileNetV2 backbone, global average pooling, dropout and dense binary head
- **Input:** 224 × 224 × 1 spectrogram, normalized to `[0,1]`
- **Output:** scalar sigmoid score interpreted by the application as `P(malware)`
- **Model owner / developer:** ThreatVision project authors, Ahsan Ali Salamat and Usman Manzoor
- **Version:** model artifact named `v0.1`; exact version-control lineage is unavailable

## Intended use

The model is used as an advisory signal in an academic pre-execution file-triage application. It is not an autonomous endpoint protection product, a malware family attribution tool, or a substitute for controlled analysis by a qualified analyst. The final malware/benign label is determined by static-analysis criteria; the CNN score may change the numeric threat score by at most five points.

## Factors and input scope

The neural branch consumes an image derived from consecutive byte-pair counts and DCT-II coefficients. The application also computes PE structure and static features, but those signals are handled by the separate static scorer. Although the transform can process arbitrary byte sequences, the final scorer depends heavily on PE structures. Performance by file format, entropy, packing status, family, collection date, or signing status has not been established.

## Training data

- **Dataset name and provenance:** unavailable for the local model.
- **Collection dates, labels, sample counts, deduplication, partitions:** unavailable.
- **Training history and model-selection record:** unavailable.
- **MaleX:** a separate published benchmark associated with Mohammed et al. (2021); use of MaleX to train this checkpoint has not been verified.

## Evaluation

No independently documented held-out evaluation metrics are available for this deployed checkpoint. Accordingly, no local ROC-AUC, accuracy, precision, recall, F1, false-positive rate, or calibrated operating threshold is reported here. The 0.970 ROC-AUC, 94.0% recall, 84.7% precision, 0.891 F1, and 0.380 cutoff referenced in project materials are literature-reported values associated with Mohammed et al. (2021) and MaleX; they are not ThreatVision model results.

The project audit records selected input probes where random bytes and a compressed PDF received high neural scores, while a structured text PDF and constant-byte stream received low scores. These are exploratory observations, not an evaluation set or population error estimate. Inference-time observations around 350–500 ms on CPU are also not a controlled benchmark.

## Ethical and technical considerations

High model confidence is not a probability guarantee and does not establish malicious intent. High-entropy benign content may produce elevated scores. A conceptual radial-gradient display in the user interface is not a model explanation: the backend does not compute Grad-CAM gradients. Family names shown by the wider application are heuristic profiles, not predictions from a validated multi-class family model.

The model is blind to behavior that occurs only at runtime, including memory-only payloads and dynamic unpacking. It may not generalize to non-PE files, newer malware, unseen collection sources, or changing packers. No security, safety, or deployment claim is supported by the available evaluation evidence.

## Caveats and recommended use

Treat the neural score as one exploratory signal alongside the static evidence dossier. Do not use it as a standalone verdict, block/allow control, family attribution, or substitute for sandboxing and expert review. Any future use beyond demonstrations should begin with provenance documentation, leakage-resistant evaluation, calibration, robustness testing, and a clearly bounded intended-use statement.

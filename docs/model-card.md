# ThreatVision Model Card

This model card describes the deployed MobileNetV2-based inference artifact only to the extent supported by the project record. It follows the reporting principles proposed by Mitchell et al. (2019); unavailable fields are stated rather than inferred.

## Model details

- **Artifact:** `threatvision_v01.keras` (not included in this repository)
- **Architecture:** grayscale input adapter, ImageNet MobileNetV2 backbone, global average pooling, dropout, and dense binary head
- **Input tensor:** 224 × 224 × 1 spectrogram, normalized to `[0,1]`
- **Output:** scalar sigmoid score interpreted by the application as a malware score
- **Project authors:** Ahsan Ali Salamat and Usman Manzoor, original collaborative capstone authors
- **Artifact version:** filename includes `v01`; exact version-control lineage is unavailable

## Intended use and scope

The model was developed as an advisory signal for pre-execution Windows PE triage. Its local training distribution is undocumented. The transform can process arbitrary bytes, and the application accepts some non-PE files, but these facts do not establish that such inputs belong to the validated model domain. The final malware/benign label comes from static-analysis criteria; the CNN can change the numeric threat score by at most five points.

It is not an autonomous endpoint-protection product, a validated malware-family classifier, or a substitute for controlled analysis by a qualified analyst.

## Inputs and factors

The neural branch consumes an image derived from adjacent byte-pair counts and DCT-II coefficients. PE structure and selected static features are processed separately by the heuristic scorer. Performance by file format, entropy, packing status, family, collection date, or signing status has not been established.

## Training data and evaluation

The local dataset name and provenance, collection dates, labels, sample counts, duplicate controls, partitions, training history, and model-selection record are unavailable. Use of MaleX to train this checkpoint has not been verified.

No independently documented held-out metrics are available. This repository reports no local ROC-AUC, accuracy, precision, recall, F1, false-positive rate, or calibrated operating threshold. Selected random-byte and PDF probes are out-of-domain diagnostics, not an evaluation set or a population error estimate. CPU timing observations are not a controlled benchmark.

## Ethical and technical considerations

A model score is not a probability guarantee and does not establish malicious intent. The selected probes raise a question about sensitivity to entropy or other correlated properties but do not demonstrate shortcut learning. The user-interface heatmap is a CSS illustration, not a model explanation. The wider application's family names are heuristic profiles, not validated neural predictions.

The model cannot observe behaviors that occur only at runtime, such as memory-only payloads or dynamic unpacking. Generalization to newer malware, unseen sources, non-PE files, and changing packers has not been established.

## Recommended use

Treat the neural score as an exploratory signal alongside the static evidence dossier. Do not use it as a standalone verdict, blocking control, family attribution, or replacement for sandboxing and expert review. Any broader use requires documented provenance, leakage-resistant evaluation, calibration, robustness testing, and a bounded intended-use statement.

# ThreatVision Model Card

This model card describes the deployed MobileNetV2-based inference artifact only to the extent supported by the project record. It follows the reporting principles proposed by Mitchell et al. (2019); unavailable fields are stated rather than inferred.

The university record lists the Final Year Project as a group submission by Ahsan Ali Salamat and Usman Manzoor. The technical development described in this card was completed independently by Ahsan Ali Salamat.

## Model details

- **Artifact:** `threatvision_v01.keras` (not included in this repository)
- **Architecture:** grayscale input adapter, MobileNetV2 backbone (ImageNet initialization reported but not independently verified), global average pooling, dropout, and dense binary head
- **Input tensor:** 224 × 224 × 1 spectrogram, normalized to `[0,1]`
- **Output:** scalar sigmoid score interpreted by the application as a malware score
- **Technical developer:** Ahsan Ali Salamat, The University of Faisalabad
- **Archive metadata:** Keras 3.14.1; saved 2026-05-15
- **Parameter count:** 2,422,084 total, 1,512,580 trainable, and 909,504 non-trainable, recomputed from serialized layer shapes and trainability flags
- **Saved compile configuration:** Adam at approximately `5 × 10⁻⁶`, binary cross-entropy, and accuracy, ROC AUC, precision, and recall metrics
- **Artifact lineage:** a debug script references `phase2_best.keras`, but the file and an export record are unavailable

## Intended use and scope

The model was developed as an advisory signal for pre-execution Windows PE triage. Its local training distribution is undocumented. The transform can process arbitrary bytes, and the application accepts some non-PE files, but these facts do not establish that such inputs belong to the validated model domain. The final malware/benign label comes from static-analysis criteria; the CNN can change the numeric threat score by at most five points.

It is not an autonomous endpoint-protection product, a validated malware-family classifier, or a substitute for controlled analysis by a qualified analyst.

## Inputs and factors

The neural branch consumes an image derived from adjacent byte-pair counts and DCT-II coefficients. PE structure and selected static features are processed separately by the heuristic scorer. Performance by file format, entropy, packing status, family, collection date, or signing status has not been established.

## Training data and evaluation

The local dataset name and provenance, collection dates, labels, sample counts, duplicate controls, partitions, training history, and model-selection record are unavailable. Use of MaleX to train this checkpoint has not been verified. The saved compile configuration records optimizer settings but does not establish the complete training history or data.

No independently documented held-out metrics are available. This repository reports no local ROC-AUC, accuracy, precision, recall, F1, false-positive rate, or calibrated operating threshold. The supplied diagnostic pilot contains ten rows labeled benign PE, twenty transformations of two of those files, and synthetic or out-of-domain probes; it contains no known-malicious PE cohort. Its neural scores and final labels are exploratory observations, not performance estimates. CPU timing observations are not a controlled benchmark.

## Ethical and technical considerations

A sigmoid output is reported as a neural score; it is not a calibrated probability. The overlay responses varied across two source files, and the transformations changed several byte properties at once. They do not establish entropy as the cause or prove shortcut learning. The user-interface heatmap is a CSS illustration, not a model explanation. The wider application's family names are heuristic profiles, not validated neural predictions.

The model cannot observe behaviors that occur only at runtime, such as memory-only payloads or dynamic unpacking. Generalization to newer malware, unseen sources, non-PE files, and changing packers has not been established.

## Recommended use

Treat the neural score as an exploratory signal alongside the static evidence dossier. Do not use it as a standalone verdict, blocking control, family attribution, or replacement for sandboxing and expert review. Any broader use requires documented provenance, leakage-resistant evaluation, calibration, robustness testing, and a bounded intended-use statement.

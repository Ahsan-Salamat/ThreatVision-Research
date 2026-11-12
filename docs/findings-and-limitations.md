# Findings and Limitations

## What the available observations show

Selected probes produced different neural scores: pseudo-random bytes and compressed PDF content received high scores, while a structured text PDF and constant-byte input received low scores. This is evidence of the recorded outputs for those inputs only. It is not an estimate of error rates or deployment performance. The available record lacks repeated trials, a complete protocol, representative sampling, and uncertainty estimates.

## Intended inputs and diagnostic probes

ThreatVision was designed for Windows PE triage, although the local training distribution is not documented. The deployed transform can process arbitrary bytes, and the upload path accepts some non-PE formats. The PDF and random-byte inputs were diagnostic probes outside the model's intended PE domain. Their scores cannot be counted as false positives in an operational or statistical sense.

## Shortcut-learning hypothesis

One possible explanation is that the CNN responds to entropy or spectral dispersion that correlates with labels in its training data. The selected scores are compatible with that hypothesis but do not identify a causal feature. Packing, file format, data source, label confounding, preprocessing behavior, and checkpoint lineage are also unresolved. Shortcut learning has not been demonstrated for ThreatVision, and dataset noise has not been established as the sole cause.

## Missing data and evaluation evidence

The local training source, acquisition dates, label process, sample counts, duplicate handling, and split manifest are not documented. Training histories, independent holdout results, prediction-level outputs, threshold calibration, and external-dataset evaluation are also unavailable. The repository makes no local accuracy, ROC-AUC, precision, recall, F1, false-positive-rate, or calibrated-threshold claim. Literature results for MaleX cannot fill these gaps.

## Static analysis and decision logic

The application is pre-execution and cannot observe runtime unpacking, memory-only payloads, process hollowing after launch, or other behavior that requires execution. Its fusion scorer depends on PE structure, so non-PE inputs may lack relevant signals. Imports and section indicators are heuristics, not proof of malicious behavior. The static weights and thresholds have not been independently calibrated. Static criteria determine the final binary label; the CNN can adjust the numerical score by at most five points, but this design does not establish that either signal is accurate.

## Model and interface

The deployed artifact is MobileNetV2-based. SE-ResNet is a literature architecture, not a deployed ThreatVision checkpoint. Family labels are rule-based profiles rather than validated multi-class predictions. The interface heatmap is a CSS illustration; the backend does not compute Grad-CAM or another gradient attribution. The local inference threshold is reported as 0.50, but no calibration evidence is available.

## Threats to validity

- **Construct validity:** A threat score and a malware label represent different concepts; a high score does not establish malicious intent.
- **Internal validity:** Missing training and split records prevent attributing the observed scores to one feature or cause.
- **External validity:** The selected probes do not represent Windows PE deployment populations or current malware.
- **Conclusion validity:** No independent metrics or uncertainty estimates support performance comparisons.
- **Reproducibility:** The public materials describe the preprocessing and model topology, but omit weights, training data, training history, and complete evaluation artifacts.

The engineering phase is complete for practical reasons. The scientific questions remain open; proposed follow-up work is described in [Future research](future-research.md).

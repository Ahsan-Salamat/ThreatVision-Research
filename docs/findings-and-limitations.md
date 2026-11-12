# Findings and Limitations

## Observed behavior

The available audit records selected probes in which random bytes and a compressed PDF received high neural malware scores, while a structured text PDF and constant-byte input received low scores. This is a verified report that those selected probes were run, not a verified estimate of model performance. The audit does not provide repeated trials, representative sampling, confidence intervals, or a complete protocol.

## Shortcut-learning hypothesis

One possible explanation is that the CNN responds to entropy or broadband spectral dispersion that correlates with labels in its training data. The observed outputs are consistent with that possibility, but they do not establish a causal mechanism. Dataset noise has not been proven to be the sole cause. Other explanations—including class/source confounding, preprocessing behavior, checkpoint lineage, or an unrepresentative test input—remain unresolved because local training provenance and histories are unavailable.

## Dataset representativeness and contamination

The local training source, acquisition dates, label process, sample counts, exact/near-duplicate handling, and split manifest are missing. The project cannot establish whether the local training data represents benign packed software, new malware families, current distributions, or different file types. It also cannot rule out duplicates or train/test contamination. These gaps prevent a reliable assessment of generalization.

## Missing training and evaluation evidence

No epoch histories, validation logs, independent holdout results, prediction-level outputs, threshold calibration, or external-dataset report are available. The published MaleX metrics are literature results and cannot fill these gaps. The selected input probes and CPU timing observations do not constitute a benchmark.

## Static-analysis limitations

The application is pre-execution and cannot observe runtime unpacking, memory-only payloads, process hollowing after launch, or behavior that only occurs after execution. Its fusion scorer depends heavily on Windows PE structure; non-PE files may lack structural signals or receive incomplete scoring. Imports and section indicators are heuristics, not proof of malicious behavior. Manually chosen weights and thresholds are not shown to be calibrated on an independent dataset.

## Model and interface discrepancies

The deployed artifact is MobileNetV2-based. SE-ResNet appears in project-facing materials as a literature model, but no such local checkpoint is available. The family profiles are rule-based entropy/sparsity heuristics, not a verified multi-class neural classifier. The UI heatmap is a CSS radial-gradient concept; the backend does not compute gradients or live Grad-CAM. The deployed inference threshold is reported as 0.50; the 0.380 cutoff in project-facing material is a literature recommendation.

## Threats to validity

- **Construct validity:** A malware label and a threat score may encode different concepts. A high score is not proof of malicious intent.
- **Internal validity:** Missing training and split records prevent attributing model behavior to one feature or intervention.
- **External validity:** Selected synthetic and structured probes do not represent deployment populations or current malware.
- **Conclusion validity:** No independent metric estimates uncertainty or supports performance comparisons.
- **Reproducibility:** The checkpoint and preprocessing description exist in the audited project, but the dataset, training history, and complete evaluation artifacts do not.

The current engineering phase is complete for practical reasons, not because these scientific limitations have been resolved. See [Post-submission investigation](post-submission-investigation.md) and [Future research](future-research.md).

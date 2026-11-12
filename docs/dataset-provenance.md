# Dataset Provenance

## Local training and evaluation data

The available handoff does not establish the provenance, acquisition dates, licensing, exact sample counts, label sources, deduplication procedure, or train/validation/test membership of the data used to train `threatvision_v01.keras`. Local training histories and a retained independent evaluation report are also unavailable. Consequently, this portfolio does not attribute local training to the MaleX dataset and does not report local accuracy, precision, recall, F1, or ROC-AUC.

Before a reproducible evaluation, authors should document the exact dataset version, collection window, permitted use, SHA-256-based duplicate policy, label source and confidence, file-format inclusion rules, family grouping, and split manifest. Malware binaries must not be included in the public documentation repository.

## MaleX in the literature

The MaleX corpus is a separate literature benchmark described by Mohammed et al. (2021), with 1,044,394 PE executables and a reported class composition of 864,882 malicious and 179,512 benign files. The handoff lists a 70/15/15 train/validation/test partition. These are literature details and must remain clearly attributed to that publication. They are not evidence about ThreatVision's local model training data.

The paper reports ROC-AUC 0.970, recall 94.0%, precision 84.7%, and F1 0.891 in its benchmark context. These numbers must not be presented as ThreatVision results. The project-facing confusion matrix identified in the audit sums to the full corpus rather than the stated 15% holdout split, so it is not reproduced here as an independent test result.

## Available local test observations

The audit records synthetic inputs including repetitive bytes, random bytes, and a structured header plus random noise. These are focused probes, not a curated labeled dataset. Selected random inputs produced a high CNN score, while a structured text PDF produced a low score and a compressed PDF produced a high score. No population-level inference can be made from these examples.

## Dataset governance for future work

A publishable study should keep sample binaries in an appropriately controlled environment and publish only safe metadata: source identifiers where licensing permits, hashes for benign samples when safe, split manifests, transformation scripts, and aggregate statistics. Malware hashes can be sensitive and should be reviewed before publication. Dataset licenses and redistribution rights require author verification.

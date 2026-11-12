# Dataset Provenance

## Training and evaluation data for ThreatVision

The public project record does not establish the source, acquisition dates, licensing, sample counts, label provenance, duplicate handling, or train/validation/test membership of the data used for `threatvision_v01.keras`. Training histories and an independent evaluation report are also unavailable. It is therefore not possible to say whether the local checkpoint used MaleX, or to report local accuracy, precision, recall, F1, or ROC-AUC.

A future evaluation should record the dataset version, collection window, permitted use, exact and near-duplicate policy, label source and confidence, file-format rules, family grouping, and split manifest. Malware binaries should remain in an appropriately controlled environment rather than in this public documentation repository.

## MaleX in the cited study

Mohammed et al. (2021) describe MaleX as 1,044,394 PE executables, including 864,669 labeled malicious and 179,725 benign files. For balanced CNN experiments, the paper describes 70/20/10 training, validation, and test splits. It also uses a much larger left-out subset containing only malicious files to examine generalization. These are details of the published study, not evidence about ThreatVision's local training data.

The paper reports mean binary accuracy of 96% across its balanced MaleX experiments. Other reported results use different evaluation contexts, including an all-malicious test subset and an ROC curve that includes training and validation scores. These figures must not be presented as a single held-out benchmark result or as ThreatVision results; see [Experimental record](experimental-record.md) for details.

## Diagnostic inputs

The available project record describes probes with repetitive or constant bytes, random bytes, and structured or compressed PDFs. Such inputs help reveal how a model responds to selected byte patterns, but PDFs and random streams are outside the model's intended Windows PE triage domain. They are not a representative labeled test set. The observed score differences do not establish a population false-positive rate or prove sensitivity to entropy.

## Dataset governance for future work

A future study should keep sample binaries in a controlled environment and share only metadata that is safe and permitted: source identifiers where licensing allows, hashes where appropriate, split manifests, transformation details, and aggregate statistics. Dataset licenses and redistribution rights require verification before data are collected or published.

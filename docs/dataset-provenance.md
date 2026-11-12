# Dataset Provenance

## Training and evaluation data for ThreatVision

The public project record does not establish the source, acquisition dates, licensing, sample counts, label provenance, duplicate handling, or train/validation/test membership of the data used for `threatvision_v01.keras`. Training histories and an independent evaluation report are also unavailable. It is therefore not possible to say whether the local checkpoint used MaleX, or to report local accuracy, precision, recall, F1, or ROC-AUC.

A future evaluation should record the dataset version, collection window, permitted use, exact and near-duplicate policy, label source and confidence, file-format rules, family grouping, and split manifest. Malware binaries should remain in an appropriately controlled environment rather than in this public documentation repository.

## MaleX in the cited study

Mohammed et al. (2021) describe MaleX as 1,044,394 PE executables, including 864,669 labeled malicious and 179,725 benign files. For balanced CNN experiments, the paper describes 70/20/10 training, validation, and test splits. It also uses a much larger left-out subset containing only malicious files to examine generalization. These are details of the published study, not evidence about ThreatVision's local training data.

The paper reports mean binary accuracy of 96% across its balanced MaleX experiments. Other reported results use different evaluation contexts, including an all-malicious test subset and an ROC curve that includes training and validation scores. These figures must not be presented as a single held-out benchmark result or as ThreatVision results; see [Experimental record](experimental-record.md) for details.

## Post-submission diagnostic inputs

The supplied measurements contain ten rows labeled benign PE, twenty transformed files derived from two of those PEs, six out-of-domain probes, eight synthetic random streams, and two synthetic constant streams. The CSV records SHA-256 hashes, but the source manifest, label verification, original transformation inputs, and random seeds are not supplied. The transformed rows are dependent on their two source PEs; the remaining rows' independence is not established. No known-malicious PE appears in the table.

PDFs, random byte streams, constant streams, and the synthetic `MZ`-plus-random input are diagnostic probes rather than representative Windows PE evaluation cases. A PE signature or parser flag on a synthetic byte stream does not make it a valid benign or malicious PE example. These observations cannot estimate population error rates or establish that entropy caused a neural score.

The sample-level measurement CSV is kept outside the public repository pending confirmation of source-data and derived-measurement redistribution terms. Aggregate results and their limitations appear in the [Experimental record](experimental-record.md).

## Dataset governance for future work

A future study should keep sample binaries in a controlled environment and share only metadata that is safe and permitted: source identifiers where licensing allows, hashes where appropriate, split manifests, transformation details, and aggregate statistics. Dataset licenses and redistribution rights require verification before data are collected or published.

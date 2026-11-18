# Dataset Provenance

## Training and evaluation data for ThreatVision

The public project record does not establish the source, acquisition dates, licensing, sample counts, label provenance, duplicate handling, or train/validation/test membership of the data used for `threatvision_v01.keras`. Training histories and an independent evaluation report **for that exact 224×224 deployment checkpoint** remain unavailable; separate historical notebook outputs and a 22-row training CSV have been recovered but cannot yet be linked to it. It is therefore not possible to say whether the local checkpoint used MaleX, or to report local accuracy, precision, recall, F1, or ROC-AUC.

A future evaluation should record the dataset version, collection window, permitted use, exact and near-duplicate policy, label source and confidence, file-format rules, family grouping, and split manifest. Malware binaries should remain in an appropriately controlled environment rather than in this public documentation repository.

## Recovered local development records — separate from the deployed model

The developer also recalls an **approximately 85% MobileNetV2** run. This is an **unverified historical recollection**, not a label- or split-verified benchmark; the available notebook/log exports do not record it. See [the claim-evidence reconciliation](audits/HISTORICAL_ACCURACY_CLAIM.md).

The recovered `ThreatVision.ipynb` output records 4,000 matched image entries (2,000 per label) and a **2,800/800/400** training/validation/test split, while `Copy of MaleX_matched_images.csv` provides 4,000 distinct 64-character hash strings. Its saved outputs also print **67.00%** test accuracy for a scratch CNN and **61.50%** for a separate MobileNetV2. These are historical notebook outputs, *not independently reproduced experimental results*, and no source images or PE binaries accompanied the exports. In particular, neither the sample labels nor group/lineage independence can be independently established from the hashes alone.

A different notebook, `ThreatVisionFInal.ipynb`, prints class-folder counts of **39,999** benign DCT images and **39,998** malware DCT images (79,997 entries). It records the beginning of a distinct 256×256 MobileNetV2 training attempt, **not a verified completed training run**. Its training and validation directory loaders use different `shuffle` settings despite using the same `validation_split`, a potential split-overlap problem requiring dataset reconstruction. A third notebook, `Untitled0.ipynb`, records separate family-classification/residual-CNN work and must not be treated as the deployed binary model.

The available 22-row `training_log.csv` contains **two epoch sequences** and records `val_auc=0.0` and `val_precision=1.0` in every row. Neither split membership nor log-to-checkpoint association is established. The recovered **256×256** `best_model.keras` and the previously documented **224×224** `threatvision_v01.keras` are different model artifacts. See the [reconciliation audit](audits/RECOVERY_CROSSCHECK_2026-11-18.md) before using any historical numbers in a research claim.

## MaleX in the cited study

Mohammed et al. (2021) describe MaleX as 1,044,394 PE executables, including 864,669 labeled malicious and 179,725 benign files. For balanced CNN experiments, the paper describes 70/20/10 training, validation, and test splits. It also uses a much larger left-out subset containing only malicious files to examine generalization. These are details of the published study, not evidence about ThreatVision's local training data.

The paper reports mean binary accuracy of 96% across its balanced MaleX experiments. Other reported results use different evaluation contexts, including an all-malicious test subset and an ROC curve that includes training and validation scores. These figures must not be presented as a single held-out benchmark result or as ThreatVision results; see [Experimental record](experimental-record.md) for details.

## Post-submission diagnostic inputs

The supplied measurements contain ten rows labeled benign PE, twenty transformed files derived from two of those PEs, six out-of-domain probes, eight synthetic random streams, and two synthetic constant streams. The CSV records SHA-256 hashes, but the source manifest, label verification, original transformation inputs, and random seeds are not supplied. The transformed rows are dependent on their two source PEs; the remaining rows' independence is not established. No known-malicious PE appears in the table.

PDFs, random byte streams, constant streams, and the synthetic `MZ`-plus-random input are diagnostic probes rather than representative Windows PE evaluation cases. A PE signature or parser flag on a synthetic byte stream does not make it a valid benign or malicious PE example. These observations cannot estimate population error rates or establish that entropy caused a neural score.

The sample-level measurement CSV is kept outside the public repository pending confirmation of source-data and derived-measurement redistribution terms. Aggregate results and their limitations appear in the [Experimental record](experimental-record.md).

## Dataset governance for future work

A future study should keep sample binaries in a controlled environment and share only metadata that is safe and permitted: source identifiers where licensing allows, hashes where appropriate, split manifests, transformation details, and aggregate statistics. Dataset licenses and redistribution rights require verification before data are collected or published.

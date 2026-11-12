# Future Research

This plan is proposed work. It begins with provenance because the pilot cannot currently be reproduced and the deployed checkpoint's training data and history are unknown. The main question is whether the existing byte-bigram/DCT representation adds useful classification information beyond simpler file statistics and PE static features.

## 1. Recover and validate provenance

- **Hypothesis:** The deployed checkpoint and preprocessing can be identified and reproduced from recoverable artifacts.
- **Baseline and data:** `threatvision_v01.keras`, the production preprocessing implementation, archived representative input bytes, and any recoverable training or export records.
- **Confounders:** Missing weights or source data, changes in library versions, and undocumented training-serving differences.
- **Measure:** Checkpoint hashes, tensor and image equivalence, and neural-score differences on fixed inputs.
- **Falsification:** Fail the reproduction claim if exact artifact lineage or agreed input-output tolerances cannot be demonstrated. Continue to later comparisons only with a clearly identified model and preprocessing pipeline.

## 2. Establish a simple statistical baseline

- **Hypothesis:** Size, byte entropy, null fraction, or a one-dimensional byte histogram may account for much of the available signal.
- **Baseline and data:** Logistic regression on pre-specified scalar statistics, followed by a 256-bin histogram model; use a lawful labeled PE collection only if raw binaries, labels, and terms are available.
- **Confounders:** Source and time imbalance, duplicate and family leakage, label uncertainty, and packer prevalence.
- **Measure:** PR-AUC, ROC-AUC, calibration, and TPR at pre-registered FPR operating points, with confidence intervals and per-source/per-packer results.
- **Falsification:** The claim that frequency features add value is not supported if they fail to exceed the simpler baseline by a pre-specified meaningful margin on the same held-out examples.

## 3. Run controlled perturbation experiments

- **Hypothesis:** The current score may respond to file size, entropy, or byte ordering independently of a file's original label.
- **Baseline and data:** Paired original files and transformations with sham controls: content repetition, null padding, histogram-preserving shuffle, and overlays. Begin with known benign PE files; do not treat transformed files as malware examples.
- **Confounders:** Each intervention can alter several byte and representation properties; transformations may invalidate a file or change its parser behavior.
- **Measure:** Paired neural-score changes, static-feature changes, and final-label changes by intervention and source file. Report the exact transformation and byte-level checks.
- **Falsification:** A proposed single-factor explanation is rejected if the transformation changes its intended factor or materially changes uncontrolled properties. Any entropy-specific claim requires a design that separates entropy from size, ordering, and format.

## 4. Compare raw bigrams and DCT representations

- **Hypothesis:** The DCT representation may provide an inductive bias that improves held-out classification over raw normalized bigram matrices.
- **Baseline and data:** Matched CNN architectures on raw bigram matrices and DCT images, trained and evaluated on identical lawful samples and splits.
- **Confounders:** Training seeds, augmentation choices, preprocessing parity, model capacity, and split leakage.
- **Measure:** Paired test-set differences in PR-AUC, ROC-AUC, calibration, and TPR at pre-specified FPRs, with confidence intervals across training seeds.
- **Falsification:** Do not claim a DCT benefit if its performance difference is within the pre-registered equivalence margin or favors the raw-bigram baseline.

## 5. Evaluate static-only and combined systems

- **Hypothesis:** Combining neural scores with static indicators may improve triage over static analysis alone without unacceptable errors in important strata.
- **Baseline and data:** Static-only rules and a combined scorer evaluated on the same independently labeled PE split; freeze all weights and thresholds before final testing.
- **Confounders:** Hand-selected thresholds, class prevalence, packed benign programs, source shifts, and correlated features such as entropy appearing in both branches.
- **Measure:** Per-class and per-stratum precision/recall, PR-AUC, calibration, decision-curve or cost-weighted errors, and exact confidence intervals for FPR and TPR.
- **Falsification:** The combined system adds no supported value if the pre-specified improvement criterion is not met or if packed-benign errors exceed a pre-registered acceptable bound.

## 6. Reconsider dataset construction only if needed

- **Hypothesis:** Existing datasets may lack the raw binaries, provenance, benign packed software, or label quality needed for the controlled comparisons above.
- **Baseline and data:** Audit candidate datasets and their terms before proposing a new collection; document which required strata and raw files are available.
- **Confounders:** Dataset licensing, label provenance, temporal mismatch, duplicate families, and selection bias.
- **Measure:** Coverage against a pre-specified requirements matrix and a documented feasibility/rights review.
- **Falsification:** A new dataset is not justified if an existing lawful source supports the required comparisons with adequate provenance and strata.

## Sample size and uncertainty

A 4,000-file balanced benchmark would provide about 2,000 benign test cases if half were reserved for testing. Even with zero false positives among 2,000 independent benign examples, the approximate one-sided 95% upper bound is 0.0015 (the rule-of-three approximation). That sample therefore cannot establish an FPR at or below 0.001 with 95% confidence. Roughly 3,000 independent benign test cases with zero false positives are needed just to put that upper bound near 0.001; clustering by source or family and any observed errors increase the required sample. The final sample size should be calculated from a pre-specified interval width and target operating point, not fixed in advance at 4,000.

Public benchmark names do not guarantee access to raw executable files suitable for the DCT pipeline. EMBER2024 documents a release of extracted features and labels; those features alone cannot be passed through ThreatVision's byte-to-DCT pipeline. BODMAS describes PE files, vectors, and metadata, but its file availability and use terms still need to be checked for the intended study [7, 11]. Confirm raw-binary access, label source, data-use terms, and safe handling before selecting either dataset. No duration is promised for the full research program; provenance recovery, data governance, model comparisons, and independent review may exceed a short laptop study.

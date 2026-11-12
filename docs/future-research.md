# Future Research

The questions below are proposed research, not completed experiments. The purpose is to define a study that could test the concerns raised by the current project without assuming that a new dataset or model will solve them.

## Research questions

1. How much do byte-bigram/DCT features contribute beyond entropy, packing, file format, and dataset-source characteristics?
2. How do label noise, duplicate or near-duplicate samples, and source contamination affect measured performance?
3. Does the model generalize across collection periods, malware families, packers, and file formats?
4. Do frequency and static PE signals provide complementary information compared with simpler static baselines?
5. How well calibrated are model scores, and when should the system abstain or defer to an analyst?
6. Can feature explanations on DCT coordinates be validated for faithfulness and stability?

## Proposed data and provenance plan

Begin by selecting lawful data sources with recorded acquisition windows and clear terms of use. Preserve provenance at sample or source-batch level. Record label source, label date, confidence or consensus rule, file type, packing status, and cryptographic hashes in a controlled manifest. Deduplicate exact hashes and investigate near duplicates and family overlap. Keep raw malware samples in a restricted research environment; publish only metadata that is safe and permitted to share.

The dataset should include benign compressed installers, packed utilities, signed software, corrupted or malformed files, and non-PE examples where relevant, rather than treating high entropy or a packer flag as synonymous with maliciousness. A new dataset could improve documentation and control but would not automatically remove bias, label error, or distribution shift.

## Proposed experimental design

- Freeze training, validation, and test partitions before model selection. Group related samples by family or campaign when possible and include a time-separated test period.
- Compare simple static-feature baselines, the existing bigram/DCT model, a byte or spatial-image baseline, and static/visual fusion. Use common partitions and label definitions.
- Stratify results by file type, entropy band, packing status, signer status, source, and time period.
- Ablate null suppression, the DCT transform, each static feature group, and the CNN score adjustment.
- Compare random splits with family-grouped and temporal splits to study leakage and drift.
- Pre-register operating thresholds and report ROC-AUC and PR-AUC alongside false-positive rate at fixed recall, calibration, per-stratum errors, and confidence intervals.
- Test selected semantics-preserving transformations and unseen packers where safely and lawfully available.
- Evaluate gradient-derived explanations only after checking their stability under controlled perturbations and known input changes.

## Resources and feasibility

A study would require verified dataset rights, secure malware storage and handling, repeatable preprocessing, sufficient compute for model training and ablations, and time for label review and independent evaluation. The project author currently lacks the resources needed for this scope, which is why the present phase is being concluded. This is a feasibility statement, not a claim that compute is the only methodological barrier.

## Expected contribution

The proposed work could clarify how much of the CNN's signal reflects class-related structure versus entropy, packing, or dataset artifacts; quantify the contribution of static PE analysis; and describe where performance changes across time and format. It may also show that one or more approaches are not useful. No superior accuracy or successful mitigation is promised.

## Possible extensions

If the primary study supports them, later work could test contrastive objectives, control-flow graph features, uncertainty-aware abstention, or analyst-facing explanations. These should follow the same provenance and leakage controls and be justified by results from the first study.

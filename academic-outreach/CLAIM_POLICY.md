# ThreatVision academic claim policy — 18 November 2026

## Supported ways to describe the project

- "I independently developed the technical implementation of a university-group-submitted Software Engineering FYP."
- "ThreatVision integrates static PE triage, byte-bigram/DCT visual features, a MobileNetV2-derived advisory score, and an analyst-facing web interface."
- "The representation comes from prior published research, not a novel transform I invented."
- "I recovered eight old notebooks and a separate 256×256 Keras model archive. That archive and the distinct 224×224 production checkpoint safely loaded and passed synthetic runtime probes; neither has a verified training lineage or measured classification performance."
- "The research repository implements safe preprocessing/evaluation tests and documents a proposed controlled study of incremental predictive value."
- "My historical notebooks have saved test-output printouts, but they have not been independently reproduced or tied to the deployed checkpoint."

## Recovered but unverified performance recollection

The developer separately recalls **approximately 85% MobileNetV2 accuracy**, but the recovered notebooks, anomalous 22-row log, and recovered checkpoint archive **do not substantiate this figure** or identify whether it was training, validation or independent test accuracy. Preserve the recollection in the [historical claim register](../docs/audits/HISTORICAL_ACCURACY_CLAIM.md), **not** as a result in the professor-facing email, brief, or prospectus. No epoch rows, plots, confusion matrices or test predictions may be invented to match it.

## Claims **not** supported

- "ThreatVision achieved 85% verified MobileNetV2 test accuracy" — developer-reported historical best without surviving supporting evaluation output, model identity or held-out split.
- "ThreatVision achieves 67% / 61.5% validated detection accuracy" — notebook printouts are historical, and refer to separate older experiments without an independently verified dataset/split.
- "A 79,997-sample experiment proves generalization" — the later run is incomplete in the export and has a partition-overlap risk.
- "The 256×256 recovered model is the production 224×224 model" — metadata and saved layer configurations differ.
- "The 22-epoch CSV proves robust ROC-AUC" — every `val_auc` is 0.0 and class membership is unknown.
- "The public scanner works" — authenticated browser/real inference flow not independently verified.
- "The CNN decides the malware label" — static scoring rules make the final binary decision.
- "I invented byte-bigram/DCT malware visualization" — this technique is from prior literature.
- "I have a peer-reviewed malware paper or a confirmed professor/scholarship" — neither is evidenced here.

## Outreach minimum checklist

- [ ] All corrections present on the public `main` branch, verified remotely
- [ ] Linked one-page summary, evidence reconciliation and prospectus match the README
- [ ] Academic CV correctly states degree, grades, training experience and verified projects
- [ ] No password, token, personal secrets, private Drive sharing link or executable in the public repository
- [ ] Exact professor and publication have been verified, with a tailored fit paragraph
- [ ] Live website omitted until the walkthrough is browser-verified
- [ ] No test accuracy or other benchmark number in cold email
- [ ] Separate research discussion from formal admission requirements

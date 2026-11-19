# ThreatVision — evidence index for academic reviewers

| Question | Strongest currently accessible record | Boundary |
| --- | --- | --- |
| What was engineered? | [README](../README.md), [system architecture](../docs/system-architecture.md), [methodology](../docs/methodology.md), [source tooling](../research/) | Full private application source is not included in the research repository. |
| Which scientific work introduced the representation? | [References](../docs/references.md), [bibliography](../references.bib), HICSS 2021 DOI `10.24251/HICSS.2021.858` | Do not attribute the original DCT representation to ThreatVision. |
| What original artifacts survived? | [Recovery inventory](../docs/audits/recovered-artifact-inventory.md), [archive metadata summary](../docs/audits/recovered-artifact-verified-summary.json) | Raw archives, model weights and notebook source are held privately. |
| Do the experiments and model versions align? | **[Full notebook/manifest/checkpoint reconciliation](../docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md)** | Two different model checkpoints, different datasets, and historical limitations are explicitly separated. |
| What empirical evidence exists? | [46-row pilot record](../docs/experimental-record.md); [historical material](../docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md) | 46-row CSV/data not in recovered ZIPs; notebook printouts are not independently reproduced performance. |
| What runs reproducibly today? | [Reproducibility instructions](../REPRODUCIBILITY.md), [35 safe research tests](../tests/), [production checkpoint verification](../docs/audits/PRODUCTION_CHECKPOINT_VERIFICATION.md), [recovery archive auditor](../research/recovery_audit.py) | The local backend integration uses a harmless generated PE. Synthetic/runtime checks are not a labeled malware benchmark. |
| What is the proposed next study? | [Research prospectus](../docs/research-prospectus.md), [future research](../docs/future-research.md) | Proposed; no completed controlled evaluation. |
| How should I describe this to professors? | [One-page project summary](PROJECT_SUMMARY.md), [claim policy](CLAIM_POLICY.md), [email template](PROFESSOR_EMAIL_TEMPLATE.md) | Email requires actual professor/publication personalization. |
| Which issues remain open? | [Final readiness report](../docs/audits/FINAL_PROFESSOR_OUTREACH_READINESS.md) | The hosted website fails the accuracy review; remote repository content is older than this local checkout. Predictive performance and checkpoint lineage remain unverified. |

## User-reported historical peak

An approximately 85% MobileNetV2 result is **owner-reported, without recovered run evidence**. It is intentionally omitted from claims in the professor email and one-page brief. [Evidence and verification gate](../docs/audits/HISTORICAL_ACCURACY_CLAIM.md); [reconstructed verification notebook](../notebooks/RECONSTRUCTED_MobileNetV2_Validation.ipynb).

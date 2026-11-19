# ThreatVision — undergraduate engineering project and proposed MSc research

**Technical author:** Ahsan Ali Salamat · BS Software Engineering · The University of Faisalabad (Pakistan)
**Formal FYP record:** University group submission with Usman Manzoor; technical implementation is attributed by the author to Ahsan Ali Salamat.
**Repository link:** Add the public repository URL only after the owner publishes the reviewed local changes and verifies the public README and evidence links. The currently reachable remote is older than this summary.

## Engineering project

I independently implemented an analyst-facing Windows Portable Executable (PE) triage system integrating static file analysis, a byte-bigram/frequency-domain image representation, MobileNetV2 inference and a bounded score adjustment. The byte-bigram/DCT technique follows Mohammed et al. (HICSS 2021); it is **not** presented as my invention. The application's final benign/malicious label is determined by static rules. Its neural score can adjust the numerical threat score by at most five points; it does not independently make the final decision.

## Available technical evidence

The repository provides documented architecture, deterministic preprocessing tests, dataset-manifest validation, source/lineage-aware evaluation infrastructure, checkpoint-provenance checks, and an explicitly limited 46-row diagnostic pilot. The companion application's **224×224** production checkpoint was verified against its SHA-256, safely loaded, and run on five deterministic synthetic tensors plus a harmless PE-derived tensor. App and research preprocessing matched exactly at eight stages on three harmless fixtures, and the corresponding actual checkpoint outputs also matched. The local backend completed a harmless generated-PE smoke test with that checkpoint. These checks establish current runtime and implementation parity only. Two recovered historical Colab exports contain original notebooks, a distinct **256×256** Keras checkpoint and a 4,000-image manifest. One older notebook includes unreplicated test-accuracy printouts; a later notebook describes a separate approximately 80,000-image workflow. Neither the historical figures nor the 22-row anomaly-prone training log can be attributed to the production checkpoint. Full audit: [evidence reconciliation](../docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md), [production checkpoint verification](../docs/audits/PRODUCTION_CHECKPOINT_VERIFICATION.md), and [preprocessing parity record](../docs/audits/PRODUCTION_PREPROCESSING_PARITY.md).

## Research question

**Do frequency-domain neural representations add measurable predictive value beyond conventional PE static features when dataset bias, sample lineage, and generalization are properly controlled?**

Proposed approach: compare logistic-regression static-feature and static-plus-frozen-neural-score baselines on the same legally obtained, independently labeled PE cohort; use immutable grouped splits, train-only preprocessing and a prespecified held-out evaluation; assess whether any incremental gain persists under source/time shifts and perturbations. A null result is scientifically informative. This is **proposed work** rather than a completed benchmark.

## Boundaries

- No independently validated malware detection accuracy, ROC-AUC, false-positive rate or calibrated probability is claimed.
- The original PE/PNG training datasets were not included in the reviewed recovery exports. The production checkpoint is present in the companion application tree and its local inference path is verified on synthetic inputs and a harmless PE fixture. The hosted website was browser-audited and fails the academic accuracy review because it still presents unsupported model and performance claims. Do not include its URL in outreach until corrected content is published and independently rechecked.
- The public repository excludes raw binaries, model weights and private application code, pending rights and security review.

**Research interests:** trustworthy malware machine learning, robust evaluation, static PE analysis, dataset shift and machine-learning-assisted triage. I am seeking MSc-level academic discussion and will follow each university's formal admissions process.

**Historical-accuracy note:** A developer-reported approximately 85% MobileNetV2 run is documented only as an unrecovered recollection, not a verified benchmark; see [claim register](../docs/audits/HISTORICAL_ACCURACY_CLAIM.md). No numerical classification-performance claim is used for outreach.

# ThreatVision — undergraduate engineering project and proposed MSc research

**Technical author:** Ahsan Ali Salamat · BS Software Engineering · The University of Faisalabad (Pakistan)
**Formal FYP record:** University group submission with Usman Manzoor; technical implementation is attributed by the author to Ahsan Ali Salamat.
**Public research repository:** https://github.com/Ahsan-Salamat/ThreatVision-Research

## Engineering project

I independently implemented an analyst-facing Windows Portable Executable (PE) triage system integrating static file analysis, a byte-bigram/frequency-domain image representation, MobileNetV2 inference and a bounded score adjustment. The byte-bigram/DCT technique follows Mohammed et al. (HICSS 2021); it is **not** presented as my invention. The application's final benign/malicious label is determined by static rules. Its neural score can adjust the numerical threat score by at most five points; it does not independently make the final decision.

## Available technical evidence

The repository provides documented architecture, deterministic preprocessing tests, dataset-manifest validation, source/lineage-aware evaluation infrastructure, checkpoint-provenance checks, and an explicitly limited 46-row diagnostic pilot. Two recovered historical Colab exports contain original notebooks, a structurally readable earlier **256×256** Keras checkpoint and a 4,000-image manifest. One older notebook includes unreplicated test-accuracy printouts; a later notebook describes a separate approximately 80,000-image workflow. Neither the historical figures nor the 22-row anomaly-prone training log can be attributed to the **different, documented 224×224 deployment checkpoint**. Full audit: [evidence reconciliation](../docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md).

## Research question

**Does a byte-bigram/DCT neural representation add practically meaningful predictive information over PE static features, once sources, families, collection time, packing and duplicate/lineage leakage are controlled?**

Proposed approach: compare logistic-regression static-feature and static-plus-frozen-neural-score baselines on the same legally obtained, independently labeled PE cohort; use immutable grouped splits, train-only preprocessing and a prespecified held-out evaluation; assess whether any incremental gain persists under source/time shifts and perturbations. A null result is scientifically informative. This is **proposed work** rather than a completed benchmark.

## Boundaries

- No independently validated malware detection accuracy, ROC-AUC, false-positive rate or calibrated probability is claimed.
- The original PE/PNG datasets and the exact production checkpoint were not included in the reviewed recovery exports; live inference and current public demo behavior have not been verified.
- The public repository excludes raw binaries, model weights and private application code, pending rights and security review.

**Research interests:** trustworthy malware machine learning, robust evaluation, static PE analysis, dataset shift and machine-learning-assisted triage. I am seeking MSc-level academic discussion and will follow each university's formal admissions process.

**Historical-accuracy note:** A developer-reported approximately 85% MobileNetV2 run is documented only as an unrecovered recollection, not a verified benchmark; see [claim register](../docs/audits/HISTORICAL_ACCURACY_CLAIM.md). No numerical classification-performance claim is used for outreach.

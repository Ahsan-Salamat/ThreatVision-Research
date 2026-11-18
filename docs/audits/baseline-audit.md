# Baseline audit — 17 November 2026

**Historical snapshot:** This baseline predates the November 18 recovery of original Colab notebooks, the 256×256 checkpoint, and training logs. Its references to missing historic materials are superseded by the [recovery crosscheck](RECOVERY_CROSSCHECK_2026-11-18.md).

The research checkout is a separate documentation repository on main at cb27efa. Existing README, ignore-file and screenshot changes were present before this pass. Application source is in sibling frontend and backend Git checkouts. This pass is scoped to ThreatVision-Research as requested.

| Claim | Local evidence |
| --- | --- |
| Bigram transform uses 256 × 256 counts, suppresses (0,0), maximum scales and quantizes before DCT-II, log magnitude and area resize | Application backend/python_scripts/convert_to_bigram_dct.py functions build_bigram_matrix, preprocess_matrix, matrix_to_gray, apply_2d_dct, resize_to_cnn |
| Some comments and entropy metadata incorrectly call the first normalization log1p | Same source, preprocess_matrix and compute_entropy_stats |
| Model input is grayscale float32 divided by 255, batched to 1 × 224 × 224 × 1 | Application backend/python_scripts/classify_image.py lines 215–224 |
| Neural branch uses 0.5 threshold | Same source line 235 |
| Static fusion permits bounded neural score nudges | Application backend/python_scripts/fusion_scorer.py lines 329–408 |
| Local checkpoint exists | backend/python_scripts/model/threatvision_v01.keras, SHA-256 and archive metadata recorded in checkpoint-metadata.json |
| MobileNetV2 archive topology and saved optimizer configuration | checkpoint-metadata.json and ../model-architecture.md |
| Historical training provenance unavailable | ../model-card.md, ../dataset-provenance.md |
| Pilot is source-dependent and lacks verified malicious cohort | ../experimental-record.md |
| Prior local walkthrough exists outside this repository | Sibling frontend/src/components/ResearchDemo.jsx and workspace outreach-package/FINAL_AUDIT.md |

Archive inspection does not establish runtime loading or inference repeatability. No new verified cohort or benchmark was recovered. The 46-row pilot remains diagnostic. The existing architecture and scientific limitations agree on the bounded role of neural scores. The extracted research functions omit stale prose claims about training equivalence because the training source is unavailable.

The frequency-domain paper's arXiv record confirms byte-bigram/DCT image representations. EMBER describes a released static-feature benchmark and a strong non-neural baseline. Those external results supply context and do not measure ThreatVision. [Frequency-domain study](https://arxiv.org/abs/2101.10578) · [EMBER](https://arxiv.org/abs/1804.04637)

A fresh public-demo request through the web tool failed to access the URL. A subsequent curl HEAD request returned HTTP 200 from Netlify, which establishes HTTP availability only. This observation cannot establish that the server is down. The prior 14 November browser audit remains dated evidence. Production demonstration readiness needs a new successful browser inspection.

## Scope of implemented evaluation

The validator rejects duplicate hashes even within one split. This conservative policy requires deduplication before fitting. Known families and lineages must stay in one partition. Source strings are recorded but source confounding and unknown lineage are not detected automatically. The evaluator accepts externally extracted features, so feature provenance and absence of target leakage require review. It does not recreate production static scoring. Its validation partition is reserved and unused because hyperparameters and threshold are fixed.

The research source is a numerical extraction, with a checkpoint/source checksum to identify drift. Production has not yet been refactored to import it. Automated parity tests against the sibling implementation and independent training-time equivalence remain pending.

Three local synthetic parity checks against the original preprocessing passed on 17 November. Inputs were two ASCII bytes, four repetitions of byte values 0–255, and 1,024 null bytes. This verifies those cases only.

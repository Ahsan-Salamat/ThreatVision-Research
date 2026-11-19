# Local reconciliation report

**Updated:** 19 November 2026

This index now reflects the completed checkpoint, preprocessing, application, and training-pipeline verification. The initial local implementation report contains the checkout state, changes, commands, and remaining limits: [`LOCAL_IMPLEMENTATION_REPORT.md`](LOCAL_IMPLEMENTATION_REPORT.md). Final outreach readiness is in [`docs/audits/FINAL_PROFESSOR_OUTREACH_READINESS.md`](docs/audits/FINAL_PROFESSOR_OUTREACH_READINESS.md).

## Current evidence

- The 224×224 production checkpoint and separate recovered 256×256 checkpoint each passed registered-SHA safe loading and six repeatable probes. Neither has independently validated classification performance or established training lineage.
- Three harmless fixtures matched between current application and research preprocessing at eight stages; the real production model returned identical outputs on both implementations' tensors. This is current serving-code parity, not historical training parity.
- The backend's harmless generated-PE HTTP path exercised static analysis, DCT conversion, the checksum-pinned production model, bounded fusion, and API response formatting. No executable was run.
- A one-epoch, CPU-only training CLI smoke completed with fresh random weights and temporary synthetic PE-shaped fixtures. It first exposed a TensorFlow bytes-conversion bug, which was fixed and covered by a regression test. The smoke's pseudo-labels and metrics are not scientific evidence.
- The research suite passes **38/38**; backend Python tests pass **7/7** and Jest passes **11/11**. Frontend lint, score-helper tests, and public/private builds pass locally.
- The hosted website remains unsuitable for professor outreach based on the last successful rendered audit. No commit, push, or deployment occurred.

Predictive performance remains unverified because an authorized, independently labeled, lineage-controlled malware cohort is unavailable. Keep historical notebook printouts, the anomalous training log, the recovered checkpoint, the production checkpoint, and the owner-reported ~85% recollection as separate evidence classes.

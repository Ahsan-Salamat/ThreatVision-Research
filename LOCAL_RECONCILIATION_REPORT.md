# Local reconciliation report

**Date:** 18 November 2026  
**Repository:** `/Users/ahsansalamat/Desktop/ThreatVision/ThreatVision-Research`  
**Branch and base HEAD:** `main`, `5c3d51b550a28af1de763407f7e30d279978495d`

## Starting state and package review

The local Git checkout was clean before integration. The corrected ZIP was present at the requested Downloads path, contained 64 entries, and passed CRC validation. It was extracted to `/tmp/tv-reconciliation-package`, outside the repository. A path-by-path byte comparison found 32 files to add or update. Existing dataset validation, extraction, checkpoint, preprocessing, evaluation, splitting, training, and uncertainty modules matched the ZIP and were preserved. No repository history was replaced, staged, committed, pushed, or deployed.

## Integrated files

Added `DELIVERY_NOTES.md`; the claim policy, professor email template, one-page PDF/DOCX; historical-accuracy and recovery-crosscheck audits; verified artifact summary; reconstructed validation notebook; and the historical-accuracy/recovery-audit modules and tests.

Updated `.gitignore`, README, reproducibility guide, outreach evidence index and project summary, readiness and baseline audits, recovered-artifact inventory, dataset provenance, experimental record, findings/limitations, methodology, model architecture/card, post-submission investigation, research prospectus Markdown and DOCX, and the dashboard screenshot. Added the research prospectus PDF.

## Historical evidence reconciliation

The documents now separate the 4,000-image notebook study, later approximately 79,997-image workflow, 22-row anomalous training log, recovered 256×256 model, and separately documented 224×224 production model. The approximately 85% MobileNetV2 result is explicitly owner-reported and unverified. Historical notebook printouts and the 80.27% maximum validation accuracy are not presented as independently validated results. The recovered validation AUC/precision anomaly and possible later-loader split overlap remain unresolved. No predictions or metrics were fabricated.

## Verification performed

Using `/tmp/tv-research-env/bin/python` with research dependencies installed:

- `python -m unittest discover -s tests -v` — **21 passed, 0 failed** in 4.498 seconds.
- The same 21 tests in a temporary Git-free copy — **21 passed, 0 failed** in 3.899 seconds.
- `python3 -m compileall -q research tests` — passed.
- Notebook JSON inspection — valid nbformat 4. Code cells have no execution counts or output cells.
- DOCX ZIP integrity and PDF signatures — passed.
- ZIP package CRC — passed.
- System `python3 -m unittest discover -s tests -v` — **18 discovered, 13 passed, 5 errored** because the system interpreter lacks NumPy; errors were limited to evaluation/preprocessing imports. The isolated research environment includes the declared numerical dependencies and passed the full suite.
- `git diff --check` — initially found two Markdown hard-break trailing spaces in the updated project summary. They were removed; the final rerun passed.
- Relative Markdown link scan — zero broken local destinations. The reconstructed notebook parses as nbformat 4 and has no executed cells or stored outputs.

Tests exercise synthetic engineering records only. They do not establish malware classification performance. TensorFlow inference/training, recovered model runtime loading, and actual labeled-sample evaluation were not run. The reconstructed notebook was not executed. The original archives and model remain untouched.

## Scientific and outreach status

The recovered model archive and 4,000-row filename/hash manifest are evidence of historical artifacts, not independently verified labels, samples, or test partitions. The historical training log has 22 rows with `val_auc=0.0` and `val_precision=1.0` throughout. The recalled ~85% has no matching saved prediction record. No independently labeled PE cohort or current frontend source is present in this repository. Public demo behavior remains unverified.

The materials support a carefully personalized exploratory email about the independently implemented undergraduate engineering project and a proposed research question. Do not claim validated detection accuracy, exact reconstruction of historical training, or an operational public inference demo.

## Review list

All changes shown by `git status --short` are ready for manual review. The corrected package is the source of these proposed files. The external ZIP is not tracked. Original notebook exports, datasets, model checkpoints, credentials, and private application files remain excluded.

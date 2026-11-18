# Handover — audited ThreatVision research dossier (18 November 2026)

This folder is a **prepared local publishing copy**, based on the owner's `ThreatVision-Research(3).zip` at embedded Git commit `7d3b085` and cross-checked against **both original Drive exports**. This ZIP does not contain `.git`, raw original notebook exports, PE binaries, original PNGs, private application code, or model weights. **It has not been committed, pushed to GitHub, or deployed.**

## Newly prepared or revised material

- `research/recovery_audit.py` — read-only owner-held ZIP metadata auditor; no Keras execution.
- `tests/test_recovery_audit.py` — three additional safe tests (overall **14 PASS**).
- `docs/audits/recovered-artifact-verified-summary.json` — sanitized machine-readable audit evidence generated from the **actual source ZIPs**.
- `docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md` — source-by-source evidence matrix, split-integrity risk, distinct checkpoint topologies and honest scientific boundaries.
- Updated README, `REPRODUCIBILITY.md`, model card, model architecture, dataset provenance, methodology, experimental record, findings, original-artifact inventory, post-submission account, research prospectus and readiness report.
- Updated `docs/research-prospectus.docx` and added matching `docs/research-prospectus.pdf`.
- Created `academic-outreach/PROJECT_SUMMARY.md`, `EVIDENCE_INDEX.md`, `CLAIM_POLICY.md` and `PROFESSOR_EMAIL_TEMPLATE.md`.
- Added a reviewed one-page outreach handout (`academic-outreach/ThreatVision_One_Page_Research_Summary.pdf` and editable `.docx`).

## Testing/verification

- The Drive archive hashes and inner `.keras` hash match the previous inventory and the new machine-readable audit summary.
- ZIP CRC checks passed on both original exports and the nested model archive.
- Safe `python -m unittest discover -s tests -v`: **14 PASS**.
- `python -m compileall -q research tests`: PASS.
- Internal Markdown path check: no broken local destinations at time of packaging.
- Prospectus and one-page handout were rendered to pages and inspected.

## Mandatory owner actions

1. Preserve the original Drive ZIPs, unmodified; do not commit the eight notebooks, model archive or unverified sample data without an appropriate rights/security audit.
2. In your local Git checkout, carefully review this copy's changes, then commit and push approved files. Confirm the remote page and PDF links in an incognito browser. The supplied copy has **no Git metadata**, so the working-tree history and remote state are not represented.
3. Customize `academic-outreach/PROFESSOR_EMAIL_TEMPLATE.md` using a **real paper of the recipient**, and check eligibility for the chosen MSc programme. Use the one-page PDF and GitHub repository as the initial evidence, not an unsupported demo or performance claim.
4. For scientific validation, recover independently labeled raw PE files and group-aware split membership, load each checkpoint in a controlled compatible environment, investigate the original `val_auc=0.0` logs, and conduct genuine held-out evaluation.

**Final classification:** historical-documentary alignment improved, scientific validation **not complete**, suitable for **exploratory, accurate outreach after publication**.

## Supplemental recovered-accuracy clarification (18 November 2026)

Developer-reported ~85% MobileNetV2 is not supported by the recovered notebooks/logs. Added explicit claim ledger, unexecuted reconstructed notebook, strict per-sample accuracy auditor and seven synthetic tests. All **21** safe tests passed in this edited copy. No trained weights, PE samples, prediction records or fabricated outputs were added. See `docs/audits/HISTORICAL_ACCURACY_CLAIM.md`.

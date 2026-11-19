# ThreatVision local implementation report

**Date:** 19 November 2026

## Executive result

Local engineering verification is **PASS for the exercised paths**. Exploratory professor outreach is **PARTIAL** until corrected local research files are manually published and links checked. Publishable malware-classification validation is **BLOCKED** because no independently labeled, lineage-audited PE benchmark is available. The hosted website should not be linked to professors; the last successful rendered audit found unsupported claims.

No commit, push, deployment, reset, or remote modification was performed. All changes remain local and unstaged.

## Checkout state and preservation

| Checkout | Branch and HEAD at start | Initial state |
| --- | --- | --- |
| `ThreatVision-Research` | `main`, `fc0cb95394cde8231fe4e6c8c2045e68b1adb584` | Clean |
| `ThreatVision Final/backend` | `main`, `9516cc659bb3c9c7c159ac5a96139405f0edc745` | Dirty before this work: application edits, logs, coverage, and tests |
| `ThreatVision Final/frontend` | `main`, `28f4294f04089207ae0739f8a661a449339474fa` | Dirty before this work: broad UI, routing, configuration, dependency and lint changes |

The pre-existing backend and frontend edits were preserved. Research HEADs were not changed. There are no staged changes.

## Implemented changes

### Research verification

- Consolidated `research/checkpoint.py` on the shape-aware verifier so both entry points share the same checksum, safe-loading, profile, and probe rules.
- Registered the production 224×224 and recovered 256×256 checkpoint SHA-256 identities. The CLI requires an explicit profile and rejects a hash that does not match that identity before deserializing weights.
- Added a generated harmless PE-derived probe for each checkpoint profile. The 256×256 case is explicitly documented as an engineering resize, not a historical training reconstruction.
- Added `research/preprocessing_parity.py`, which writes machine-readable per-stage hashes, shapes, dtypes, and numerical deltas for the current app and research implementations. It can also compare outputs from the real production checkpoint.
- Added regression coverage for unregistered model identities and exact parity across eight preprocessing stages.
- Fixed a training-smoke defect where `tf.numpy_function` supplied raw bytes but the callback attempted `.numpy()`. Added a regression test for the bytes-to-tensor adapter.

### Backend guard and regression tests

- Pinned `classify_image.py` to the production model SHA-256 before Keras loading. A replacement checkpoint requires an explicit matching `MODEL_SHA256` setting.
- Added `.env.example` documentation and tests for checksum mismatch. The mismatch path does not deserialize the model and does not expose a neural score; the API marks the result simulated.
- Previously present local backend safeguards and loopback-only development auth behavior were retained.

### Research and outreach materials

- Updated the README, reproducibility guide, model card, architecture record, claim policy, evidence index, project summary, and prospectus to reflect the new evidence without changing scientific claims.
- Updated both checkpoint verification JSON records and added the stage-by-stage production parity record.
- Updated the final outreach assessment and this implementation report.
- Refreshed the one-page summary and research prospectus DOCX/PDF versions. The summary remains one page; the prospectus remains two pages. Every rendered page was reviewed after the final edits.

## Runtime evidence

### Production checkpoint

`threatvision_v01.keras` SHA-256: `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`. It loaded with `compile=False, safe_mode=True` in the existing `threatvision` Conda environment (Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1, NumPy 1.26.4). Input shape is `(None,224,224,1)`, output shape `(None,1)`, and parameter count 2,422,084. Five deterministic synthetic probes and one harmless PE-derived probe produced finite sigmoid-range values and repeated exactly (maximum delta 0 at tolerance `1e-7`). The full JSON contains scores, fixture/tensor hashes, profile, package/backend information, and a sanitized path label.

The separate recovered 256×256 checkpoint SHA-256 is `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`. It also loaded safely and passed six repeatable finite-output probes in the same environment under its distinct profile. Its PE-derived engineering input does not establish historical preprocessing parity.

### Application/research preprocessing parity

Three deterministic harmless fixtures were compared across byte stream, bigram counts, zero-pair suppression, normalization, grayscale quantization, DCT output, 224×224 resize, and final model tensor. Shapes and dtypes matched. All per-stage hashes matched and every maximum absolute difference was `0.0`. The actual production model was run on both application and research tensors; outputs matched exactly for all three fixtures. This establishes parity between the current serving and research code only. It does not establish that either reproduces historical training preprocessing.

### Backend path and failure behavior

The Jest integration used a generated harmless PE and exercised upload validation, static analysis, production DCT conversion, the actual checksum-pinned checkpoint, bounded fusion, and API response formatting. The neural response is labeled as an uncalibrated sigmoid score and remains separate from class confidence. Static rules determine the label and the neural score adjusts the numerical score by no more than five points. The uploaded fixture was not executed.

Tests cover missing, empty, corrupt-signature, unsupported-extension, oversized, missing-checkpoint, checksum-mismatch, too-short preprocessing, auth failure and invalid model output paths. Mismatched checkpoint bytes are rejected before model loading and produce no neural score. Simulated outputs are excluded from CNN fusion. The local auth bypass is loopback-only and binds to `127.0.0.1`.

## Validation executed

| Command or check | Result |
| --- | --- |
| `conda run -n threatvision python -m unittest discover -s tests -v` in research repo | **38 passed, 0 failed** |
| Research `python -m compileall -q research tests` | **Passed** |
| Research fresh-weight training CLI `--smoke --cpu` | **Passed**, one train and validation step with temporary synthetic PE-shaped fixtures and pseudo-labels explicitly not ground truth; outputs stayed under `/tmp` |
| Research checkpoint verifier, production profile | **Passed**, six probes |
| Research checkpoint verifier, recovered 256 profile | **Passed**, six probes |
| Research preprocessing parity runner with real model | **Passed**, 3 fixtures × 8 preprocessing stages plus output comparison |
| Backend Python unittest suite | **7 passed, 0 failed** |
| Backend Jest | **2 suites, 11 tests passed** |
| Frontend ESLint | **Passed, no findings** |
| Frontend score helper tests | **3 passed, 0 failed** |
| Public and private Vite builds | **Passed**, generated under `/tmp` |
| `npm audit` | **0 vulnerabilities** |
| `git diff --check` in research, backend, frontend | **Passed** after final report whitespace cleanup |

Conda base uses TensorFlow 2.21.0 and NumPy 2.4.4 but lacks Matplotlib for the evaluation smoke test. Runtime probe scores differed between that TensorFlow version and TensorFlow 2.16.1; cross-runtime numerical equivalence is not claimed. The training smoke used synthetic pseudo-labels only to exercise pipeline wiring; its outputs are not classification evidence and are not included in the repository.

## Website and public repository

The last successful rendered live-site review, on 18 November 2026, found unsupported validation AUC, dataset, architecture, threshold, Grad-CAM, and live telemetry claims. `/demo` returned to the homepage and protected routes redirected to sign-in. On 19 November, a browser follow-up timed out, and the web open tool could not access the host; therefore the prior rendered review remains the last successful live observation. The public GitHub repository was previously confirmed behind this local state. Keep the hosted website out of professor outreach and publish nothing automatically.

The local research tree contains no tracked Keras checkpoints, executable samples, private archives, or environment files. New verification JSON uses sanitized display paths; private absolute model paths and input bytes are not stored. The remote repository was not modified.

## Changed files

New changes in this work are limited to the following areas:

- **Research code/tests:** `research/checkpoint.py`, `research/verify_model.py`, `research/train.py`, new `research/preprocessing_parity.py`, `tests/test_verify_model.py`, `tests/test_train_input.py`, and `tests/test_application_preprocessing_parity.py`.
- **Research evidence/docs:** `README.md`, `REPRODUCIBILITY.md`, `LOCAL_IMPLEMENTATION_REPORT.md`, `docs/audits/FINAL_PROFESSOR_OUTREACH_READINESS.md`, checkpoint and parity reports/JSON, `docs/model-card.md`, `docs/model-architecture.md`, `docs/research-prospectus.md` and its DOCX/PDF, plus the academic claim policy, evidence index, project summary, and one-page summary DOCX/PDF.
- **Backend:** `.env.example`, `python_scripts/classify_image.py`, `python_scripts/tests/test_classify_image_contract.py`, and `tests/classify.test.js`.
- **Frontend:** no additional file edits in this report pass; the pre-existing local changes were validated and preserved.

## Final readiness

**Exploratory outreach: PARTIAL.** The local packet is technically specific and avoids unsupported results. The owner must review and manually publish the research changes, then verify links. Omit the website until a new live browser review shows corrected, accurate content.

**Publishable scientific validation: BLOCKED.** Obtain a lawful, independently labeled PE cohort with traceable sources, duplicate handling, lineage/family grouping, time/source holdouts, and an exact checkpoint-linked evaluation before reporting classification metrics. Preserve the recovered 67.00%, 61.50%, 80.27% validation-log maximum, and ~85% recollection as distinct historical evidence classes; none is a production-checkpoint benchmark.

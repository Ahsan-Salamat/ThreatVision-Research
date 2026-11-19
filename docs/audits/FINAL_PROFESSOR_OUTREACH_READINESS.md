# Final professor outreach readiness

**Audit date:** 19 November 2026

**Scope:** Local research, backend, and frontend checkouts. No commit, push, deployment, or remote modification was performed.

## Verdicts

- **Exploratory professor outreach: PARTIAL.** The local evidence packet now supports an honest discussion of the engineering work and a specific research question. The public research repository remains older than the reviewed files, and the hosted website failed the last rendered accuracy review. Do not include either link until the owner publishes and rechecks the reviewed materials; omit the website from outreach in particular.
- **Publishable scientific validation: BLOCKED.** No lawful, independently labeled PE cohort with verified provenance, immutable lineage-aware splits, and checkpoint-linked predictions is available. Do not claim accuracy, AUC, calibration, threshold quality, or generalization.
- **Local engineering verification: PASS for the checks listed below.** These results establish current code-path behavior, not malware-detection effectiveness.

## Repository state

| Checkout | Branch and HEAD at start | Initial working tree |
| --- | --- | --- |
| `ThreatVision-Research` | `main`, `fc0cb95394cde8231fe4e6c8c2045e68b1adb584` | Clean |
| `ThreatVision Final/backend` | `main`, `9516cc659bb3c9c7c159ac5a96139405f0edc745` | Already contained local edits and generated logs/coverage; preserved |
| `ThreatVision Final/frontend` | `main`, `28f4294f04089207ae0739f8a661a449339474fa` | Already contained extensive local edits; preserved |

All changes remain local and unstaged. No commit, push, deployment, reset, or deletion was performed.

## Evidence and checks

| Area | Result | Evidence and limits |
| --- | --- | --- |
| Production 224×224 checkpoint | **PASS** | SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`; loaded with `compile=False, safe_mode=True`; input `(None,224,224,1)`, output `(None,1)`, 2,422,084 parameters. Six synthetic probes were finite, within the sigmoid range, and repeatable at `1e-7` tolerance (maximum delta 0). Runtime: Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1, NumPy 1.26.4, Apple Silicon CPU/Metal. |
| Recovered 256×256 checkpoint | **PASS, separate artifact** | SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`; safely loaded under its own registered profile. Six probes were finite and repeatable. Its PE-derived engineering input was adapted from the current 224 pipeline and is not historical training parity. |
| Preprocessing compatibility | **PASS for current serving implementation** | Three deterministic harmless fixtures matched across eight stages: byte stream, pair counts, zero-pair suppression, normalization, grayscale quantization, DCT output, resized image, and model input. SHA-256, shape, dtype, and max absolute delta were recorded at each stage. Actual production model outputs also matched exactly between app and research tensors. All maximum deltas were 0.0. Historical training preprocessing remains unknown. |
| Backend end-to-end flow | **PASS for harmless fixture** | Jest exercised upload validation → static PE analysis → production DCT conversion → the checksum-pinned production checkpoint → bounded static-led fusion → HTTP response. The model's raw score is separately exposed as an uncalibrated sigmoid score; simulated scores are excluded. No uploaded binary was executed. |
| Failure and security behavior | **PASS for tested cases** | Missing, empty, corrupt-signature, unsupported-extension, oversized, missing-checkpoint, checksum-mismatch, too-short preprocessing, invalid model output, and auth failure cases are covered. A checksum mismatch is detected before Keras deserialization and yields a clearly simulated response without a neural score. Local auth bypass is loopback-only and forces `127.0.0.1`. |
| Research suite | **PASS** | `python -m unittest discover -s tests -v`: 38 passed, 0 failed in the existing `threatvision` environment. `python -m compileall -q research tests`: passed. |
| Training CLI smoke | **PASS for pipeline wiring only** | One epoch completed using the saved production topology with fresh random weights and temporary PE-shaped byte fixtures. The manifest explicitly marks the benign/malicious values as synthetic pseudo-labels, not ground truth. Output and history were written under `/tmp`; these scores are not research evidence. |
| Backend suite | **PASS** | Backend Python tests: 7 passed. Jest: 2 suites, 11 tests passed, including the real model endpoint and mismatch path. |
| Frontend checks | **PASS locally** | ESLint passed with no findings; score helper tests 3/3; public and private Vite builds passed. `npm audit` reported 0 vulnerabilities. Builds were written to `/tmp`, not deployed. |
| Website and public links | **FAIL for outreach pending re-audit** | The last rendered live-site audit (18 November 2026) observed unsupported AUC, dataset, model, threshold, explanation, and telemetry claims; `/demo` returned to the homepage, and protected routes redirected to sign-in. A 19 November browser follow-up could not be completed because the available browser session timed out and the web open tool could not access the host. Treat the 18 November audit as the last successful rendered check. The public GitHub copy was previously confirmed older than the local review. |

Detailed checkpoint outputs are in [`PRODUCTION_CHECKPOINT_VERIFICATION.md`](PRODUCTION_CHECKPOINT_VERIFICATION.md) and [`production-checkpoint-verification.json`](production-checkpoint-verification.json). Stage-by-stage hashes and neural output comparisons are in [`PRODUCTION_PREPROCESSING_PARITY.md`](PRODUCTION_PREPROCESSING_PARITY.md) and [`production-preprocessing-parity.json`](production-preprocessing-parity.json). Experiment distinctions are in [`MODEL_AND_EXPERIMENT_LINEAGE.md`](MODEL_AND_EXPERIMENT_LINEAGE.md) and [`HISTORICAL_ACCURACY_CLAIM.md`](HISTORICAL_ACCURACY_CLAIM.md).

## Scientific and academic claim consistency

The current application label is static-rule-driven. The neural output contributes at most a five-point advisory adjustment and is not a calibrated probability. Runtime probes, harmless PE fixtures, synthetic scores, the 46-row diagnostic pilot, recovered notebook printouts, the anomalous 22-row log, the separate recovered checkpoint, and the owner-reported approximately 85% recollection remain distinct evidence classes. None supports a verified classification benchmark for the production checkpoint.

The training smoke used disposable PE-shaped fixtures and synthetic pseudo-labels solely to exercise data loading, preprocessing, fresh-weight topology initialization, one train step, validation, and output writing. It exposed and led to a fix for a bytes-conversion error in the `tf.numpy_function` callback. This smoke does not validate labels or measure detection performance, and the script still describes fresh-weight topology reconstruction, not historical training.

The professor-facing Markdown, DOCX, and PDF materials now use the canonical question: **Do frequency-domain neural representations add measurable predictive value beyond conventional PE static features when dataset bias, sample lineage, and generalization are properly controlled?** The one-page summary and prospectus describe the new runtime and parity evidence without assigning it scientific meaning. Both PDFs were regenerated from the updated DOCX files and visually reviewed; page counts remain one page and two pages respectively.

## Public repository safety

The research checkout excludes the production and recovered model weights, raw PE binaries, private datasets, and private application source. The newly generated JSON records contain sanitized checkpoint labels and hashes rather than private absolute model paths. No sensitive source file was published because nothing was pushed. A publication-time scan and review is still required before manual publication.

## Open items

1. Obtain authorized, independently labeled PE data with auditable provenance and lineage-aware splits before evaluating detection performance.
2. Recover the production checkpoint's training and preprocessing lineage; do not assign historical notebook metrics or the ~85% recollection to either checkpoint.
3. Recheck the live website and remote repository after the owner publishes corrected content. The website should remain out of outreach until its claims and routes pass a fresh browser review.
4. Review local diffs and the DOCX/PDF packet before manually publishing any research changes.

**Recommended outreach framing:** present ThreatVision as an independently implemented engineering prototype and proposed evaluation study. Invite feedback on whether frequency-domain neural features add value beyond static PE features under controlled dataset shift and leakage-resistant evaluation. Do not include a benchmark claim or the live website URL.

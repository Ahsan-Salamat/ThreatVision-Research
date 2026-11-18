# Professor outreach readiness — updated 18 November 2026

**Scope:** Reconciliation of owner-supplied original Colab/Drive archives with the research repository snapshot at embedded Git commit `7d3b085`; prepared repository working copy includes local, uncommitted documentation/test changes. **This report is not proof of a remote GitHub push.** Full evidence table: [RECOVERY_CROSSCHECK_2026-11-18.md](RECOVERY_CROSSCHECK_2026-11-18.md).

| Category | Status | What has been verified | What still blocks stronger claims |
| --- | --- | --- | --- |
| Archive/inventory recovery | **PASS, static integrity only** | Two outer ZIP CRCs, nested Keras CRC, SHA-256 hashes, notebook structure, manifest/log counts. Earlier 256×256 model configuration intact. | TensorFlow runtime, exact training history, label accuracy, notebook-to-weights lineage. |
| Internal research consistency | **PASS with explicitly unresolved evidence** | The README, model card, methods, dataset notes, prospectus and outreach documents now distinguish the 4,000-row manifest, 79,997-folder-image record, 46-row diagnostic pilot, and two distinct model descriptions. | It is not possible to make all historical experiments and model artifacts one proven training lineage. |
| Engineering reproducibility | **PARTIAL** | 21 safe Python unit tests passed independently (14 prior + seven new synthetic audit tests); artifact auditor runs without TensorFlow; original provenance sidecar checks remain in the evaluator. | Training, inference, the private production static analyzer and a real model/data end-to-end run remain unverified. |
| Scientific malware detection evidence | **BLOCKED / NOT ESTABLISHED** | Historical outputs, the pilot and manifest are properly labeled and separately discussed. | No authorized, independently verified PE corpus with immutable, leakage-resistant partitions and runnable checkpoint inference. Split-integrity risk in later notebook. |
| Public demo | **BLOCKED / UNVERIFIED** | Local read-only screenshot exists in the research repository. | No independent current browser test of public pages/results; avoid linking to the demo as proof of live inference. |
| **Exploratory professor outreach** | **READY AFTER PUBLICATION AND PERSONALIZATION** | Evidence-backed one-page summary, research prospectus, annotated evidence index, accurate limitations, and tailored-email template prepared. | Must verify updated GitHub revision is public, attach truthful CV and personalize to an actual paper/professor. This does **not** imply eligibility, admission or funding. |

## Verification record

On 18 November 2026, `python -m unittest discover -s tests -v` produced **14 PASS** results: the original 11 synthetic/validation tests plus three read-only recovery-auditor tests. `python -m compileall` and document link checks should be rerun after publishing. The two Drive ZIPs, their SHA-256 and the nested Keras archive were verified by read-only code; **no notebook, weights, or potentially malicious samples were executed**. Original raw image/PE dataset and deployed 224×224 checkpoint bytes were absent from the reviewed uploads. The separate 256×256 model is structurally intact but **not runtime-verified**.

## Historical anomalies and honest limits

- `training_log.csv`: 22 records, two epoch sequences (13+9), `val_auc=0.0` and `val_precision=1.0` in every row. The underlying validation split and checkpoint association remain unknown.
- `ThreatVisionFInal.ipynb`: 39,999 benign + 39,998 malicious image-folder entries; saved output begins a training attempt but does not show completed training. Training and validation loaders use different shuffle settings with `validation_split`, which creates a plausible overlap risk.
- `ThreatVision.ipynb`: saved output records a 4,000-image (2,000/2,000) subset and historical 67.00% scratch-CNN / 61.50% MobileNetV2 test printouts. Without underlying images, PE labels and actual saved models, these are *not independently validated benchmark results*.
- The recovered 256×256 `best_model.keras` and documented 224×224 `threatvision_v01.keras` have different SHA-256, Keras versions, input sizes and serialized layer order; do not merge them.

## New historical accuracy claim and verification infrastructure

The developer recalls a best MobileNetV2 result of approximately **85% accuracy**. Neither the recovered historical notebook exports nor the 22-row training log supports this number; the latter has a maximum `val_accuracy` of **80.27%** but anomalous AUC. Consequently the 85% is recorded in [the historical claim register](HISTORICAL_ACCURACY_CLAIM.md) as **unverified**, rather than inserted into the professor materials. A separate reconstructed verification notebook and a strict per-sample prediction-audit utility were added; no prediction rows or model outputs were fabricated. The updated local safe test suite passed **21 tests** (14 prior + 7 synthetic claim-audit tests). These are engineering checks only.

## What to do before sending

1. Review the [reconciliation](RECOVERY_CROSSCHECK_2026-11-18.md) and [claim policy](../../academic-outreach/CLAIM_POLICY.md) for accuracy and rights to publish.
2. Commit and push the **prepared** files, and verify links from an incognito browser. Nothing in this ZIP was pushed by this audit.
3. Send only [the one-page project summary](../../academic-outreach/PROJECT_SUMMARY.md) or [research prospectus](../research-prospectus.md) and a tailored [email](../../academic-outreach/PROFESSOR_EMAIL_TEMPLATE.md); omit live demo and historical accuracy claims.
4. To upgrade from an exploratory conversation to reproducible experimental claims, recover authorized PE/PNG data and exact split membership, load each model in a compatible isolated environment, test inference and run pre-registered baselines.

**Decision:** Suitable for **limited, personalized academic introduction** after local publication checks; **not** ready to represent independently validated malware detection, a reconstructed historical training run, or a verified public inference demonstration.

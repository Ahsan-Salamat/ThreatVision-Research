# Final professor outreach readiness

**Audit date:** 18 November 2026  
**Scope:** local research checkout and companion application; no remote publication or deployment performed.

## Verdict

**PARTIAL — technically credible as an undergraduate engineering prototype and proposed study after the owner publishes the reviewed local research changes. Do not include the live site URL.** The evidence does not support a validated malware classifier, a reproducible historical training run, or a performance claim. The public GitHub page is reachable, but it has not been updated with this uncommitted checkout. The live website is reachable but fails the academic accuracy review because it presents unsupported architecture, dataset, benchmark, threshold, and telemetry claims.

## Readiness by area

| Area | Status | Evidence |
| --- | --- | --- |
| Production checkpoint identity and safe execution | **PASS** | The original 224×224 artifact matches SHA-256 `1e8f713d…f6aaca`; safe load and five synthetic forward passes succeeded; outputs were finite, shaped `(1,1)`, bounded `[0,1]`, and repeatable. |
| Separate recovered checkpoint | **PASS, runtime only** | The distinct 256×256 `best_model.keras` hash `62feb539…73102` loaded and passed synthetic probes under its own `[0,255]` input profile. No experiment lineage or accuracy is thereby established. |
| Production preprocessing compatibility | **PASS for implementation parity** | App and research transforms matched exactly for three deterministic synthetic fixtures (max absolute tensor delta 0). Historical training parity remains unknown. |
| Local application path | **PASS for safe smoke** | HTTP and Node tests exercised upload validation, static analysis, DCT conversion, the actual production checkpoint, and fusion with a harmless generated PE. `confidence` is predicted-class confidence; `neuralScore` is the separate raw uncalibrated malware sigmoid output. Missing scores remain unavailable. Missing auth configuration fails closed except with an explicit development/test-only local bypass; production ignores the bypass. The bypass now accepts loopback clients only and forces the listener to `127.0.0.1`. Simulated fallback scores and indicators are excluded from the API neural-score field, UI neural-score display, fusion evidence, and saved scan history. |
| Automated engineering checks | **PASS with tooling caveat** | Fresh research suite: 35/35; backend Python: 6/6; backend Jest: 10/10, including real production-model integration, raw-score response checks, and loopback-only bypass checks; frontend score-helper regression tests: 3/3. Public and private Vite builds passed. Headless Chrome rendered both local builds at 390px; the public build showed the inference-unavailable notice and disabled-upload disclosure, document width equaled the viewport, and no resource returned an error. Backend integration used Python 3.11.15 / TensorFlow 2.16.1, which differs from `requirements.txt`'s TensorFlow 2.19.0 pin. One preceding verbose full Jest run reported `write EPIPE`; the final full suite passed. The base Conda environment's research suite has one error because Matplotlib is absent. Repository-wide frontend lint fails on existing lint debt and generated `dist-private` bundles. |
| Scientific malware performance | **BLOCKED / UNVERIFIED** | No authorized, independently labeled PE cohort with immutable lineage-aware partitions is available. No accuracy, ROC-AUC, recall, FPR, calibration, or operating threshold is supported. |
| Historical 85% claim | **OWNER-REPORTED / UNVERIFIED** | The reviewed archives do not support the recollection. It is not attributed to either checkpoint. |
| Public website | **FAIL for outreach** | Chrome rendered the live homepage with no JS console errors or failed asset requests, but it displays unsupported “0.970 Validation AUC,” 1.04M MaleX, SE-ResNet, calibrated cutoff, Grad-CAM, and live threat telemetry claims. `/demo` returns to the homepage; protected routes redirect to `/auth`. Mobile viewport has overflowing telemetry content. Do not link this site until owner publishes corrected content and it is re-audited. |
| Research repository link | **PARTIAL** | GitHub repository and raw README return HTTP 200. The remote copy remains older than the reviewed local changes, which are intentionally uncommitted and unpublished. |
| Local documentation and outreach packet | **PASS locally** | Research question, evidence index, limitations, summary, prospectus, and lineage notes distinguish verified runtime checks from historical outputs and unknowns. Changes are local and uncommitted; remote links still need owner verification after publication. |

## Recommended outreach framing

Present ThreatVision as a completed undergraduate engineering project with a verified local inference path and an open research question: **Do frequency-domain neural representations add measurable predictive value beyond conventional PE static features when dataset bias, sample lineage, and generalization are properly controlled?** Invite feedback on study design and threat validity. Do not advertise a benchmark result, a calibrated probability, live public scanning, or a verified Grad-CAM explanation.

## Before sending

1. Review the local changes and manually publish them through the owner's normal process.
2. Manually publish the reviewed local repository changes, then verify the remote README and prospectus. Exclude the public demo URL until its deployed content matches the evidence.
3. Personalize the email to a professor's work and attach only the reviewed one-page summary or prospectus.

Before any backend deployment, configure and verify the Supabase token verifier and keep `ALLOW_UNAUTHENTICATED_LOCAL` disabled in deploy environments.

Detailed records: [checkpoint verification](PRODUCTION_CHECKPOINT_VERIFICATION.md), [lineage register](MODEL_AND_EXPERIMENT_LINEAGE.md), [recovery crosscheck](RECOVERY_CROSSCHECK_2026-11-18.md), and [historical accuracy audit](HISTORICAL_ACCURACY_CLAIM.md).

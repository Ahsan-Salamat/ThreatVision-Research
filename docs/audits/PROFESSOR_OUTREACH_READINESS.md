# Professor outreach readiness — 18 November 2026

| Category | Decision | Evidence |
| --- | --- | --- |
| Experimental evidence | PARTIAL | Manifest validation and static/neural/combined comparison infrastructure exist. The original diagnostic cohort lacks independently verified malicious examples. No new detection results were generated. |
| Reproducibility | PARTIAL | Runnable source, safe tests and CI were added. Historical training code, training partitions and checkpoint lineage remain unavailable. Eleven tests passed in a clean virtual environment, including the latest provenance checks and bootstrap interval test. TensorFlow installation was attempted but its 200 MB wheel repeatedly timed out. Checkpoint runtime loading and inference remain unverified. |
| Demonstration | BLOCKED | A fresh web-tool request could not access the public demo; curl subsequently returned HTTP 200 from Netlify. Rendered behavior remains unverified. The sibling frontend has a local walkthrough, previously tested on 14 November. This pass is limited to the research directory and does not establish current production functionality. |
| Professor outreach | PARTIAL | The repository has a defensible research question, inspectable initial tooling, scientific limitations and linked prospectus. Public demonstration and complete experiment reproduction remain unresolved. |

Overall, NOT READY for outreach claiming a verified public demonstration or reproducible detection performance. The repository can support a discussion of undergraduate implementation and a proposed MSc evaluation, with these limitations explicit.

## Verification record

On 18 November 2026, the isolated Python 3.13 environment with research dependencies ran 11 tests successfully in 4.211 seconds. Checks cover synthetic metric output, sidecar mismatch and missing-preprocessing-hash rejection, Git-free revision fallback, source and temporal split logic, deterministic bootstrap intervals, manifest leakage checks, and numerical preprocessing. Three synthetic inputs matched production preprocessing. TensorFlow 2.20 installation did not finish because the 200 MB wheel timed out, so checkpoint inference and training were not run. Compileall and git diff --check passed. Tests use synthetic bytes, headers and invented feature scores only. No executable samples were run.

## Remaining implementation and evidence

- Supply independently labeled benign and malicious PE cohorts with authorized access and trustworthy lineage, family and source metadata.
- Recover or document original training provenance. Verify checkpoint loading, stochastic augmentation behavior and repeated inference under a compatible TensorFlow environment.
- Run the new extractor and training paths in a compatible TensorFlow environment. The model artifact is outside the research repository.
- Run end-to-end extraction and training with the owner-held checkpoint and authorized samples. Current tests do not execute TensorFlow or the production static analyzer integration.
- Validate the current public demonstration through browser testing, including results and unavailable-service states. Owner approval is required before publishing local changes.
- Read the [baseline audit](baseline-audit.md) for source evidence, and [reproduction commands](../../REPRODUCIBILITY.md) for the current tooling.

No commits, pushes, deployments or research uploads were performed.

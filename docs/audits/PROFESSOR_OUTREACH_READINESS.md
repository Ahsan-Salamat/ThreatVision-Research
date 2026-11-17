# Professor outreach readiness — 17 November 2026

| Category | Decision | Evidence |
| --- | --- | --- |
| Experimental evidence | PARTIAL | Manifest validation and static/neural/combined comparison infrastructure exist. The original diagnostic cohort lacks independently verified malicious examples. No new detection results were generated. |
| Reproducibility | PARTIAL | Runnable source, safe tests and CI were added. Historical training code, training partitions and checkpoint lineage remain unavailable. Seven safe tests passed in a clean virtual environment. The runtime probe still needs TensorFlow and successful checkpoint loading. |
| Demonstration | BLOCKED | A fresh web-tool request could not access the public demo; curl subsequently returned HTTP 200 from Netlify. Rendered behavior remains unverified. The sibling frontend has a local walkthrough, previously tested on 14 November. This pass is limited to the research directory and does not establish current production functionality. |
| Professor outreach | PARTIAL | The repository has a defensible research question, inspectable initial tooling, scientific limitations and linked prospectus. Public demonstration and complete experiment reproduction remain unresolved. |

Overall, NOT READY for outreach claiming a verified public demonstration or reproducible detection performance. The repository can support a discussion of undergraduate implementation and a proposed MSc evaluation, with these limitations explicit.

## Verification record

The original system Python run passed two manifest tests and failed two numerical tests because NumPy was unavailable. The fresh virtual environment installed all declared dependencies successfully. All seven tests then passed, including the synthetic evaluation smoke test, leakage rejections, and numerical transformations (167.282 seconds including first-import/font-cache overhead). Three additional synthetic inputs matched the original application preprocessing exactly. Python compilation and git whitespace checks passed. Tests use synthetic bytes and headers only. No executable samples were run.

## Remaining implementation and evidence

- Supply independently labeled benign and malicious PE cohorts with authorized access and trustworthy lineage, family and source metadata.
- Recover or document original training provenance. Verify checkpoint loading, stochastic augmentation behavior and repeated inference under a compatible TensorFlow environment.
- Complete feature extraction and provenance binding, temporal/source holdouts, uncertainty estimates, full evaluator regression tests and training implementation. The current runner cannot establish those safeguards by itself.
- Complete per-stage preprocessing regression and production parity tests. The numerical functions were extracted from the source but production has not been switched to import the research module.
- Validate the current public demonstration through browser testing, including results and unavailable-service states. Owner approval is required before publishing local changes.
- Read the [baseline audit](baseline-audit.md) for source evidence, and [reproduction commands](../../REPRODUCIBILITY.md) for the current tooling.

No commits, pushes, deployments or research uploads were performed.

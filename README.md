# ThreatVision

### Malware Triage with Static Analysis and Frequency-Domain Neural Features

**Ahsan Ali Salamat** · Software Engineering Final Year Project · The University of Faisalabad · Post-submission technical investigation

I independently designed and implemented ThreatVision's technical architecture, software, and integrations. The university records the original FYP as a group submission by Ahsan Ali Salamat and Usman Manzoor; this formal record is distinct from technical authorship.

ThreatVision combines static PE analysis with a byte-bigram/DCT image path and a MobileNetV2 neural score. The transform follows prior work by Mohammed et al. (2021); the project contribution is the system implementation and integration. Static criteria determine the final malware/benign label. Neural inference can adjust the numeric threat score by at most five points.

**Research question:** Does the byte-bigram/DCT neural representation provide incremental malware-classification information beyond simple file statistics and static PE features? The evidence below is a limited diagnostic pilot, not a malware-detection benchmark.

## Project Demonstration

The [project landing page](https://threatvision.amaaholding.com/) currently serves the earlier website. The [original analyst dashboard](https://threatvision.amaaholding.com/dashboard) redirects signed-out visitors to sign-in. A separate read-only demonstration is prepared locally and awaits publication. Live inference is unavailable in the demonstration. The Render service responded to a liveness check during the audit, and end-to-end inference remains unverified.

![System overview showing upload validation branching into static PE analysis and byte-bigram/DCT neural inference, then recombining in a static-led decision and analyst report.](figures/system-overview.svg)

*Figure 1. ThreatVision system overview. The branches show distinct evidence paths and do not imply concurrent execution. Static criteria determine the final label; the neural score has bounded influence on the numeric risk score.*

![Browser screenshot of the ThreatVision read-only analyst dashboard with an inference-unavailable notice and links to static PE evidence and the experimental record.](figures/analyst-dashboard.png)

*Screenshot of the implemented read-only walkthrough running locally. The public site still serves the earlier frontend.*

## How bytes become model input

The implemented representation counts adjacent byte pairs, suppresses the `(0,0)` cell, normalizes and quantizes the matrix, applies an orthonormal 2D DCT-II, compresses coefficient magnitudes, and resizes the result. The transform is based on [published frequency-domain work](docs/references.md), not a newly proposed representation.

![Nine-step preprocessing diagram using the clearly synthetic byte sequence 4D 5A 90 00 00 00 90 5A 4D. It shows overlapping pair counts, a four-by-four slice of the 256 by 256 matrix, suppression of the null pair, quantization, DCT-II, log magnitude, resizing, and model input.](figures/preprocessing-explained.svg)

*Figure 2. Synthetic teaching example only. The sequence, matrix slice, and schematic frequency plane are illustrative; no observed file, feature map, or model output is shown. See the [methodology](docs/methodology.md) for the complete transformation.*

## Diagnostic observation

The supplied pilot CSV contains 46 artifacts: ten rows labeled benign PE, twenty transformations derived from two PEs, and sixteen synthetic or out-of-domain probes. The chart shows the two source-dependent responses to selected random-byte overlays, with each original file as the zero-overlay baseline. Nine of the ten benign-labeled PE rows had a neural score below 0.50.

![Line chart of recorded neural sigmoid scores against appended random-byte overlay size from zero to 200 KiB for windows-kill and cli-64. The windows-kill score rises slightly then falls; the cli-64 score rises across the tested sizes.](figures/diagnostic-response.svg)

*Figure 3. Neural scores for two selected files labeled benign PE in the supplied CSV and their four overlay derivatives. Scores are sigmoid outputs, not calibrated malware probabilities. The interventions change size and byte representation together; they do not isolate entropy. Rows are paired by source and are not independent experimental units.*

## Recovery and provenance update (18 November 2026)

Two original Google Drive exports were recovered and inspected read-only. They contain **eight Colab notebooks**, a structurally intact **earlier 256 × 256 × 1 MobileNetV2 checkpoint** (`best_model.keras`; SHA-256 prefix `62feb539`), a **22-row training log with anomalous validation metrics**, and a **4,000-row balanced image manifest** (2,000 of each label). The `ThreatVision.ipynb` saved outputs report separate, historical **67.00% scratch-CNN** and **61.50% MobileNetV2** test-accuracy printouts on a 4,000-image workflow. These are **unreproduced notebook printouts**, not validated metrics of the deployed checkpoint. The original images and PE files were **not supplied** with the exports.

A later `ThreatVisionFInal.ipynb` output records **39,999 benign plus 39,998 malware image-folder entries**, but only shows the **start** of a 256 × 256 training run. Its train/validation directory-loader calls use incompatible shuffling settings, creating a potential split-overlap risk. No complete, independently verified final training history can be claimed from it. Another recovered notebook concerns separate family-classification experiments; third-party reference notebooks are not counted as original project performance.

**Model versions must stay distinct:** the recovered 256 × 256 checkpoint is **not the documented 224 × 224 production checkpoint** (`threatvision_v01.keras`), and its Conv2D-to-Rescaling layer order differs from the later notebook's implementation. The earlier model passed ZIP integrity checks but was not loaded in TensorFlow. The 224 × 224 checkpoint metadata is in this repo, but its original model bytes were not supplied in the recovery exports. Detailed source-by-source findings: [recovery reconciliation](docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md) and [sanitized verification summary](docs/audits/recovered-artifact-verified-summary.json).

**Historical best-accuracy recollection (unverified):** The developer recalls approximately **85%** in a MobileNetV2 experiment, but **none of the supplied notebook outputs or logs establishes that number**, and the relevant split, checkpoint and data provenance are unknown. The highest saved `val_accuracy` in the 22-row CSV is **80.27%**; it has anomalous `val_auc=0.0` for all rows and is not independent test evidence. The 85% figure is **not a validated result** and is excluded from professor outreach performance claims. See the [85% claim audit](docs/audits/HISTORICAL_ACCURACY_CLAIM.md) and [reconstructed verification notebook](notebooks/RECONSTRUCTED_MobileNetV2_Validation.ipynb).

The only **independently executed** checks in this research repo are safe engineering tests; no genuine, independently labeled malware benchmark is claimed.

## What the evidence supports

| Established in this record | Observed in the pilot | Still unproven |
| --- | --- | --- |
| Static criteria determine the final label; the neural score has a bounded numeric adjustment. | Score responses to overlays differed across two source files; three of eight overlay rows received a final malware label. | Malware-detection performance, calibrated probabilities, a general entropy shortcut, or an entropy-only causal effect. |
| The deployed archive records a MobileNetV2-based architecture and saved compile configuration. | Two histogram-preserving byte shuffles retained size and recorded entropy while scores fell. | Training-data identity, independent label validity, and the checkpoint's full lineage. |
| The public repository documents the implementation and a small post-submission study. | Synthetic random streams received high neural scores in this set. | Generalization to a lawful, independently labeled malware corpus. |

The pilot has no known-malicious PE cohort or independently verified labels. Twenty transformed observations derive from two files, so the 46 rows are not 46 independent experimental units. The sample-level CSV, original input files, and runnable experiment are not published; rights and provenance remain unresolved. See the [experimental record](docs/experimental-record.md) and [findings and limitations](docs/findings-and-limitations.md).

## Proposed research

The first proposed experiment compares regularized logistic regression using pre-specified file statistics and static PE features with the same model plus the frozen neural score. It requires lawful raw PE files and independently documented labels, duplicate- and source-aware chronological splits, train-only scaling, validation-based model selection, and a pre-specified test metric and practical margin. If the neural score adds no practically meaningful held-out information, the incremental-value hypothesis is not supported. This experiment has not been run.

![Proposed research roadmap from recovering provenance through simple baselines, controlled perturbations, representation comparisons, and shared-split system evaluation, with dataset reconstruction considered only if existing data are insufficient.](figures/research-roadmap.svg)

*Figure 4. Proposed work only; none of these experiments is presented as completed.* See the detailed [future research plan](docs/future-research.md).

## Documentation

| Area | Documents |
| --- | --- |
| Research background and methodology | [Background](docs/research-background.md) · [Methodology](docs/methodology.md) · [Dataset provenance](docs/dataset-provenance.md) |
| Implemented architecture | [System architecture](docs/system-architecture.md) · [Model architecture](docs/model-architecture.md) · [Model card](docs/model-card.md) |
| Experimental evidence and limitations | [Experimental record](docs/experimental-record.md) · [Findings and limitations](docs/findings-and-limitations.md) |
| Post-submission investigation | [Investigation account](docs/post-submission-investigation.md) |
| Future research and prospectus | [Future research](docs/future-research.md) · [Prospectus (Markdown)](docs/research-prospectus.md) · [Prospectus (DOCX)](docs/research-prospectus.docx) |
| References and citation | [References](docs/references.md) · [BibTeX](references.bib) · [CITATION.cff](CITATION.cff) |

## Academic outreach materials

For professors, start with the [one-page research summary (PDF)](academic-outreach/ThreatVision_One_Page_Research_Summary.pdf), [two-page prospectus (PDF)](docs/research-prospectus.pdf), and [academic evidence index](academic-outreach/EVIDENCE_INDEX.md). The [ready-to-personalize email](academic-outreach/PROFESSOR_EMAIL_TEMPLATE.md) deliberately does not claim validated malware performance or a working public inference demo. The [claim policy](academic-outreach/CLAIM_POLICY.md) lists safe descriptions and forbidden unsupported claims. Admission, funding, and supervision must be assessed through each institution's formal process.

## Authorship and availability

I independently implemented ThreatVision's technical system. The original FYP's formal university record remains a group submission, as described above. This repository includes research documentation and initial evaluation tooling; it excludes application source, model weights, input binaries, training data, and the sample-level measurements pending provenance and rights review. No repository reuse license has been selected. Citation metadata is provided in [CITATION.cff](CITATION.cff).

## Reproducibility tooling

See [setup and safe tests](REPRODUCIBILITY.md) and the [current readiness assessment](docs/audits/PROFESSOR_OUTREACH_READINESS.md). Research infrastructure passes fourteen safe tests, including three additional archive-metadata audit checks. No new detection results are reported. Recovered original notebooks, model metadata and training-log cautions are summarized in the [artifact inventory](docs/audits/recovered-artifact-inventory.md) and [source-by-source reconciliation](docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md). Feature evaluation requires a matching extraction provenance sidecar.

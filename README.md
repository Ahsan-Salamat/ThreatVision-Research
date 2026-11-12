# ThreatVision: Malware Triage with Static Analysis and Frequency-Domain Features

I independently designed and developed ThreatVision's technical architecture, software, and integrations for my Software Engineering Final Year Project at The University of Faisalabad. I continued investigating the system after submission. University records list the formal FYP as a group submission by Ahsan Ali Salamat and Usman Manzoor; the record of group submission is separate from technical authorship.

ThreatVision combines PE static analysis with a byte-bigram/DCT image path and a MobileNetV2 neural score. Static criteria determine the final malware/benign label; neural inference can adjust the numeric threat score by at most five points. The byte-bigram/DCT representation follows prior work by Mohammed et al. (2021), rather than a new algorithm. Family labels are rule-based profiles, and the interface heatmap is a CSS illustration rather than a gradient-derived explanation.

## Post-submission diagnostic pilot

The supplied measurement table contains 46 input artifacts, including 10 rows labeled benign PE, 20 transformations of two PE files, and synthetic or out-of-domain probes. Among the 10 PE rows, nine neural scores were below 0.50. When random-byte overlays were appended, the score rose from 0.4600 to 0.9990 across the four `cli-64` variants, but the `windows-kill` score peaked at 0.2534 and then fell to 0.1476. Three of the eight overlay rows received a final malware label. These paired probes show source-dependent responses to the combined changes in size and byte representation; they do not isolate entropy or establish detection performance.

There were no known-malicious PE examples or independently verified test labels in this pilot. The rows are clustered: 20 transformations derive from two files. The results are descriptive, not a malware-detection benchmark. Details and limitations are in the [experimental record](docs/experimental-record.md).

## What remains unknown

The checkpoint archive identifies a MobileNetV2 model saved with Keras 3.14.1 and records Adam at `5 × 10⁻⁶`, binary cross-entropy, and accuracy/AUC/precision/recall metrics. These saved settings do not recover the training history or dataset. The reported relationship between the deployed checkpoint and a historical `phase2_best.keras` file is not independently established. No local accuracy, ROC-AUC, precision, recall, F1, calibrated operating point, or false-positive rate is claimed. The experiment code, source binaries, and sample-level CSV are not included; measurement redistribution terms still need confirmation.

## Research question

Does the byte-bigram/DCT neural representation provide incremental malware-classification information beyond simple file statistics and static PE features? The [next baseline experiment](docs/future-research.md#first-baseline-experiment) compares the same statistical and PE features with and without the frozen neural score.

## Engineering, investigation, and proposed research

- **Engineering:** I implemented and integrated the static-analysis pipeline, byte-bigram/DCT preprocessing, neural inference, bounded score adjustment, API integrations, and analyst-facing application.
- **Experimental investigation:** The post-submission pilot measured responses to selected benign PE, transformed, synthetic, and out-of-domain inputs. Its results are limited to those artifacts.
- **Proposed research:** Test whether the frequency representation adds classification information beyond simpler file statistics and static features, using controlled data, shared partitions, and explicit uncertainty estimates.

## Documentation

- [Research background](docs/research-background.md)
- [Methodology](docs/methodology.md)
- [System architecture](docs/system-architecture.md)
- [Experimental record](docs/experimental-record.md)
- [Findings and limitations](docs/findings-and-limitations.md)
- [Post-submission investigation](docs/post-submission-investigation.md)
- [Future research](docs/future-research.md)
- [Dataset provenance](docs/dataset-provenance.md)
- [Model architecture](docs/model-architecture.md) and [model card](docs/model-card.md)
- [Figures](docs/figures.md)
- [Research prospectus](docs/research-prospectus.md) ([DOCX](docs/research-prospectus.docx))
- [References](docs/references.md) and [BibTeX](references.bib)

## Citation and availability

The root [CITATION.cff](CITATION.cff) names Ahsan Ali Salamat as technical author. The formal group-submission record is described above. This public repository contains documentation only; it excludes application source, model weights, input binaries, training data, and the sample-level measurements pending rights review. No reuse license has been selected.

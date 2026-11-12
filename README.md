# ThreatVision: Malware Triage with Static Analysis and Frequency-Domain Features

ThreatVision asks whether frequency-domain features can support pre-execution malware triage without mistaking entropy, packing, or dataset artifacts for evidence of malicious behavior. We built it as a collaborative undergraduate Software Engineering Final Year Project at The University of Faisalabad. The deployed application combines PE static analysis with a byte-bigram/DCT image path and a MobileNetV2-based CNN score; static rules determine the final malware/benign label, and the CNN can change the numeric score by at most five points.

After submission, I tested selected inputs to understand the model's behavior. Random bytes and a compressed PDF received high neural scores, while a structured text PDF and a constant-byte stream received low scores. These PDFs and random bytes are outside the model's intended Windows PE domain. The score differences raise questions about entropy and other confounding signals but do not demonstrate shortcut learning or establish a false-positive rate. The local training distribution, training history, and independent evaluation are unavailable. I considered a controlled dataset and stronger evaluation as possible next steps, but neither has been carried out or validated. I am concluding this phase because the data access, curation, compute, and time those experiments require are not presently available. A controlled study could establish whether the frequency representation adds useful evidence beyond these confounds.

## What the system does

The application converts adjacent byte-pair counts into a 256 × 256 matrix, suppresses the `(0,0)` count, normalizes and quantizes the matrix, applies a two-dimensional DCT-II, compresses coefficient magnitudes, and resamples the result to a single-channel 224 × 224 input. A MobileNetV2-based model returns a scalar score. In a separate path, static analysis extracts PE structure and selected file indicators. A heuristic scorer combines static evidence and a small CNN score adjustment, while static criteria control the final binary label.

The byte-bigram/DCT representation follows prior work by Mohammed et al. (2021), cited in [References](docs/references.md). ThreatVision integrates a related method; it does not claim to originate it. The CNN is advisory, not an independently validated malware detector. The user-interface heatmap is a CSS illustration, and family labels are heuristic profiles rather than learned predictions.

## Evidence and limits

The available evidence supports a description of the deployed MobileNetV2-based artifact and selected input probes. It does not include an independently documented training corpus, training history, prediction-level holdout results, or external evaluation. No accuracy, ROC-AUC, precision, recall, F1, false-positive rate, or calibrated operating point is claimed for the local checkpoint. Published MaleX results belong to the cited study and are not ThreatVision measurements.

The diagnostic PDFs and random-byte streams are outside the model's intended Windows PE domain. Their scores show only how the model responded to those selected inputs. A high score on an out-of-domain probe is not a false positive in the statistical sense. The cause of the observed score differences remains uncertain; shortcut learning is one hypothesis to test, not an established finding.

## Project history and authorship

ThreatVision began as a collaborative undergraduate Final Year Project by Ahsan Ali Salamat and Usman Manzoor. After submission, I continued investigating model behavior and possible evaluation improvements. This later account uses “I” for that investigation and “we” for the original collaborative project. Individual authorship and timing for every post-submission code change are not established, so none are assigned here. The acknowledgements and supervisor's preferred public name remain subject to author confirmation. The repository does not imply university endorsement.

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

## Citation

The root [CITATION.cff](CITATION.cff) identifies the two original project authors and links to this public repository. There is no DOI or versioned release. The CFF authorship reflects the collaborative project; it does not assign authorship for each later documentation change.

## Availability and reuse

This is a public, documentation-only repository about the ThreatVision undergraduate project. It contains project documentation and illustrative feature images; it does not include application source code, model weights, malware binaries, or the local training data. The method is described for research discussion and is not accompanied by the artifacts needed to reproduce training or independent evaluation. No reuse license has been selected. Permission to redistribute the two feature images has not been confirmed, and there is no claim of peer review, external validation, or reproducibility from the public materials.

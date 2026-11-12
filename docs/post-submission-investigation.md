# Post-Submission Investigation

I independently designed and developed ThreatVision's technical architecture, implementation, and integrations for my Software Engineering Final Year Project at The University of Faisalabad. University records list the formal FYP as a group submission by Ahsan Ali Salamat and Usman Manzoor. Private backend and frontend Git histories contain 11 and 13 commits, respectively, attributed to Ahsan. Those histories support my account of technical authorship; they do not prove that no unrecorded contribution occurred.

After the academic submission, I continued investigating how the deployed neural model responded to selected byte inputs. The available CSV records a pilot with 46 input artifacts. Ten rows are labeled benign PE; 20 are transformations of two PEs; the remainder are synthetic or out-of-domain probes. The CSV's names, labels, and PE status lack independent source records, and the transformed rows are dependent observations.

## What I measured

The 10 rows labeled benign PE had a mean neural score of 0.2166 (sample SD 0.1707); nine scores were below 0.50. In two histogram-preserving shuffles, file size and Shannon entropy remained the same as their source rows, while the neural scores changed from 0.201538 to 0.041138 and from 0.459961 to 0.055603. This indicates sensitivity to byte ordering in these two cases, not evidence that the model represents malware semantics.

Appending random-byte overlays produced different score trajectories for the two source PEs. The `cli-64` score rose from 0.459961 to 0.999023 across four overlays. For `windows-kill`, it rose from 0.201538 to 0.253418 and then fell to 0.147583. Three of the eight overlay rows received a final malware label. Each transformation changes several byte-level properties, so the observations do not show that entropy alone caused the score changes. The static rules did not neutralize every high-score overlay.

The eight synthetic random-stream rows scored between 0.996582 and 0.999512, across sizes from 5 KiB to 1 MiB. The null-padding and repeated-content rows changed file size and/or entropy while producing little or no score change. These are useful diagnostic observations, but the data do not establish a size-only effect: the noise inputs are not documented as nested or paired streams, and the rows are not independent. The pooled size correlation is descriptive and does not disprove file-size confounding.

## What the system decides

In the implementation, static-analysis conditions determine the final binary label. Neural inference contributes a bounded adjustment of at most five points to the numeric threat score. In the pilot, all 10 rows labeled benign PE and all eight synthetic random streams received benign final labels, while three overlay variants and one synthetic `MZ`-plus-random input received malware labels. This selected set cannot establish reliability or accuracy for either component. The static weights and thresholds have not been calibrated on an independently labeled corpus.

## What remains open

The checkpoint archive identifies a MobileNetV2-based model and records Keras 3.14.1 and a save time of 2026-05-15. Its top-level compile configuration records Adam near `5 × 10⁻⁶`, binary cross-entropy, and accuracy, ROC AUC, precision, and recall. These settings do not establish training data or history. A debug script references `phase2_best.keras`, but that file is unavailable and no provenance record establishes it as the source of the deployed checkpoint. Training data, split membership, epoch history, and model-selection records remain unavailable.

The pilot has no known-malicious PE cohort, verified labels, repeated independent samples, or balanced evaluation split. It cannot support detection metrics or a population false-positive estimate. The experiment code and input files were not included in the remediation package, so the measurements cannot currently be reproduced from the public repository. The sample-level CSV remains private pending confirmation of redistribution terms.

I am concluding this development phase because further comprehensive investigation requires recoverable provenance, a controlled labeled dataset, a reproducible experiment program, and additional computational resources. This does not mean no further work can be done on existing hardware. The concrete next study is to test whether the current frequency-domain representation adds information beyond simple statistics and PE static features under a shared, leakage-resistant evaluation. See [Future research](future-research.md).

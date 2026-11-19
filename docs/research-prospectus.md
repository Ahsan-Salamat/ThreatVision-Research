# ThreatVision Research Prospectus

**Technical author:** Ahsan Ali Salamat, The University of Faisalabad

**Formal FYP record:** Group submission by Ahsan Ali Salamat and Usman Manzoor

### Engineering contribution

I independently designed and implemented ThreatVision's software architecture, integrations, and technical system for my Software Engineering final-year project. The application combines PE static analysis, byte-bigram/DCT preprocessing, MobileNetV2 inference, bounded score fusion, and an analyst-facing web interface. Private backend and frontend histories contain 11 and 13 commits attributed to me. These records support my account of technical authorship; they cannot rule out unrecorded contributions. The university's formal group-submission record remains a separate administrative fact.

The byte-bigram/DCT representation follows prior work by Mohammed et al. (2021); ThreatVision's contribution is its engineering implementation and integration, not a new transform. Static criteria determine the final binary label, while the CNN can adjust the numeric threat score by no more than five points. Family outputs are rule-based profiles. The interface heatmap is a CSS illustration, not a gradient explanation.

### Post-submission experimental investigation

After the academic submission, I investigated the neural model's response to selected Windows PE, synthetic, and out-of-domain inputs. The supplied CSV contains 46 unique file hashes: ten rows labeled benign PE, twenty transformations derived from two of those files, and sixteen synthetic or out-of-domain probes. The ten PE rows have mean neural score 0.2166 (sample SD 0.1707), with nine below 0.50.

Overlay responses depended on the source PE. Appending random bytes raised the `cli-64` neural score from 0.459961 to 0.999023 across four variants, whereas the `windows-kill` score rose from 0.201538 to 0.253418 and then fell to 0.147583. Three overlay variants received a malware final label. The transformations alter multiple byte properties, and the pilot has no known-malicious PE cohort or independently verified labels. It therefore does not isolate entropy, establish shortcut learning, or measure malware-detection effectiveness. The CSV and evidence limits are detailed in the [experimental record](experimental-record.md).

### Research question and proposed tests

The main question is: **Do frequency-domain neural representations add measurable predictive value beyond conventional PE static features when dataset bias, sample lineage, and generalization are properly controlled?** The next work should proceed in order: recover and validate checkpoint and preprocessing provenance; establish scalar and byte-histogram baselines; run paired, controlled perturbations; compare raw-bigram and DCT representations; and evaluate static-only and combined systems on a shared, leakage-resistant labeled split. Each comparison should pre-specify its hypothesis, baseline, data, confounders, metric, and result that would count against the hypothesis.

The benchmark must contain lawful raw binaries with documented labels, sources, time windows, duplicate handling, and packing status. A dataset with 4,000 files is not automatically sufficient to support an FPR of 0.001: with 2,000 independent benign test files and zero errors, the approximate one-sided 95% upper bound is 0.0015. The test size must be chosen for the target interval and account for family/source clustering. New dataset construction is warranted only if existing data cannot support the required raw-file and provenance controls. The full study has no promised completion time.

### Recovered provenance and historical evaluation limits (November 2026)

Two original Colab/Drive exports have been checked without executing notebooks or weights. They contain eight notebooks, a **256×256** MobileNetV2 Keras checkpoint dated 11 May 2026, a 4,000-image manifest with balanced label strings, and a 22-row training log. An older notebook's stored outputs report **67.00%** scratch-CNN and **61.50%** MobileNetV2 test accuracies, but these have not been independently reproduced and cannot be assigned to the **different 224×224 deployed checkpoint**. The later notebook reports 79,997 image-folder entries, yet does not establish a completed reproducible training run. Its separate train/validation loader shuffling introduces a possible partition-overlap risk. The training log's uniformly zero validation AUC and unit precision require investigation; no validated detection-performance result is claimed. [Source-by-source audit](audits/RECOVERY_CROSSCHECK_2026-11-18.md).

### Current status

The production 224×224 checkpoint passed registered-SHA safe loading and six repeatable synthetic probes in Python 3.11.15, Keras 3.14.1 and TensorFlow 2.16.1. Its application and research preprocessing stages and neural outputs matched exactly on three harmless fixtures. A local harmless-PE HTTP flow reached static analysis, DCT conversion, inference and fusion. These checks do not establish historical training parity, model lineage, labels, splits, accuracy or calibration. A prior TensorFlow 2.21 run produced different synthetic outputs, so cross-runtime numerical equivalence is not established. The recovered 256×256 checkpoint remains separate. The hosted site still displays unsupported model and performance claims; the public repository is older than the reviewed local checkout. Do not use either public link until the owner publishes and verifies the reviewed materials. Sample-level pilot measurements remain outside the public tree pending confirmation of redistribution terms.

### References

Aghakhani et al. (2020), “When Malware is Packin’ Heat; Limits of Machine Learning Classifiers Based on Static Analysis Features,” NDSS 2020, https://doi.org/10.14722/ndss.2020.24310.  
Mohammed et al. (2021), “Malware Detection Using Frequency Domain-Based Image Visualization and Deep Learning,” *Proceedings of the 54th Hawaii International Conference on System Sciences*, 7132–7141, https://doi.org/10.24251/HICSS.2021.858.

**Public repository link:** Add after the owner publishes the reviewed local changes and verifies the remote README and evidence links.

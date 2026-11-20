# ThreatVision: research prospectus

**Technical author:** Ahsan Ali Salamat, The University of Faisalabad

**Formal final-year-project record:** Group submission by Ahsan Ali Salamat and Usman Manzoor

## Project and engineering contribution

ThreatVision is a Windows PE triage prototype combining static analysis with a byte-bigram/DCT image path and a MobileNetV2-based advisory score. I independently designed and implemented its technical architecture, analysis pipeline, application integrations and analyst interface. The byte-bigram/DCT representation follows Mohammed et al. (2021); ThreatVision's contribution is the engineering implementation and integration. Static criteria determine the final binary label, while the neural score can adjust the numerical threat score by at most five points. The sigmoid output is not calibrated as a probability.

## Verified engineering evidence

The companion application's 224×224 checkpoint was verified against SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`, loaded with safe Keras deserialization, and tested on five deterministic synthetic tensors and one harmless PE-derived tensor. The separate recovered 256×256 checkpoint was verified under its own registered identity. Three deterministic harmless fixtures matched exactly between current application and research preprocessing at eight stages, and the real production checkpoint returned matching outputs from both paths. A local companion-backend test exercised a harmless-PE request through static analysis, inference, score fusion and API formatting. The public research suite passes 38 engineering tests. These checks establish runtime and implementation behavior; they do not measure classification performance or recover historical training.

## Proposed research question

**Do byte-bigram/DCT neural representations contribute predictive information beyond conventional PE static features under leakage-resistant evaluation?**

The initial study would compare pre-specified static-feature baselines with the same features plus a frozen neural score on identical, lawful PE examples with independently documented labels. Duplicate, source and lineage groups would be assigned to immutable partitions; scaling and model selection would use training and validation data only. A prespecified held-out metric and group-aware uncertainty estimate would test whether any gain is practically meaningful. Source and time shifts, packed-benign samples and controlled perturbations are secondary analyses. A null result would be informative.

<!-- page break -->

## Design and decision criteria

The primary comparison would use regularized logistic regression. The baseline would include file size, byte entropy, null fraction and available PE static indicators; the augmented model would add only the frozen checkpoint score. The primary endpoint would be paired held-out PR-AUC difference with a source/family-group bootstrap interval. The study would also report operating-point errors and packed-benign cases using a threshold fixed on validation data. It would not tune the checkpoint or choose the threshold on the final test set. An improvement smaller than a preregistered practical margin, or an increase in important benign errors, would count against the proposed value.

The sample plan must reflect the desired precision and independent source/family groups. For example, zero false positives among 2,000 independent benign test files still gives an approximate one-sided 95% upper false-positive-rate bound of 0.0015. The project would not claim a 0.001 rate from that sample. Unknown overlap with the checkpoint's historical training set also limits generalization claims until its data lineage can be recovered.

## Data and evidence limits

The model's training-data identity, label provenance, split membership and checkpoint-selection history have not been established. Recovered historical notebooks and logs describe separate experiments and cannot be assigned to the production checkpoint; see the [experiment and checkpoint lineage register](experiment-lineage.md). A 46-row diagnostic pilot has no independently confirmed labels or known-malicious PE cohort, and its sample-level inputs are unavailable in this repository. It is not a detection benchmark. No accuracy, ROC-AUC, calibrated probability, false-positive rate or generalization claim is made.

Original PE and image datasets and model weights are not included. The public research code and tests can be inspected and the safe suite can run without malware samples. Exact model inference needs the external checkpoint; application parity needs the companion application's converter. Setup and commands are in [Reproducibility](../REPRODUCIBILITY.md).

All samples would need lawful acquisition terms and independently supported labels. The study should publish a versioned manifest, duplicate/lineage assignments and split-generation method while keeping executable files in controlled storage. Feature extraction, scaling, threshold selection and model comparison must preserve provenance and prevent information from the test set entering development.

## Selected references

- Aghakhani et al. (2020), “When Malware is Packin’ Heat; Limits of Machine Learning Classifiers Based on Static Analysis Features,” NDSS 2020. [doi:10.14722/ndss.2020.24310](https://doi.org/10.14722/ndss.2020.24310).
- Mohammed et al. (2021), “Malware Detection Using Frequency Domain-Based Image Visualization and Deep Learning,” *Proceedings of the 54th Hawaii International Conference on System Sciences*, 7132–7141. [doi:10.24251/HICSS.2021.858](https://doi.org/10.24251/HICSS.2021.858).

See the full [references](references.md) and [proposed research plan](future-research.md).

# Research Prospectus

## Evaluating frequency-domain features for malware triage

**Project basis:** ThreatVision, an undergraduate Software Engineering final-year project at The University of Faisalabad  
**Original project authors:** Ahsan Ali Salamat and Usman Manzoor

### Research background

Static malware triage examines files without executing them, but packing, obfuscation, and dataset effects can make static signals difficult to interpret. Malware visualization and binary-derived image features have been explored in prior work. Mohammed et al. (2021) describe counting byte bigrams and transforming the representation with a DCT; their work also reports a benchmark study on MaleX. ThreatVision implements a related preprocessing pipeline but does not claim the method as original. Research on packed binaries has shown that classifiers can learn packer-associated signals that do not necessarily correspond to malicious behavior or transfer to unseen packers (Aghakhani et al., 2020).

The question motivating my post-submission investigation is whether a frequency-domain model can distinguish class-related evidence from entropy, packing, file format, or dataset-source cues. This question remains open because the training data provenance and an independent evaluation record for the deployed checkpoint are unavailable.

### Completed undergraduate work

ThreatVision was developed collaboratively as an undergraduate final-year project. It combines upload validation, PE static analysis, a bigram/DCT preprocessing path, a MobileNetV2-based inference artifact, heuristic score fusion, and a web-based scan dossier. The deployed model returns a scalar malware score, but static-analysis criteria determine the final malware/benign label. Neural inference can adjust the numerical threat score by at most five points. The family profiles in the application are heuristic rules; the interface heatmap is a CSS illustration, not a gradient-derived explanation.

After submission, I continued investigating model behavior and considered ways to improve data quality and evaluation. The audit records selected random-byte and compressed-PDF inputs receiving high neural scores, while selected structured or constant-byte inputs received low scores. I interpret these probes as motivation to test possible shortcut learning, not as proof of its cause or prevalence. No exact dates are asserted. The project handoff does not establish individual authorship or exact timing for every later code change.

### Research gap and proposed hypotheses

The available evidence cannot determine whether the high scores arose from entropy sensitivity, data noise, source or label confounding, preprocessing, checkpoint lineage, or another factor. Dataset noise has not been shown to be the sole cause, and a new dataset would not necessarily solve the problem.

The proposed study would test whether: (1) performance changes when benign and malicious files are controlled for entropy, packing, and file format; (2) static PE signals add useful information beyond the frequency image; (3) family-grouped and time-separated evaluation differs from random splitting; and (4) neural scores can be calibrated well enough to support cautious analyst use. These are hypotheses, not findings.

### Planned methodology

Select lawful datasets with documented sources, collection windows, and label procedures. Record provenance, exact and near-duplicate controls, file format, packer status, and label confidence in a restricted manifest. Construct family-grouped and time-aware train, validation, and test partitions before model selection. Include benign packed utilities and compressed files, alongside malicious files and suitable non-PE controls.

Compare simple static baselines, the existing bigram/DCT model, a byte or spatial-image baseline, and hybrid variants. Ablate null suppression, the DCT transform, static signal groups, and the CNN score adjustment. Pre-register thresholds and report ROC-AUC and PR-AUC, false-positive rate at fixed recall, calibration, confidence intervals, and results by time, family, format, entropy, and packing status. Evaluate robustness on unseen sources and packers where safe and lawful. Treat explanation maps as exploratory until faithfulness and stability have been assessed.

### Data and resource requirements

This work requires permissioned data access, secure malware handling, label review, duplicate analysis, compute for training and ablations, and time for independent evaluation. It also needs clear data-use terms and a plan for publishing safe metadata without redistributing malware. I am concluding the current development phase because those resources are not presently available. This is a practical limit on the current investigation, not the end of the research problem.

### Potential research contribution

The study could clarify whether frequency-domain features carry evidence beyond entropy, packing, and dataset artifacts, and measure the contribution of static PE signals under realistic splits. It may identify where the approach does not generalize. No improved accuracy is promised or assumed.

### References

Aghakhani et al. (2020), “When Malware is Packin’ Heat; Limits of Machine Learning Classifiers Based on Static Analysis Features,” NDSS 2020, https://doi.org/10.14722/ndss.2020.24310.  
Mohammed et al. (2021), “Malware Detection Using Frequency Domain-Based Image Visualization and Deep Learning,” *IEEE Access*, 9, 87405–87417, https://doi.org/10.1109/ACCESS.2021.3089069.

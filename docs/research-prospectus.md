# Research Prospectus

## Evaluating frequency-domain features for malware triage

**Project basis:** Collaborative undergraduate Software Engineering Final Year Project at The University of Faisalabad

**Original project authors:** Ahsan Ali Salamat and Usman Manzoor

### Research background

Static malware triage examines files without executing them, but packing, obfuscation, and dataset effects can complicate the interpretation of static signals. Prior research has visualized binaries and studied image-based malware classification. Mohammed et al. (2021) introduced byte-bigram counts transformed with a DCT and evaluated them on MaleX. ThreatVision implements a related preprocessing path and does not claim the method as original. Research on packed binaries has also shown that classifiers may learn packer-associated signals that fail to generalize to unseen packers (Aghakhani et al., 2020).

The question that motivated my post-submission investigation is whether a frequency-domain model can distinguish malware-related evidence from entropy, packing, file format, or dataset-source cues. This remains unresolved because the local training distribution, training history, and independent evaluation for the deployed checkpoint are unavailable.

### Completed undergraduate work

We developed ThreatVision collaboratively as a final-year project. The application integrates upload validation, PE static analysis, byte-bigram/DCT preprocessing, a MobileNetV2-based inference artifact, heuristic score fusion, and a web scan report. Static-analysis criteria determine the final malware/benign label; the CNN can adjust the numeric threat score by at most five points. The family profiles are heuristic rules, and the interface heatmap is a CSS illustration rather than a gradient-derived explanation.

After submission, I continued investigating model behavior. Selected random-byte and compressed-PDF inputs received high neural scores, while selected structured and constant-byte inputs received low scores. These PDFs and random streams are outside the model's intended Windows PE triage domain. The probes motivate a controlled study of possible score sensitivity to entropy, file format, and other confounding factors, but they do not establish shortcut learning or a false-positive rate. Individual authorship and dates for later code changes are not established, so this account does not assign them.

### Research gap and hypotheses

The available evidence cannot determine whether the observed scores arose from entropy sensitivity, source or label confounding, preprocessing, checkpoint lineage, or another factor. Dataset noise has not been shown to be the sole cause. A new dataset would not by itself resolve these possibilities.

A follow-up study could test whether model performance changes when benign and malicious files are controlled for entropy, packing, and format; whether PE static signals add information beyond the frequency image; whether family-aware and time-aware splits change conclusions; and whether neural scores can be calibrated for cautious analyst use. These are questions, not findings.

### Proposed methodology

Select lawful datasets with documented sources, collection windows, and label procedures. Record provenance, duplicates, file format, packing status, and label confidence in a restricted manifest. Freeze family-aware and time-aware partitions before model selection. Include benign packed utilities and compressed files alongside malicious PE samples and relevant non-PE controls.

Compare simple static baselines, the existing bigram/DCT model, a byte or spatial-image baseline, and hybrid variants using common partitions and labels. Ablate null suppression, the DCT transform, static feature groups, and the CNN score adjustment. Pre-register thresholds and report ROC-AUC, PR-AUC, false-positive rate at fixed recall, calibration, confidence intervals, and results by time, family, format, entropy, and packing status. Test robustness on unseen sources and packers where safe and lawful. Treat explanation maps as exploratory until their stability and faithfulness are assessed.

### Data and resource requirements

This work requires permissioned data access, secure malware handling, label review, duplicate analysis, compute for training and ablations, and time for independent evaluation. It also requires clear data-use terms and a plan for sharing safe metadata without distributing malware. I am concluding the current development phase because those resources are not presently available. This is a practical limit on the current phase, not a resolution of the research question.

### Potential contribution

The proposed study could clarify whether frequency-domain features carry evidence beyond entropy, packing, and dataset artifacts, and measure the contribution of static PE signals under realistic splits. It may show that the approach does not generalize. No accuracy improvement is assumed.

### References

Aghakhani et al. (2020), “When Malware is Packin’ Heat; Limits of Machine Learning Classifiers Based on Static Analysis Features,” NDSS 2020, https://doi.org/10.14722/ndss.2020.24310.  
Mohammed et al. (2021), “Malware Detection Using Frequency Domain-Based Image Visualization and Deep Learning,” *Proceedings of the 54th Hawaii International Conference on System Sciences*, 7132–7141, https://doi.org/10.24251/HICSS.2021.858.

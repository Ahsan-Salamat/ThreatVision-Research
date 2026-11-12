# Post-Submission Investigation

## From the capstone to a research question

ThreatVision began as a collaborative undergraduate Final Year Project by Ahsan Ali Salamat and Usman Manzoor. After submission, I continued examining the system, with particular interest in how its neural model responded to inputs that did not resemble ordinary Windows PE files. I am describing my investigation separately from the collaborative engineering work because the available project record does not assign individual authorship or dates to every later code change.

## What prompted the investigation

In selected diagnostic probes, random-byte input and a compressed PDF received high neural scores; a structured text PDF and a constant-byte input received low scores. This pattern made me question which properties of the transformed bytes influenced the CNN. The model was developed for Windows PE triage, but its actual training distribution is undocumented. The PDF and random-byte streams therefore should be treated as out-of-distribution probes, not as representative malware or benign PE examples.

The scores varied across these selected input types. That observation is limited to the probes recorded: there are no repeated trials, complete sample set, controlled feature comparisons, or uncertainty estimates. It does not establish an operational false-positive rate. Sensitivity to entropy or spectral dispersion is one possible explanation, alongside file format, packing, source or label confounding, preprocessing behavior, and checkpoint history. Shortcut learning has not been scientifically demonstrated for this model, and dataset noise has not been shown to be the sole cause.

## What the deployed system does with the CNN score

The application uses PE static-analysis criteria to determine the final malware/benign label. The CNN can adjust the numeric threat score by at most five points, but it has no authority over the binary label. This bounds the model's role in the implemented application; it does not validate the static rules or establish that the score adjustment improves decisions. No independent calibration or evaluation report for the static scorer is available.

## What I considered testing

I considered whether a dataset with documented sources, defensible labels, duplicate controls, and explicit representation of benign packed or compressed files could support a more informative evaluation. I also considered family-aware and time-aware splits, comparisons with simpler static baselines, and tests that vary entropy, packing, and format while holding other properties as constant as possible. These are research directions only. I have not built or validated the proposed dataset, and no experiments are reported here as completed.

A new dataset would not automatically resolve model weaknesses. The representation, label process, model selection, split design, and evaluation protocol could each introduce their own bias. The missing local training data and histories also prevent me from determining whether the current checkpoint learned class-related structure or correlated dataset properties.

## Why I am concluding this phase

The controlled follow-up would require access to suitable data, careful curation and label review, secure malware handling, computational capacity, and time for repeated comparisons and independent testing. Those resources are not presently available to me, so I am concluding the current development phase. This practical limit does not resolve the scientific question.

The present account is therefore a record of completed collaborative engineering followed by an individual investigation that identified a testable concern. It does not claim peer review, external validation, or reproducibility from the public materials. I would next test whether the CNN adds information beyond entropy, packing, format, and data source under a pre-specified, leakage-resistant evaluation.

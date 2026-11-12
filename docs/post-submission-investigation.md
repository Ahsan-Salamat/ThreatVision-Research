# Post-Submission Investigation

## Scope and authorship

ThreatVision began as a collaborative undergraduate final-year project. After the project submission, I continued investigating the implementation and the model behavior. This account follows that relative chronology; no submission date or date for the subsequent probes is supplied here. The available audit identifies the authors of the original capstone but does not establish individual authorship or exact timing for each post-submission code change. I therefore distinguish my investigation from implementation details that can only be attributed to the project collectively.

## What prompted further investigation

The deployed image model returned high malware scores for selected random-byte and compressed-PDF inputs, while selected structured or constant-byte inputs received low scores. The audit records these probes but does not provide a complete test protocol, repeated trials, a representative sample, or a controlled comparison. I treated the pattern as a reason to investigate possible shortcut learning: the model may respond to entropy or spectral dispersion that happens to correlate with its training labels. The probes do not prove that explanation, and they do not show that dataset noise alone caused the behavior.

## Engineering response recorded in the handoff

The audited scorer gives static analysis authority over the final malware/benign label and limits the neural model to a numerical adjustment of at most five points. The handoff connects this arbitration design to concern about high-entropy false alarms. This is a verified property of the deployed scoring logic, not a validated remedy: the static rules themselves have no independent calibration or evaluation report in the supplied evidence. The post-submission record does not identify who authored this specific change or when it was made, so this account does not claim individual implementation credit.

## Dataset and evaluation questions

I considered whether a more carefully controlled dataset, constructed with reliable provenance and labels, could make future evaluation more informative. That is a proposed direction, not a dataset already built or a result already demonstrated. Such work would require source and acquisition metadata, duplicate and near-duplicate controls, label adjudication, representation of benign packed and compressed files, and split designs that reduce family, temporal, and source leakage. It would also require pre-registered baselines and evaluation criteria, secure handling of malware, and sufficient computational resources for data preparation and model comparison.

A new dataset would not automatically solve shortcut learning. The representation, model, label process, and split protocol would still need to be examined through controlled experiments and external evaluation. Alternative explanations for the observed model scores remain possible because the training corpus and histories are not available.

## Why this phase is concluding

I am concluding and documenting the current development phase because the resources required for a meaningful follow-up study are not currently available. These include suitable data access, careful labeling and curation, compute, and time for repeated controlled evaluation. Resource constraints are one reason to stop the current phase; they do not establish the cause of the model behavior, and this decision does not close the research problem.

The project is therefore best presented as completed undergraduate engineering followed by an independent investigation that surfaced methodological questions. No peer-reviewed publication, comprehensive dataset study, or validated performance result is claimed. The next step would be a separately scoped research study with a documented protocol and appropriate supervision and resources.

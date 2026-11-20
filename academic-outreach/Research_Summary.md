# ThreatVision research summary

**Ahsan Ali Salamat** · BS Software Engineering · The University of Faisalabad, Pakistan

**Formal project record:** Group-submitted final-year project with Usman Manzoor

## Engineering contribution

I independently designed and implemented ThreatVision's technical architecture, PE static-analysis pipeline, byte-bigram/DCT image transformation, MobileNetV2 integration, bounded score fusion and analyst-facing interface. The frequency-domain representation follows Mohammed et al. (2021); it is established prior work, not a new transform. Static rules determine the final label, while the neural score can adjust the numerical risk score by at most five points.

## Evidence

The 224×224 production checkpoint was checked against its registered SHA-256, safely loaded and run on five deterministic synthetic tensors plus a harmless PE-derived input. A separate recovered 256×256 checkpoint was verified under its own identity. Application and research preprocessing matched exactly across eight stages for three harmless fixtures, including outputs from the real production model. A local companion-backend test also exercised a harmless PE through analysis and inference. The public research suite passes 38 engineering tests. These checks demonstrate selected software behavior; they do not measure detection performance.

## Proposed research

**Do byte-bigram/DCT neural representations contribute predictive information beyond conventional PE static features under leakage-resistant evaluation?**

The first study would compare pre-specified static-feature baselines with those same features plus a frozen neural score on lawful PE files with independently documented labels. Duplicate and lineage groups would remain within immutable partitions; source/time holdouts and a preregistered metric would test whether any incremental value generalizes. A null result would be informative.

## Limitations

The production checkpoint's training data, labels, split membership and selection history are not established. The available diagnostic pilot has no known-malicious PE cohort or independently verified labels. The original data and model weights are not included. No accuracy, AUC, calibrated probability, false-positive rate or generalization result is claimed. See the [model card](../docs/model-card.md), [experimental record](../docs/experimental-record.md) and [reproducibility guide](../REPRODUCIBILITY.md).

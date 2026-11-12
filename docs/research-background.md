# Research Background

## Malware triage and analysis modalities

Static analysis inspects file structure, imports, strings, and code without executing the sample. Dynamic analysis observes behavior during execution, but results can depend on the sandbox environment and whether the relevant behavior is triggered. The two approaches provide different evidence. Packing and obfuscation can conceal or distort static features [2, 5].

A strong benchmark score does not show by itself that a classifier learned properties tied to malicious behavior. Aghakhani et al. studied packed binaries and found that packer-related signals can lead to poor generalization to unseen packers [2]. This motivates controlled evaluation of packing effects; it does not establish the same failure mechanism in ThreatVision.

## Binary visualization and frequency features

Nataraj et al. represented binaries as grayscale images and studied their visual texture [1]. Saxe and Berlin applied deep neural features to two-dimensional binary program features [3]. Mohammed et al. introduced byte-bigram counts transformed with a DCT and evaluated the representation using MaleX [5]. ThreatVision implements a related preprocessing pipeline; the representation and its main steps are prior work, not an original contribution of this project.

A fixed-size frequency image can expose global patterns, but it also removes aspects of byte order and mixes different semantic causes into similar image statistics. Entropy, compression, packing, padding, file format, and data source can affect the representation. Controlled experiments are needed to determine whether the model uses class-related evidence or such correlates.

## Dataset and evaluation design

Benchmark interpretation depends on dataset provenance, label construction, duplicates, time windows, and split design. EMBER documents its dataset versions and collection periods [6]. EMBER2024 describes weekly collection and temporal evaluation [7]. These projects illustrate why split and provenance details matter; they are not evidence that ThreatVision used either dataset.

The local training source, label process, deduplication method, and split manifest for `threatvision_v01.keras` are not documented. The available record therefore cannot establish its training-set composition or generalization. Proposed data requirements are listed in [Dataset provenance](dataset-provenance.md), and possible evaluation methods are outlined in [Future research](future-research.md).

## Relevance to ThreatVision

ThreatVision combines a frequency-domain CNN score with PE static indicators. Static criteria control the final binary label, while the neural score can adjust the numeric threat score by no more than five points. This is an implemented decision rule, not evidence of calibrated fusion or accurate classification. The later diagnostic probes included random bytes and PDFs outside the intended Windows PE domain. Their differing scores motivate questions about input sensitivity but do not establish that the model learned a shortcut.

## References

Full citations are in [References](references.md) and [references.bib](../references.bib).

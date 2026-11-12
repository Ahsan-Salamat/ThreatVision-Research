# Research Background

## Malware triage and analysis modalities

Malware analysis commonly combines static inspection of a file with dynamic observation of its execution. Static analysis can inspect headers, sections, imports, strings, and code without running a sample. It can be efficient and useful for triage, but packing and obfuscation can hide or distort the features being inspected. Dynamic analysis can reveal behavior, yet sandbox observations may depend on environmental conditions and may not trigger all behavior. These are complementary views rather than interchangeable evidence [1, 2].

Machine-learning systems built from static features can learn stable properties of malware, but a benchmark score does not by itself show that the model learned malicious behavior. Aghakhani et al. studied packed binaries and showed that benign and malicious packing practices can create misleading associations and poor generalization to unseen packers [2]. This prior work motivates controlling for packing and related file characteristics when evaluating a static detector; it does not establish that ThreatVision has the same failure mechanism.

## Binary visualization and frequency representations

Nataraj et al. demonstrated malware visualization by reshaping binary data into grayscale images and examining texture patterns [1]. Saxe and Berlin studied deep neural features derived from two-dimensional binary program features [3]. Mohammed et al. later described a byte-bigram representation transformed into the DCT frequency domain and reported experiments on the MaleX benchmark [4]. ThreatVision adapts and operationalizes the latter family of methods in its preprocessing pipeline. It does not claim to originate byte-to-image malware visualization, bigram counting, or the DCT representation.

A frequency representation can expose global patterns and give a convolutional model a fixed-size input. It also discards aspects of the original byte ordering and maps multiple semantic conditions into similar visual statistics. High entropy, compression, packing, padding, and file type can all affect a frequency image. Whether the CNN distinguishes malware-related structure from those properties must be established by controlled evaluation rather than inferred from the transform itself.

## Dataset and evaluation design

A malware benchmark depends on provenance, label construction, duplicate controls, time window, and split methodology. EMBER documents the feature version and collection periods for its PE benchmark; EMBER2024 describes weekly collection and a temporal holdout, along with multiple file types and label categories [5, 6]. These examples show why dataset version and split definitions matter when interpreting model performance. They are references for documentation practice, not evidence that ThreatVision used either dataset.

The local training-data provenance, deduplication process, label source, and split manifest for `threatvision_v01.keras` are unavailable. The project therefore cannot support claims about its training set, contamination risk, or generalization. Further dataset requirements are listed in [Dataset provenance](dataset-provenance.md), and a proposed study is outlined in [Future research](future-research.md).

## Relevance to ThreatVision

ThreatVision combines a frequency-domain CNN score with PE static indicators. The deployment rule deliberately gives the static analysis full authority over the final binary label and limits neural influence to a small score adjustment. This architecture makes it possible to present distinct types of evidence, but it does not establish that the fusion is calibrated or that the overall system is accurate. The post-submission investigation was prompted by selected high model scores on random and compressed inputs; the possible relationship to entropy remains a hypothesis.

## References

1. Nataraj et al. (2011), *Malware images: Visualization and automatic classification*.
2. Aghakhani et al. (2020), *When Malware is Packin’ Heat; Limits of Machine Learning Classifiers Based on Static Analysis Features*.
3. Saxe and Berlin (2015), *Deep neural network based malware detection using two dimensional binary program features*.
4. Mohammed et al. (2021), *Malware Detection Using Frequency Domain-Based Image Visualization and Deep Learning*.
5. Anderson and Roth (2018), *EMBER: An Open Dataset for Training Static PE Malware Machine Learning Models*.
6. Joyce et al. (2025), *EMBER2024: A Benchmark Dataset for Holistic Evaluation of Malware Classifiers*.

Full citations are in [References](references.md) and [references.bib](../references.bib).

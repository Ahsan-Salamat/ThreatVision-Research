# Diagnostic pilot record

This is a limited, post-submission diagnostic observation of model outputs. It is not a malware-detection benchmark. The production checkpoint's engineering verification is reported separately in the [model card](model-card.md) and [runtime record](audits/PRODUCTION_CHECKPOINT_VERIFICATION.md).

## Inputs and preprocessing

The supplied pilot table contains 46 distinct hash strings: 10 rows labeled benign Windows PE, 20 transformations derived from two of those inputs, six out-of-domain probes, eight synthetic random streams and two synthetic constant streams. The transformation groups include byte shuffles, null padding, random-byte overlays and repeated content. The original input binaries, full source/label manifest, transformation program and random seeds are not in this repository. The 10 benign labels have not been independently confirmed.

The current byte representation counts overlapping adjacent pairs in a 256×256 matrix, suppresses the `(0,0)` count, normalizes and quantizes counts, applies an orthonormal 2D DCT-II, log-compresses coefficient magnitudes, rescales to 8-bit and resizes to 224×224. The caller divides by 255 before inference. This current pipeline matched the companion application's converter on harmless deterministic fixtures; historical training preprocessing has not been established.

## Descriptive observations

| Input group in supplied table | Rows | Mean neural score ± sample SD | Score ≥ 0.50 | Final label: malware |
| --- | ---: | ---: | ---: | ---: |
| Rows labeled benign Windows PE | 10 | 0.2166 ± 0.1707 | 1/10 | 0/10 |
| Byte shuffles | 2 | 0.0484 ± 0.0102 | 0/2 | 0/2 |
| Null padding | 6 | 0.3307 ± 0.1415 | 0/6 | 0/6 |
| Random-byte overlays | 8 | 0.5470 ± 0.3768 | 4/8 | 3/8 |
| Repeated content | 4 | 0.3332 ± 0.1521 | 0/4 | 0/4 |
| Out-of-domain probes | 6 | 0.7157 ± 0.4001 | 4/6 | 1/6 |
| Synthetic random streams | 8 | 0.9981 ± 0.0012 | 8/8 | 0/8 |
| Synthetic constant streams | 2 | 0.3916 ± 0.1858 | 1/2 | 0/2 |

These summaries describe the supplied rows only. Standard deviations are not confidence intervals, and rows derived from the same inputs are dependent. The synthetic and out-of-domain groups are not representative PE examples.

Two histogram-preserving byte shuffles preserved the supplied file-size and Shannon-entropy values while the recorded neural scores fell. Random-byte overlay responses varied by source: one source's score rose across its overlays, while the other's rose and then fell. Three of the eight overlay rows received a malware final label. An overlay changes file size and several byte-frequency properties together, so the pilot does not isolate an entropy effect. Null padding and repeated-content interventions showed little or no score movement in the supplied records. These observations do not identify what the model learned.

The supplied table's pooled Spearman correlation between file size and neural score is −0.0691. It mixes unrelated probes and dependent transformations; the independent-row p-value is not interpreted, and the correlation does not rule out size confounding.

## Interpretation limits

The pilot contains no known-malicious PE cohort, no independently verified labels and no independent test partition. The 20 transformed rows derive from only two PE inputs; independence of other rows is also undocumented. A PE signature on synthetic bytes does not make those bytes a valid benign or malicious sample. The application uses static-analysis rules for its final label; the neural score can adjust the numeric threat score by at most five points. Neither component's weights or thresholds have been calibrated against a verified evaluation cohort.

The pilot cannot establish accuracy, ROC-AUC, precision, recall, F1, calibration, a population false-positive rate, shortcut learning or generalization. Its underlying data and transformation process are unavailable here, so independent reproduction is not possible. The measurements are retained only as a narrowly qualified diagnostic observation pending provenance and redistribution review.

The byte-bigram/DCT representation is based on prior work by Mohammed et al. (2021), not an original representation claim. Full citations are in [References](references.md).

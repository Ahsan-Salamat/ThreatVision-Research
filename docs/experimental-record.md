# Experimental Record

This record separates the deployed model, a small post-submission diagnostic pilot, and results reported in prior literature. The pilot describes model outputs on the supplied measurements; it is not a malware-detection benchmark.

## Checkpoint and provenance

The local `threatvision_v01.keras` archive was inspected directly. Its Keras configuration identifies a MobileNetV2-based functional model with a grayscale input adapter, a 128-unit dense layer, and a sigmoid output. The archive metadata records Keras 3.14.1 and a save time of 2026-05-15. Parameter counts recomputed from the serialized layer shapes and trainability flags are 2,422,084 total, 1,512,580 trainable, and 909,504 non-trainable. Of 154 layers nested in the MobileNetV2 backbone, 17 are marked trainable in the saved config. The previously published 2,424,196 count is unsupported; the reason for the discrepancy is not established.

The archive's top-level `compile_config` records Adam with learning rate `4.999999873689376 × 10⁻⁶`, β₁ = 0.9, β₂ = 0.999, and ε = 10⁻⁷, along with binary cross-entropy and accuracy, ROC AUC, precision, and recall metrics. This is saved compile configuration, not an epoch history or evidence of the data used. A debugging script references a separate `phase2_best.keras` path and loads it with `compile=False`. That checkpoint is unavailable, and no artifact hash or export record establishes that it is the source of `threatvision_v01.keras`.

Training scripts, the original training converter, epoch histories, dataset manifests, sample-level labels, and split membership are unavailable. The local training data cannot be identified as MaleX or another named corpus. Literature metrics are not local checkpoint results.

## Preprocessing used in the diagnostic record

For each byte stream, the pipeline counts overlapping adjacent byte pairs into a 256 × 256 matrix, sets `M(0,0)` to zero, divides the remaining counts by their maximum, quantizes to 8-bit grayscale, applies an orthonormal two-dimensional DCT-II, maps coefficient magnitudes through `log(1 + |F|)`, rescales to 8-bit, and resamples to 224 × 224. The model's sigmoid output is reported here as a **neural score**; no calibration evidence supports interpreting it as a calibrated probability.

The transformation can change several properties at once. In particular, appending random bytes changes size, entropy, byte frequencies, and bigram-DCT features together. The pilot therefore cannot attribute a score change to entropy alone.

## Diagnostic pilot and sample structure

The supplied `DIAGNOSTIC_RESULTS.csv` contains 46 rows with 46 distinct SHA-256 values. It labels 10 rows as benign Windows PE inputs; 20 rows are transformations of two of those PE files (two shuffles, six null-padding variants, eight overlays, and four repeated-content variants). The remaining 16 rows are six out-of-distribution probes, eight synthetic random streams, and two synthetic constant streams. Thus, the 46 rows are not 46 independent experimental units. The 20 transformations are clustered on two source PEs; source relationships and random-generation seeds for the other synthetic inputs are not fully documented. The CSV's benign labels and PE indicators have not been independently validated against source records.

| CSV stratum | Rows | Mean neural score ± sample SD | Neural score ≥ 0.50 | Final label: malware |
| --- | ---: | ---: | ---: | ---: |
| Rows labeled benign Windows PE | 10 | 0.2166 ± 0.1707 | 1/10 | 0/10 |
| T1: byte shuffle | 2 | 0.0484 ± 0.0102 | 0/2 | 0/2 |
| T2: null padding | 6 | 0.3307 ± 0.1415 | 0/6 | 0/6 |
| T3: random-byte overlay | 8 | 0.5470 ± 0.3768 | 4/8 | 3/8 |
| T4: repeated content | 4 | 0.3332 ± 0.1521 | 0/4 | 0/4 |
| Out-of-distribution probes | 6 | 0.7157 ± 0.4001 | 4/6 | 1/6 |
| Synthetic random streams | 8 | 0.9981 ± 0.0012 | 8/8 | 0/8 |
| Synthetic constant streams | 2 | 0.3916 ± 0.1858 | 1/2 | 0/2 |

The descriptive standard deviations above summarize the rows in each stratum; they are not confidence intervals and do not account for dependence among transformed samples.

## Selected paired observations

| Input and transformation | Size (bytes) | Entropy (bits/byte) | Neural score | Static score | Final score / label |
| --- | ---: | ---: | ---: | ---: | --- |
| `windows-kill.exe`, original | 80,384 | 3.7151 | 0.201538 | 17 | 13 / benign |
| `windows-kill`, +10 KiB overlay | 90,624 | 4.4090 | 0.227783 | 20 | 16 / benign |
| `windows-kill`, +50 KiB overlay | 131,584 | 5.8591 | 0.253418 | 27 | 23 / benign |
| `windows-kill`, +100 KiB overlay | 182,784 | 6.6310 | 0.191650 | 31 | 27 / benign |
| `windows-kill`, +200 KiB overlay | 285,184 | 7.2535 | 0.147583 | 34 | 31 / malware |
| `cli-64.exe`, original | 14,336 | 5.2505 | 0.459961 | 18 | 15 / benign |
| `cli-64`, +10 KiB overlay | 24,576 | 6.7596 | 0.720215 | 25 | 29 / benign |
| `cli-64`, +50 KiB overlay | 65,536 | 7.6918 | 0.846680 | 29 | 33 / benign |
| `cli-64`, +100 KiB overlay | 116,736 | 7.8658 | 0.989258 | 30 | 35 / malware |
| `cli-64`, +200 KiB overlay | 219,136 | 7.9485 | 0.999023 | 31 | 36 / malware |

The overlay response differed between the two source files. The `cli-64` neural score rose across these four transformations, while the `windows-kill` score rose modestly and then fell. Three of the eight overlay rows received a final malware label. Each overlay also changes file size and the byte and frequency representation, so this is evidence about these interventions, not an entropy-only causal effect or a general packing result.

For the two histogram-preserving shuffles, file size and Shannon entropy match their source rows in the CSV. The `windows-kill` score changed from 0.201538 to 0.041138; the `cli-64` score changed from 0.459961 to 0.055603. This supports sensitivity to byte ordering under these two interventions. It does not establish that the representation captures malware semantics.

The six null-padding rows retain the same neural score as their corresponding original input in the CSV despite changes in size and entropy. Repeated-content rows also show little score movement: `windows-kill` remains at 0.201538, while `cli-64` changes from 0.459961 to 0.460693 and 0.468994 at 2× and 4× size. Eight synthetic random-stream rows from 5 KiB to 1,000 KiB (1,024,000 bytes) have scores between 0.996582 and 0.999512; these are different generated inputs, not a documented size-only intervention.

Across all 46 rows, the descriptive Spearman correlation between size and neural score is approximately −0.0691. This pooled correlation mixes unrelated probes and dependent transformations, so its reported independent-row p-value is not used. It neither disproves size confounding nor replaces a controlled size experiment.

## Static decision behavior

The implementation uses static-analysis criteria to determine the final malware/benign label. The CNN contributes only a bounded adjustment of at most five points to the numeric threat score. In the pilot CSV, all 10 rows labeled benign PE and all eight synthetic noise rows received a benign final label. Three overlay rows and one synthetic `MZ`-plus-random row received a malware label. These selected outputs do not establish the accuracy or reliability of the static decision rules. Their weights and thresholds remain uncalibrated project heuristics.

## Interpretation and reproducibility limits

The pilot contains no known-malicious PE cohort, no balanced labeled split, and no independent benchmark. The 10 rows labeled as benign PE are not accompanied by source and label-verification records. The measured neural scores and final labels are exploratory observations, not accuracy, ROC-AUC, precision, recall, F1, calibration, or false-positive-rate estimates. The supplied correlation p-values assume independent rows; the transformations violate that assumption, so those p-values are not used.

The public repository does not include the model weights, original input binaries, transformation program, run logs, random seeds, or source manifest. The remediation package supplies a measurements CSV but not executable code for reproducing the 46-row study. The sample-level CSV is kept outside the public repository pending confirmation of source-data and derived-measurement redistribution terms. Public aggregate results above can be checked against the local copy, but independent reproduction is not currently possible.

The pilot supports only a narrow conclusion: selected benign PE and synthetic inputs produced varied neural scores, and a score response to overlays depended on the source file. Whether the frequency representation adds useful classification information beyond file statistics and static features remains untested.

## Prior literature

Mohammed et al. (2021) describe the byte-bigram/DCT approach and report results on MaleX. Those results belong to the published study, not to the local ThreatVision checkpoint. See [References](references.md) for the full citation and [Dataset provenance](dataset-provenance.md) for dataset distinctions.

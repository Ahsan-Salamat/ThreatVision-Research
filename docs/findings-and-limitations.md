# Findings and Limitations

## Findings from the diagnostic pilot

The supplied CSV records 46 distinct file hashes: 10 inputs labeled benign PE, 20 transformed files derived from two of those PEs, six out-of-domain probes, eight synthetic random streams, and two synthetic constant streams. The ten PE rows have mean neural score 0.2166 (sample SD 0.1707), with nine below 0.50. These are descriptive values for selected files, not estimates from a representative population.

Byte shuffling preserved file size and the recorded Shannon entropy for two PE inputs, while both neural scores fell. This shows sensitivity to ordering under those interventions. It does not identify the learned feature or establish semantic malware recognition. Overlay results varied by source: the score rose from 0.4600 to 0.9990 for `cli-64`, but the `windows-kill` score peaked at 0.2534 before falling to 0.1476. Three of eight overlays received a final malware label. Since overlays also change size, entropy, and frequency features, the study does not isolate entropy as the cause.

Scores on random streams were uniformly high in this sample, but the probes are synthetic and outside the intended Windows PE domain. Null padding and repeated content produced little or no change in the recorded scores. The pooled Spearman correlation between size and score is approximately −0.0691, but it combines dependent transformations and unrelated input types. Neither this correlation nor the noise-size series rules out a size effect.

## What this study does not establish

The pilot includes no known-malicious PE examples and no independently verified sample labels. It is not a balanced detection benchmark. The 20 transformed observations are clustered on only two PE inputs, and random-stream generation seeds and source relationships are not recorded. Reported p-values that treat all rows as independent are not used. The CSV supplies measurements and hashes, but no source manifest, original overlay files, or runnable program reproducing all 46 rows.

No accuracy, ROC-AUC, precision, recall, F1, calibrated probability, operating threshold, or population false-positive rate can be inferred. A sigmoid output is called a neural score; calibration has not been evaluated. The outputs on selected benign and synthetic inputs do not establish deployment reliability.

## Model and data provenance

The deployed archive's configuration identifies a MobileNetV2 model. It records Keras 3.14.1 and a save time of 2026-05-15. Counts recomputed from its serialized layer shapes are 2,422,084 total parameters (1,512,580 trainable and 909,504 non-trainable), with 17 of 154 nested backbone layers marked trainable. The earlier 2,424,196 figure is unsupported; its cause is not established. The saved top-level `compile_config` records Adam near `5 × 10⁻⁶`, binary cross-entropy, and accuracy, ROC AUC, precision, and recall. A script references a historical `phase2_best.keras` checkpoint, but the file is absent and the deployed artifact's lineage is unestablished.

Training scripts, dataset acquisition records, label procedures, sample counts, split manifests, training histories, and model-selection records are unavailable. It is not established that the local checkpoint was trained on MaleX. Published results from Mohammed et al. (2021) describe that paper's dataset and protocol, not ThreatVision.

## Static decision system and intended use

Static analysis determines the final malware/benign label; neural inference can adjust the numeric threat score by at most five points. Three overlay rows and one synthetic `MZ`-plus-random row in the CSV received a malware final label. These outcomes demonstrate neither effective mitigation nor reliable detection. The static weights and thresholds are hand-set project heuristics and have not been calibrated on a verified labeled corpus. Static indicators such as imports and entropy can also occur in benign software.

The system is a pre-execution triage prototype. It cannot observe runtime unpacking or behavior that occurs only after execution. The deployed model's training domain is undocumented, and the transform's ability to accept arbitrary bytes does not validate non-PE use. Family labels are rule-based profiles. The interface heatmap is a CSS illustration, not Grad-CAM or a model explanation.

## Reproducibility and next step

The public repository omits source code, model weights, original test binaries, training data, the 46-row sample table, and the experiment program. Sample-level measurements remain private pending confirmation of redistribution rights. The current record therefore supports an account of engineering and an exploratory pilot, but not independent reproduction.

The next study should first recover model and preprocessing provenance, then compare simple file statistics, raw bigrams, DCT features, and static-only and combined systems on a common, lawful, labeled split. It should control source, family, time, packing, and duplicate structure and report uncertainty at relevant false-positive rates. The [future research plan](future-research.md) defines falsifiable steps.

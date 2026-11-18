# Recovered original artifacts

**Reviewed:** 18 November 2026  
**Method:** Read-only ZIP listing, CRC checks, notebook JSON inspection, CSV parsing, and Keras archive metadata inspection. Notebook cells, binaries and model were not executed.

The two original exports remain unchanged in Downloads and identical workspace copies. Their SHA-256 hashes are:

| Export | Size | SHA-256 |
| --- | ---: | --- |
| ThreatVision export | 10,025,663 bytes | `c1f72a0856f0be1d02e5026ed845993cbefc94b5514dcaf7254dad6cfefb1859` |
| Colab notebooks export | 2,639,592 bytes | `9c2ada12ddbd6fdb270a07078e732f359d7eed9201d324699d5fbcfc201ba840` |

Both outer archives and the nested model ZIP passed CRC verification.

## Model

The export contains `ThreatVision/best_model.keras` (11,599,393 bytes), SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`. Archive metadata records Keras 3.13.2 and save time 2026-05-11 11:23:04, with timezone unspecified. Serialized topology names a Functional model `ThreatVision_MobileNetV2`, input `(None,256,256,1)`, and one sigmoid output `binary_output`. Its top-level layers are grayscale input, Conv2D channel adapter, Rescaling, MobileNetV2 backbone, global average pooling, dropout, dense 128, dropout, and sigmoid output.

This differs from the later `ThreatVisionFInal.ipynb` construction order, which includes augmentation before rescaling and channel adaptation. The recovered notebook is useful historical evidence, but is not proven to be the exact source of this checkpoint.

The archive is structurally readable. TensorFlow/Keras runtime loading and prediction have not been performed. The checkpoint is not copied into this repository.

## Training logs

`training_log.csv` has 22 records. Every recorded `val_auc` is 0.0 and `val_precision` is 1.0. This combination requires investigation of validation class membership, label mapping, and metric configuration. The CSV alone does not establish that validation contains one class, nor does its validation accuracy support a malware discrimination claim. The log/checkpoint relationship is unproven.

`training_log_phase1_head.csv` is empty.

## Image manifest and notebooks

The Colab export includes an image manifest with 4,000 rows, 2,000 rows for each binary label, and 4,000 distinct hash strings. The image files and underlying PE binaries are absent. Labels, independence, and file lineage cannot be verified from this manifest alone.

Eight notebooks are present. The two ThreatVision-named notebooks contain original development/training material and outputs, including historical test accuracy printouts. These outputs are not independently reproduced results. One notebook uses externally compiled processing functions. Other notebooks identify third-party or broader reference experiments. Review attribution and licensing before sharing them.

## Safe next steps

Use a compatible isolated environment to load the checkpoint with `compile=False, safe_mode=True`, record software versions and repeatability, and infer only on a harmless synthetic PE fixture. Do not execute PE files. Preserve the archive unchanged. Resolve checkpoint lineage against version history and earlier notebook revisions. Recover actual authorized data and split membership before interpreting training metrics. No detected result in these files constitutes an independently validated malware benchmark.

## Later independent cross-check

A further review of saved notebook outputs identified a 4,000-row 2,800/800/400 historical dataset partition and two **unreproduced** older test-accuracy printouts (67.00% scratch CNN; 61.50% MobileNetV2), plus a distinct later 79,997-image directory inventory and a potential training/validation partition-overlap risk. The archive metadata, original notebook code, and the 22-row anomalous log remain insufficient to establish a completed 256×256 training lineage or a 224×224 production evaluation. For details, see the [full reconciliation](RECOVERY_CROSSCHECK_2026-11-18.md).

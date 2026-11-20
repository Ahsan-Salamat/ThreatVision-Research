# Experiment and checkpoint lineage

This register keeps surviving historical observations separate from the two model archives and the current diagnostic pilot. None of the available historical metrics is a validated performance estimate for the production checkpoint.

| Record | What survives | Evidence status and limit |
| --- | --- | --- |
| Earlier 4,000-image experiment | Notebook outputs report 67.00% test accuracy for a scratch CNN and 61.50% for a separate MobileNetV2; a balanced manifest records 4,000 hash-shaped identifiers. | Historical notebook observations only. The image/PE files, label evidence, split membership and checkpoint linkage are unavailable; results have not been independently reproduced. |
| Later ~80,000-image workflow | A notebook reports 39,999 benign and 39,998 malware image-folder entries and starts a 256×256 training run. | No complete training history or independently verified evaluation survives. Separate train/validation loader calls use different shuffle settings, leaving a possible split-overlap risk. |
| Recovered 22-row log | Two sequences totaling 22 epoch rows; maximum recorded `val_accuracy` is 80.27%. `val_auc` is 0.0 and `val_precision` is 1.0 in every row. | Historical log with anomalous metrics. Validation membership, metric behavior and checkpoint association are unknown. It does not establish test performance. |
| `best_model.keras` | SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`; input `(None,256,256,1)`. | Separate recovered checkpoint, safely loaded under its registered profile and run on five synthetic probes plus one PE-derived engineering probe. Training lineage and historical preprocessing remain unverified. |
| `threatvision_v01.keras` | SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`; input `(None,224,224,1)`; 2,422,084 parameters. | Production checkpoint safely loaded and run on five deterministic synthetic tensors plus one harmless PE-derived tensor. App/research preprocessing matched on three fixtures. No training-data link or validated classification result is established. |
| Developer's separate ~85% recollection | Owner recalls approximately 85% accuracy in a MobileNetV2 experiment. | Owner-reported only. The metric type, data, split, checkpoint and supporting outputs are unavailable. Do not describe it as validated accuracy or assign it to either checkpoint. |

## Checkpoint distinction

The 224×224 production artifact and 256×256 recovered artifact have different hashes, input shapes and serialized preprocessing. The registered verifier profiles prevent silent substitution. The recovered model's PE-derived input is created by resizing the current 224×224 representation; it does not reconstruct that model's historical training pipeline. See the [checkpoint verification record](audits/PRODUCTION_CHECKPOINT_VERIFICATION.md) and [application/research parity record](audits/PRODUCTION_PREPROCESSING_PARITY.md).

The diagnostic pilot described in the [experimental record](experimental-record.md) is a separate, limited set of supplied measurements. Its rows and observations must not be treated as a training or test partition for either checkpoint.

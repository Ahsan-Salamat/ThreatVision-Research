# Historical ~85% MobileNetV2 accuracy: evidence status

**Documented:** 18 November 2026. **Status:** Owner-reported, **not independently verified**. This is a reconciliation note, not a fabricated retrospective result.

## The claim

The project developer recalls that a MobileNet-based ThreatVision experiment reached **approximately 85% accuracy**. The original dataset, exact checkpoint identity, independent test split, epoch record, and a saved output establishing **85%** were **not found** in the two recovered Google Drive exports. It is also unknown whether the number refers to **training, validation, or held-out test** accuracy. Therefore, it must not be described as a verified accuracy figure, linked to `best_model.keras` or `threatvision_v01.keras`, used to generate a confusion matrix, or quoted as the project's academic benchmark.

The developer's recollection may be genuine; **the evidence is incomplete**, not proof that the experiment never occurred.

## Closest surviving records (do not merge these studies)

| Artifact / experiment | What its original source actually records | Verification limit |
| --- | --- | --- |
| `ThreatVision.ipynb` (4,000 images) | Saved test-output printout of **67.00%** for a scratch CNN and **61.50%** for a separate MobileNetV2 | Underlying images, label evidence, and independent reproduction unavailable. Neither is the reported 85% run. |
| `training_log.csv` | **22** epoch rows; maximum `val_accuracy` is **0.8027376533 (80.27%)**; maximum `accuracy` **0.7266164422 (72.66%)**; `val_auc` is **0.0** in every row | `val_precision` is **1.0** throughout; validation class membership and checkpoint linkage unknown. Not credible evidence of 85%. |
| `ThreatVisionFInal.ipynb` (later ~79,997-image workflow) | Training script and early progress output, but **no completed epoch history** in the exported output | Validation loader uses different shuffle settings from training; overlap cannot be excluded. No 85% recorded. |
| Recovered `best_model.keras` | Runtime-verified safe load and synthetic forward pass; **256×256×1** MobileNetV2 model, SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102` | No verified notebook-to-weights lineage or held-out predictions. |
| Documented production `threatvision_v01.keras` | Verified actual checkpoint bytes, runtime load, and synthetic forward pass; **224×224×1** and a different SHA-256 | Actual checkpoint bytes absent from recovered exports; no independently reproduced evaluation. |
| Developer recollection | "My best MobileNetV2 accuracy was approximately 85%." | No saved test output, confusion matrix, original scores, or checkpoint provenance supporting the number in supplied archives. |

Third-party reference notebooks (Xception, Fusion) are **not** evidence for ThreatVision's own 85% claim, even if their recorded accuracies are higher.

## Honest recovery and verification path

1. Recover the *specific* run's Colab notebook/checkpoint/log, if it still exists. Preserve original file hashes and timestamps.
2. Recover the underlying authorized files, sample IDs and independent labels; build immutable split membership and lineage/source records. Do not change source labels to reach a target score.
3. Load the exact checkpoint using preprocessing and input shape appropriate to **that** checkpoint. Do not substitute 256×256 for 224×224.
4. Export real per-sample out-of-sample predictions with file hashes, split, checkpoint hash, provenance, labels and source.
5. Run `python -m research.historical_accuracy --predictions ... --checkpoint-sha256 ... --checkpoint ... --output ...`, which calculates descriptive metrics and rejects basic source/lineage/identity mismatches.
6. Independently audit sample origin, labels, lineage, split creation, threshold choice and model selection before publishing a benchmark claim. A passing CSV check or 85% output alone is not enough.
7. If the original run is unrecoverable, run a **new**, pre-specified evaluation and identify it by its new date, dataset version, checkpoint and environment. It cannot be retroactively named the historical 85% run.

**Research presentation:** Describe the engineering implementation and open generalization question. Do not put 85% in cold professor emails, the one-page research brief, or the prospectus until independently supported. If asked about the number, state that it is an unrecovered historical observation whose evaluation protocol is being investigated.

## Reconstructed verification assets

- `notebooks/RECONSTRUCTED_MobileNetV2_Validation.ipynb`: a clearly marked **new**, unexecuted research notebook template; no fabricated saved outputs.
- `research/historical_accuracy.py`: independent input checks and descriptive held-out metrics using actual user-supplied per-sample predictions; does not generate predictions.
- `tests/test_historical_accuracy.py`: seven **synthetic engineering unit tests**, not malware-classification results.

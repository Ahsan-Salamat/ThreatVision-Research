# ThreatVision — recovered evidence versus public research record

**Review date:** 18 November 2026  
**Evidence examined:** `ThreatVision-20261118T030006Z-1-001.zip` (the owner's original Drive export), `Colab Notebooks-20261118T025932Z-1-001.zip` (original Colab export), and the `ThreatVision-Research(3).zip` repository snapshot at embedded commit `7d3b085`.  
**Initial recovery review:** ZIP integrity, SHA-256, notebook JSON source/output inspection, CSV inspection, Keras metadata/configuration, static research-code review, and safe Python tests. At that initial review no model inference had been run. A later same-day follow-up safely loaded both checkpoint files and ran synthetic probes; see the updated production verification report. No notebook, potentially malicious binary, or model training was executed.

## Scope and evidentiary standard

The aim is to make the *published account consistent with the evidence that survived*, not to claim that every historical run or model has been independently reproduced. An observed notebook output is historical evidence of a recorded run, not a newly validated metric. A filename resembling a PE SHA-256 is not independent verification of the underlying binary or label. An intact Keras archive is not proof that it loads or predicts correctly. References to a historical implementation in the public repo should not be confused with availability of the private frontend/backend source.

## Verified artifact summary

| Source | Confirmed from the export | Not established |
| --- | --- | --- |
| Colab archive | Eight `.ipynb` files. Two (`Untitled1`, `Untitled2`) contain no meaningful code. | That every notebook was authored or executed by the project owner; third-party/reference notebooks need attribution and rights review. |
| `ThreatVision.ipynb` | Saved output reports 4,000 matched image rows, 2,000 per label; saved split-output reports 2,800 train / 800 validation / 400 test. Saved evaluation output reports scratch CNN **67.00%** test accuracy and a separate MobileNetV2 experiment **61.50%** test accuracy. | Independent regeneration of either result, the underlying PE and PNG files, label correctness, leakage controls, or linkage to either recovered/deployed `.keras` checkpoint. **Do not use these figures as independently verified performance claims.** |
| `Copy of MaleX_matched_images.csv` | 4,000 rows, 4,000 distinct 64-character hexadecimal strings, 2,000 `label=0`/benign and 2,000 `label=1`/malware records. | Validity/accuracy of actual binaries, malware labels, families, raw PE lineage, or image existence. The manifest is **not** an independently validated benchmark. |
| `ThreatVisionFInal.ipynb` | Single large code cell specifies 256×256 grayscale images, a MobileNetV2 architecture, a 20% validation split, and a reported registry of **39,999 benign plus 39,998 malicious** DCT images (79,997 total). Stored output shows the beginning of a training run, but **not a completed training history**. | That the saved checkpoint came from this exact code or that the 79,997 underlying files and labels remain accessible. The notebook's advertised speed gains are comments, not independently verified timings. |
| `Untitled0.ipynb` | Separate family-classification/SE-residual CNN work, with recorded 25,000 benign images, a malware-family filtering workflow and checkpoint-resume attempts. | Availability of its multiclass checkpoints, verified final evaluation, or connection to the deployed MobileNetV2 binary classifier. |
| `get-byteplot-and-bigramdct-image-representations.ipynb` | Exploratory representation demonstration. | A complete reproducible original pipeline without its external imports/files. |
| The Xception and Fusion notebooks | Reference/broader experiments are present, including saved outputs. | That their results are ThreatVision's independently implemented study; **do not attribute those output metrics to this project**. |
| `training_log.csv` | 22 epoch rows, with epoch counter resetting once (13 rows followed by 9). Every `val_auc` equals **0.0** and every `val_precision` equals **1.0**. | Validation class membership, whether the logged metrics behaved correctly, or a cryptographic link to `best_model.keras`. Do not select a best epoch or report predictive quality from this log. |
| `training_log_phase1_head.csv` | Empty (0 bytes). | Any phase-one result. |
| `best_model.keras` | SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`; 11,599,393 bytes; nested ZIP CRC passes; Keras 3.13.2; archive saved `2026-05-11@11:23:04` (timezone unspecified); Functional `ThreatVision_MobileNetV2`, 256×256×1 input, one sigmoid output; adapter **Conv2D before Rescaling**; no top-level saved augmentation layers. | Safe runtime load and synthetic prediction consistency have since passed on a verified temporary copy. Dataset and epoch provenance, identity with the later 224×224 checkpoint, and identity with any particular notebook remain unverified. |
| Documented `threatvision_v01.keras` | The reviewed Drive exports did not include the production artifact. Its actual bytes were later found in the companion application tree and statically inspected: SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`, Keras 3.14.1, 224×224×1 input. | Safe runtime load and five synthetic forward passes have since passed on the local original bytes. The Drive-export absence does not mean the artifact is unavailable elsewhere. Do **not** substitute `best_model.keras` for it. See [production checkpoint verification](PRODUCTION_CHECKPOINT_VERIFICATION.md). |
| 46-row post-submission pilot | The research repo documents the diagnostic analysis and explicitly limits its conclusions. | The sample-level CSV and input files are **not included in either recovered export**, so its numerical results cannot be recomputed from these exports. Do not conflate this pilot with either image-training dataset. |

### A newly identified train/validation leakage risk

In `ThreatVisionFInal.ipynb`, `build_train_pipeline()` calls `image_dataset_from_directory` with `shuffle=True`, `seed=42`, `validation_split=0.20`, `subset='training'`, while `build_val_pipeline()` makes **a separate call** with `shuffle=False` and `subset='validation'`. With independent indexing/shuffling before split, these may be **different file orderings and overlapping partitions**. Because the raw file lists and TensorFlow environment are absent, overlap cannot be quantified for the historical run. Treat this as a **substantial unresolved historical split-integrity risk**, not proof that a specific sample leaked. Recommended correction for *future* experiments: generate a single manifest of unique file hashes and explicit group-aware train/validation/test assignments; assert zero overlaps; pass these immutable partitions to training. Alternatively, when using directory loaders, create both subsets in one call with `subset='both'`, and separately verify file membership and lineage. **Do not modify the recovered notebook and rebrand it as the historical experiment.**

### A model-preprocessing incompatibility

The 256×256 saved model serializes `grayscale_input → grayscale_to_rgb (Conv2D) → preprocess (Rescaling) → MobileNetV2`. The later `ThreatVisionFInal.ipynb` constructs `grayscale_input → optional augmentation → normalize (Rescaling) → grayscale_to_rgb → MobileNetV2`. The documented 224×224 deployed model also differs in input shape and has its own augmentation nodes and other named layers. These are **three distinct architectural descriptions** until weights, exact code and artifact hashes establish otherwise. They must never be combined into a fabricated single training lineage.

### Attribution and scientific interpretation

Mohammed et al. (2021) introduced the frequency-domain representation used here; ThreatVision's claimed contribution is **engineering integration and a proposed incremental-value evaluation**, not the original invention of the transform. The literature reference was cross-checked against the HICSS publication record: https://aisel.aisnet.org/hicss-54/st/cyber_threat_intelligence/4/ . Results from literature and reference notebooks belong to their respective authors. The prior pilot can motivate hypotheses, but neither the 4,000-image saved notebook outputs nor the 79,997-image workflow establishes generalization or a validated detection rate.

## Additional owner-reported accuracy (not in recovered archives)

After the archive reconciliation, the developer reported an **approximately 85% accuracy** result from a MobileNetV2 experiment. A fresh inspection of the two original exports found **no saved 85% experiment output** in the project-owned notebook runs or 22-row training log. The log peaks at **80.27% validation accuracy** with all-zero validation AUC. The original metric type (train/validation/test), dataset, checkpoint, time, and split for the claimed 85% remain unknown. The claim is preserved only as **owner-reported, unverified history** in [HISTORICAL_ACCURACY_CLAIM.md](HISTORICAL_ACCURACY_CLAIM.md). It is **not** a new test result and does not alter prior scientifically supported conclusions.

## Public research alignment rules

1. Use **'documented production checkpoint'** only for the 224×224 artifact whose original bytes remain unavailable in this review; mark its metadata as *previously recorded*.
2. Use **'recovered earlier checkpoint'** for the intact 256×256 `best_model.keras` and reference its SHA-256. The original model is **not** in the public repository.
3. Distinguish **4,000 manifest rows** (older notebook) from **79,997 observed image-folder entries** (later code/output) and from **46 diagnostic pilot rows**. Their provenance and membership are not interchangeable.
4. Separate **historical notebook printouts** (67.00%, 61.50%, 22 epochs of anomalous metrics) from **scientifically verified results** (none yet established).
5. Document the mismatch between the recovered earlier model and the later notebook implementation; never claim exact original training reconstruction.
6. Avoid claims about model accuracy, ROC-AUC, operational false-positive rates, working public inference, or clinical/production readiness.
7. Do not publish raw notebook exports, model binaries, or data that may carry third-party rights, links, credentials or unverified samples. Publish only sanitized inventory and code for safe audit.
8. Do not infer absence of actual malware binaries from notebook outputs; simply state **not supplied in the two reviewed exports**.

## Verification record and remaining gates

- Archive SHA-256 and nested CRC passed; the non-executing `python -m research.recovery_audit` tool records an auditable metadata summary at [`recovered-artifact-verified-summary.json`](recovered-artifact-verified-summary.json).
- All **14** safe Python tests in the prepared public research repository passed (11 original + three new recovery-audit tests). These are *engineering tests*, not a malware benchmark.
- **Unresolved gates:** source-labeled PE data and immutable split manifest; real TensorFlow model loading/prediction; evidence that saved logs came from a given checkpoint; independent test-set evaluation; public demo browser verification; remote GitHub publication confirmation.

**Initial readiness decision:** At the time of this recovery-only review, runtime checks had not yet been completed. See the [final readiness report](FINAL_PROFESSOR_OUTREACH_READINESS.md) for the updated result after model execution, app integration, local documentation changes, and public-host reachability checks.

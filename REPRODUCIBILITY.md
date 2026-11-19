# Research tooling

Run from the repository root with Python 3.11 or later.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-research.txt
python -m unittest discover -s tests -v
python -m research.validate /path/to/manifest.csv /path/to/authorized-data
python -m research.evaluate --manifest /path/to/manifest.csv --data-root /path/to/authorized-data --features /path/to/features.csv --model-id CHECKPOINT_SHA256 --static-source /path/to/static_analysis.py --output results/new-run
```

The unit tests use harmless bytes and headers. **The recovery audit tool reads ZIP metadata only: it does not execute notebook code or model weights.** The evaluator requires a sidecar matching the manifest, feature file, checkpoint SHA-256, and static analyzer source SHA-256. It records preprocessing and source snapshot hashes, and requires --model-id to be the checkpoint SHA-256. The evaluator expects one row per manifest sample with numeric `static_*` columns and a frozen `neural_score`. It fits scaling and logistic regression on the training partition only. Neural-only, static logistic and combined logistic comparisons share the test samples. The combined estimator is a proposed research baseline and differs from the application's heuristic fusion. Threshold 0.5 is fixed in advance. Metrics JSON and ROC SVG are written to a new output directory.

The manifest requires sample_id, sha256, ground_truth_label, source, label_evidence, file_format, split, dataset_version, lineage_id and relative path. Optional columns include malware_family and collection_date. Empty provenance fields fail validation. A recorded evidence string still requires independent verification by the dataset owner. The validator checks header signatures, sizes, hashes, duplicate IDs and hashes, both classes in each split, and supplied lineage/family separation. It does not establish label correctness or detect unknown relationships. PE header validation does not establish that a file is loadable or harmless.

The numerical preprocessing implementation has been compared stage by stage with the companion application's converter on three deterministic harmless fixtures. Byte stream, bigram counts, zero-pair suppression, normalization, grayscale quantization, DCT output, resized image, final tensor, and the real production checkpoint's output matched exactly. See the [parity method and limits](docs/audits/PRODUCTION_PREPROCESSING_PARITY.md) and its [machine-readable results](docs/audits/production-preprocessing-parity.json). Rerun the comparison after changes to either implementation. This verifies current serving-code parity, not historical training parity.

The production checkpoint's runtime probe has been implemented and executed using the existing Apple Silicon `threatvision` environment (Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1). The separate recovered 256×256 checkpoint was also loaded and probed; see [`PRODUCTION_CHECKPOINT_VERIFICATION.md`](docs/audits/PRODUCTION_CHECKPOINT_VERIFICATION.md). Both checks use synthetic input and establish runtime behavior only. A prior TensorFlow 2.21.0 probe had different synthetic output values; repeated calls were deterministic within a run, but cross-runtime numerical equivalence is not established.

```sh
python -m research.checkpoint /path/to/threatvision_v01.keras \\
  --sha256 1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca \\
  --profile production-224-v1 \\
  --output docs/audits/production-checkpoint-verification.json
```

This uses harmless synthetic tensors and a generated PE fixture only. Both exact registered checkpoint identities are supported through separate required profiles. The verifier records runtime versions, the checkpoint hash, fixture/tensor hashes, six outputs, and repeatability evidence without recording the private absolute path.

Historical notebooks, an earlier 256×256 checkpoint, and a 22-row training log have been recovered; exact training-to-checkpoint linkage, original PE/PNG samples, and split membership remain unavailable. The companion app contains the actual 224×224 checkpoint, whose runtime is verified, but no command can reproduce its historical training. Training, extraction, source/temporal holdouts and group uncertainty modules still require an authorized real-data cohort for end-to-end scientific validation. The evaluation smoke test uses minimal synthetic headers and invented scores, deletes temporary outputs, and checks runner integration only. It is not scientific evidence.

Use the existing [dataset provenance](docs/dataset-provenance.md), [model card](docs/model-card.md), [experimental record](docs/experimental-record.md), and [limitations](docs/findings-and-limitations.md) as the scientific record.

Feature extraction from approved samples uses the production static-analysis module and verified checkpoint:

```sh
python -m research.extract --manifest /data/manifest.csv --data-root /data --checkpoint /restricted/threatvision_v01.keras --checkpoint-sha256 CHECKPOINT_SHA256 --static-source /path/to/ThreatVision/backend/python_scripts/static_analysis.py --output /data/features.csv
```

Generate fixed group, source, or temporal splits with `python -m research.splits`. Source and temporal holdouts fail when a lineage group crosses a boundary. The group strategy uses deterministic shuffled groups and rejects splits missing either class. The evaluator reports a family/lineage cluster bootstrap only when at least ten independent test groups exist. Its interval is conditional on the held-out data and is not a substitute for additional sources or dates. Static features are currently limited to size, global entropy, section count, and signature status. Static-only refers to logistic regression on those fields, not the production heuristic scorer.

A new training pipeline can initialize from the saved architecture topology with fresh random weights. It is not a reconstruction of historical training. Use `requirements-model.txt`, a validated manifest, and an authorized input cohort. `--smoke --cpu` performs one epoch on two samples per partition for engineering checks only. Do not interpret its output as a result.

## Reconstructed verification of historical accuracy claims

The project owner recalls approximately **85% MobileNetV2 accuracy**, but no supplied notebook output, 22-row log or checkpoint-linked test record verifies that figure. The highest `val_accuracy` in the recovered log is **80.27%**, with `val_auc=0.0` throughout. Do not invent missing epochs or treat these as a continuous training history. See [historical claim audit](docs/audits/HISTORICAL_ACCURACY_CLAIM.md).

A new, **unexecuted reconstruction** is provided at `notebooks/RECONSTRUCTED_MobileNetV2_Validation.ipynb`. It does not pretend to be the original notebook. It requires authentic out-of-sample predictions and the specific original checkpoint. The auditor can be run with:

```sh
python -m research.historical_accuracy \
  --predictions /private/path/real_predictions.csv \
  --checkpoint-sha256 REAL_CHECKPOINT_SHA256 \
  --checkpoint /private/path/matching_checkpoint.keras \
  --output /private/path/evaluation_output.json
```

Required CSV fields: `sample_id,sha256,ground_truth_label,label_evidence,source,dataset_version,lineage_id,split,checkpoint_sha256,prediction_score`. The auditor rejects duplicate hashes, mislabeled checkpoint identifiers, non-finite scores, lineage overlap across declared splits, and single-class test sets. It computes **descriptive** held-out metrics; it does *not* verify the legitimacy of labels or independence of an owner-declared split. The tests use synthetic fixtures only. Do not publish a claimed benchmark until externally validating sample provenance, class mapping, split assignment, threshold choice and model selection.

## Optional recovered-archive consistency audit

The original owner-held ZIPs must **not** be committed or published. Run this read-only command with your copies:

```sh
python -m research.recovery_audit \
  --model-export '/private/path/ThreatVision-20261118T030006Z-1-001.zip' \
  --notebooks-export '/private/path/Colab Notebooks-20261118T025932Z-1-001.zip' \
  --output /private/path/recovered-summary.json
```

This inspects archive CRCs, Keras archive metadata (not runtime), notebook structure, image-manifest counts and log anomalies. The sanitized reference summary is in [`docs/audits/recovered-artifact-verified-summary.json`](docs/audits/recovered-artifact-verified-summary.json). See [the crosscheck](docs/audits/RECOVERY_CROSSCHECK_2026-11-18.md) for the essential warning that a recovered 256×256 model is **not** the previously described 224×224 production model.

As of 19 November 2026, the complete research suite reports **38 passed, 0 failed** in the existing `/opt/miniconda3/envs/threatvision` environment (Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1, NumPy 1.26.4). Conda base has TensorFlow 2.21.0 and NumPy 2.4.4 but lacks Matplotlib required by the evaluation smoke test. Both checkpoints have been safely loaded and run under their separate registered identities. The one-epoch training smoke also passed using temporary synthetic PE-shaped fixtures with pseudo-labels explicitly marked as non-ground-truth; the generated metrics are not a scientific result. No genuine malware-benchmark result was performed.

## Synthetic checkpoint verification

The shape-aware verifier accepts only archives with a supported grayscale input at 224×224 or 256×256 and an actual one-unit Dense sigmoid output layer. It validates the exact SHA-256 registered to the explicit profile before loading saved weights safely. It probes zero, constant, gradient, seeded-noise and harmless PE-derived tensors using that profile. `production-224-v1` uses `[0,1]`, matching the serving caller; `recovered-256-v1` uses `[0,255]` for the separate recovered model. The PE-derived 256 input is clearly marked as a resized engineering probe, not a historical preprocessing reconstruction. The JSON records timing, software versions, checkpoint and fixture/tensor hashes, outputs, and repeatability. Synthetic probes establish load/forward-pass behavior only. Tests reject unregistered checkpoint identities, a misleading archive with an intermediate sigmoid, and a linear output.

python -m research.verify_model "/path/to/ThreatVision Final/backend/python_scripts/model/threatvision_v01.keras" --sha256 1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca --profile production-224-v1 --output docs/audits/production-checkpoint-verification.json

The production and recovered checkpoint commands have passed in the existing `/opt/miniconda3/envs/threatvision` environment. The production parity runner also used this environment. An earlier production probe used Conda base (Python 3.13.9, Keras 3.14.1, TensorFlow 2.21.0, NumPy 2.4.4); `requirements-model-verify.txt` records that alternate verifier environment. Scores should not be expected to match across these TensorFlow builds.

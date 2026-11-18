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

The original numerical preprocessing functions were extracted from the application. The original source checksum is in [checkpoint metadata](docs/audits/checkpoint-metadata.json). There is no padding or truncation in that implementation. Arbitrary bytes can be transformed without becoming valid PE research samples. Runtime parity with the source must be checked after any future changes to either implementation.

An optional runtime checkpoint probe requires a compatible TensorFlow installation.

```sh
python -m research.checkpoint /path/to/threatvision_v01.keras
```

This uses synthetic bytes only and prints repeat-run outputs explicitly as engineering probes. TensorFlow is not in the lightweight test dependencies. Its compatible environment and original checkpoint runtime remain unverified in this pass.

Historical notebooks, an earlier 256×256 checkpoint, and a 22-row training log have been recovered; however, exact training-to-checkpoint linkage, original PE/PNG samples, split membership, and the 224×224 deployed checkpoint bytes are still missing from the reviewed recovery exports. No command can currently reproduce a verified historical checkpoint training run. Training, extraction, source/temporal holdouts and group uncertainty modules are implemented but have not been verified end to end with TensorFlow and an authorized cohort. An evaluation smoke test uses minimal synthetic headers and invented scores, deletes its temporary results, and checks runner integration only. Do not treat the runner as validated scientific evidence.

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

As of the 18 November 2026 follow-up, **21 safe unit tests passed** (14 earlier tests plus seven synthetic historical-accuracy-audit tests). No TensorFlow inference or genuine malware-benchmark run was performed as part of this reconciliation.

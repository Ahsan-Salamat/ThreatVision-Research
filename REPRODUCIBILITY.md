# Research tooling

Run from the repository root with Python 3.11 or later.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-research.txt
python -m unittest discover -s tests -v
python -m research.validate /path/to/manifest.csv /path/to/authorized-data
python -m research.evaluate --manifest /path/to/manifest.csv --data-root /path/to/authorized-data --features /path/to/features.csv --model-id CHECKPOINT_SHA256 --output results/new-run
```

The unit tests use harmless bytes and headers. The evaluator expects one row per manifest sample with numeric `static_*` columns and a frozen `neural_score`. It fits scaling and logistic regression on the training partition only. Neural-only, static logistic and combined logistic comparisons share the test samples. The combined estimator is a proposed research baseline and differs from the application's heuristic fusion. Threshold 0.5 is fixed in advance. Metrics JSON and ROC SVG are written to a new output directory.

The manifest requires sample_id, sha256, ground_truth_label, source, label_evidence, file_format, split, dataset_version, lineage_id and relative path. Optional columns include malware_family and collection_date. Empty provenance fields fail validation. A recorded evidence string still requires independent verification by the dataset owner. The validator checks header signatures, sizes, hashes, duplicate IDs and hashes, both classes in each split, and supplied lineage/family separation. It does not establish label correctness or detect unknown relationships. PE header validation does not establish that a file is loadable or harmless.

The original numerical preprocessing functions were extracted from the application. The source checksum is in [checkpoint metadata](docs/audits/checkpoint-metadata.json). There is no padding or truncation in that implementation. Arbitrary bytes can be transformed without becoming valid PE research samples. Runtime parity with the source must be checked after any future changes to either implementation.

An optional runtime checkpoint probe requires a compatible TensorFlow installation.

```sh
python -m research.checkpoint /path/to/threatvision_v01.keras
```

This uses synthetic bytes only and prints repeat-run outputs explicitly as engineering probes. TensorFlow is not in the lightweight test dependencies. Its compatible environment and original checkpoint runtime remain unverified in this pass.

Historical training data and the original training program have not been recovered. No command to reproduce historical training can currently be supplied. A new architecture training implementation, automated feature extraction, source/temporal holdouts, group uncertainty intervals, remain incomplete. An evaluation smoke test uses minimal synthetic headers and invented scores, deletes its temporary results, and checks runner integration only. Do not treat the runner as validated scientific evidence.

Use the existing [dataset provenance](docs/dataset-provenance.md), [model card](docs/model-card.md), [experimental record](docs/experimental-record.md), and [limitations](docs/findings-and-limitations.md) as the scientific record.

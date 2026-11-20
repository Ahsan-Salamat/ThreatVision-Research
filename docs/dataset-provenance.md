# Dataset provenance and governance

## Production checkpoint

The available record does not identify the training dataset for the 224×224 production checkpoint. Its collection dates, license, label sources, sample hashes, duplicate policy, lineage groups and train/validation/test assignments are unknown. Recovered notebooks and manifests describe separate historical workflows and are not attributable to this checkpoint; see the [experiment lineage register](experiment-lineage.md). It is not established that the checkpoint used MaleX.

## Recovered manifests and diagnostic pilot

A recovered 4,000-row image manifest contains balanced label strings and distinct hash-shaped values, but the associated images, original PE files and label evidence were not included. A separate notebook reports a much larger image-folder inventory without a complete verified run. These records do not constitute an accessible or independently labeled benchmark.

The 46-row diagnostic pilot has no known-malicious PE cohort, independently verified labels or complete source manifest. Its sample-level inputs and measurements are excluded from this repository pending confirmation of redistribution terms. The [experimental record](experimental-record.md) describes the available aggregate observations and their limits.

## Requirements for future evaluation

Before performance evaluation, record the dataset version, lawful acquisition source and terms, collection window, label source and confidence, PE/file-format policy, exact and near-duplicate handling, family or lineage groups, and immutable split assignments. Define how packed, signed, benign-software and source/time strata will be represented. Fit scaling, feature selection and thresholds on training/validation data only. Reserve the test partition for the preregistered final comparison and preserve per-sample checkpoint and preprocessing provenance.

Keep executable samples in an appropriately controlled environment. Do not publish raw malware binaries, credentials, private datasets or source material without rights and safety review. Public benchmark names and feature-only releases do not imply that raw files are available for this byte-to-image pipeline.

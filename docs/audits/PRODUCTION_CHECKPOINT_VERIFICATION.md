# Production checkpoint verification

**Execution date:** 19 November 2026

**Result:** **PASS — safe loading and synthetic inference only.** No malware accuracy claim.

## Production 224×224 checkpoint

The companion application's `threatvision_v01.keras` was verified with SHA-256 `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca`. The archive was safely loaded with `compile=False, safe_mode=True` in the existing Apple Silicon `threatvision` environment: Python 3.11.15, TensorFlow 2.16.1, Keras 3.14.1 and NumPy 1.26.4. The model declares `(None,224,224,1)` input, `(None,1)` output and 2,422,084 parameters, with a one-unit sigmoid output.

The verifier checks the exact registered checkpoint hash before loading, confirms the serialized and loaded shapes, and runs five deterministic synthetic tensors plus one PE-derived tensor built from the harmless local fixture. All six outputs were finite, in `[0,1]`, and repeated exactly at absolute tolerance `1e-7` (maximum repeat delta **0.0**). The PE fixture and final model tensor hashes are recorded in the JSON. The PE bytes were not executed.

| Synthetic probe | Output | Repeat delta |
| --- | ---: | ---: |
| Zeros | 0.441406250 | 0 |
| Constant 0.5 | 0.410888672 | 0 |
| Ones | 0.668945312 | 0 |
| Gradient 0–1 | 0.833007812 | 0 |
| Seeded random [0,1] | 0.819335938 | 0 |
| Harmless PE through current preprocessing | 0.413574219 | 0 |

These values are runtime probes, not probabilities, accuracy evidence, calibration evidence or a stable performance benchmark. An earlier run under TensorFlow 2.21.0 produced different synthetic values from this TensorFlow 2.16.1 run; cross-runtime numeric equivalence is not established.

## Separate recovered 256×256 checkpoint

The recovered `best_model.keras` is a distinct artifact, SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`. It declares `(None,256,256,1)` input, `(None,1)` output and 2,422,084 parameters. It was also safely loaded in the same runtime under the separate `recovered-256-v1` profile, using its own `[0,255]` synthetic tensor contract. Its five generic probes and one engineering-only PE-derived probe were finite and exactly repeatable at `1e-7` tolerance. The PE-derived input was formed by resizing the current production representation to 256×256 and scaling back to `[0,255]`; this is explicitly **not** a reconstruction of its historical training preprocessing.

The checkpoints differ in input size and serialized preprocessing placement. Their hashes, output probes and layer summaries are kept separate in [`production-checkpoint-verification.json`](production-checkpoint-verification.json) and [`recovered-256-checkpoint-verification.json`](recovered-256-checkpoint-verification.json). Neither archive is included in this public research repository.

## Reproduction

Run from the research repository root with the existing `threatvision` environment:

```bash
KERAS_BACKEND=tensorflow python -m research.verify_model /path/to/threatvision_v01.keras \
  --sha256 1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca \
  --profile production-224-v1 \
  --output docs/audits/production-checkpoint-verification.json
```

Use profile `recovered-256-v1` and its registered SHA-256 only for the separate recovered checkpoint. The CLI requires a profile, verifies that the hash matches the registered identity, validates the archive's output layer, and fails nonzero if shape, output range, finiteness or repeatability checks fail. It records runtime/package versions and a sanitized display-path label instead of a private filesystem path.

## What this verifies

- Exact checkpoint-byte identity for each registered model.
- Safe archive deserialization and successful forward passes using the saved weights.
- The declared image dimensions, scalar output shape, finite sigmoid-range scores and within-run repeatability.
- Production preprocessing parity and neural output parity across the application and research implementations for three deterministic harmless fixtures; see the [stage-by-stage parity record](PRODUCTION_PREPROCESSING_PARITY.md).

It does **not** verify training history, training-data identity, label validity, split integrity, TensorFlow cross-version equivalence, calibration, accuracy, AUC, recall, false-positive rate, generalization or the historical approximately 85% recollection. No malware files were loaded or executed.

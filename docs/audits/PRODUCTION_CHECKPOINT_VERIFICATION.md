# Production checkpoint verification

**Date:** 18 November 2026  
**Artifact:** companion application's `backend/python_scripts/model/threatvision_v01.keras`  
**Result:** **PASS — safe load and synthetic forward pass only.** No malware accuracy claim.

## Artifact and architecture

- Size: 34,515,982 bytes; ZIP CRC validation passed.
- SHA-256: `1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca` (matches the expected identity).
- Keras archive metadata: Keras 3.14.1, saved `2026-05-15@10:37:36`.
- Model: Functional `malware_classifier`; input `(None,224,224,1)`; output `(None,1)`; **2,422,084** parameters; one sigmoid Dense output.
- Top-level topology: Input → RandomFlip → RandomRotation → grayscale-to-RGB Conv2D → Rescaling → MobileNetV2 → global average pooling → dropout → Dense(128, ReLU) → dropout → Dense(1, sigmoid).
- `compile=False`, `safe_mode=True` load succeeded. All five outputs were finite and in `[0,1]`; all five repeated calls had maximum absolute delta `0.0` at tolerance `1e-7`.

Full machine-readable details are in [`production-checkpoint-verification.json`](production-checkpoint-verification.json). The saved Keras configuration exposes a sigmoid score, but does not establish that the score is calibrated as a probability.

## Runtime and synthetic probes

The latest reproducible run used the existing Apple Silicon `threatvision` Conda environment, without installing or changing dependencies: Python 3.11.15, Keras 3.14.1, TensorFlow 2.16.1, NumPy 1.26.4, backend `tensorflow`. TensorFlow reported CPU and Metal devices in the JSON evidence. The effective model input contract is float32 NHWC, `(1,224,224,1)`, grayscale pixel values normalized to `[0,1]`, matching the application caller's cast-and-divide-by-255 step.

| Synthetic input | Output | First-call time | Repeat delta |
| --- | ---: | ---: | ---: |
| zeros | 0.441406250 | 1029.661 ms | 0 |
| constant 0.5 | 0.410888672 | 308.122 ms | 0 |
| ones | 0.668945312 | 340.379 ms | 0 |
| gradient 0–1 | 0.833007812 | 311.114 ms | 0 |
| seeded random [0,1] | 0.819335938 | 306.690 ms | 0 |

Times are single local observations, not a controlled latency benchmark. Inputs are synthetic and do not establish classification performance, calibration, training provenance, or generalization. An earlier successful run under Python 3.13.9 / TensorFlow 2.21.0 produced different synthetic scores for the same checkpoint; repeated calls were identical within each runtime. Cross-runtime numeric equivalence is therefore **not established**. Do not interpret these probe values as probabilities or a stable model benchmark.

## Recovered 256×256 checkpoint

The separate archived `best_model.keras` was copied from the user-provided Drive ZIP into a temporary directory and verified without modifying the archive. SHA-256 `62feb539c30edb4b2849ac760d9b9e41c8842da000e9bfc9c653b08861173102`; 11,599,393 bytes; Keras 3.13.2 metadata; input `(None,256,256,1)`; 2,422,084 parameters. It loaded under the same Python 3.11.15 / TensorFlow 2.16.1 runtime and passed finite-output, shape, and repeatability probes. Its explicit `recovered-256-v1` probe uses float32 `[0,255]` values to match the supplied verification script's historical probes. See [`recovered-256-checkpoint-verification.json`](recovered-256-checkpoint-verification.json). It remains a separate checkpoint with no proven link to the production weights.

The user-supplied `verify_recovered_model.py` was also executed unchanged against that temporary 256×256 checkpoint copy with `KERAS_BACKEND=tensorflow` (the existing environment has no PyTorch). It passed all five probes with zero repeat deltas. It was **not** pointed at the 224×224 production checkpoint because its synthetic tensors are hard-coded to 256×256; the separate shape-aware verifier was used for the production artifact.

## Application preprocessing compatibility

The companion application's classifier converts its generated DCT image to grayscale, resizes to 224×224, casts to float32, divides by 255, and adds batch/channel axes. That caller tensor matches the verified profile. The generated image itself is produced by the application's 256×256 overlapping byte-pair matrix, suppression of `(0,0)`, division by the maximum remaining bigram count, uint8 quantization, orthonormal 2D DCT-II, `log1p(abs(DCT))`, max rescaling to uint8, and area resize to 224×224. Three deterministic synthetic fixtures were then run through both the application's production converter functions and `research.preprocessing.tensor`; all resulting normalized tensors were exactly equal (`max_abs_delta=0`). Their production-image SHA-256 values are recorded in the implementation report.

The model also contains `Rescaling(scale=2.0, offset=-1.0)` **after** the learned grayscale-to-RGB convolution. The application supplies `[0,1]` grayscale pixels, so this internal layer maps the adapter output toward `[-1,1]`. Do not add another external `[-1,1]` rescaling or move this layer: that would change the saved model contract.

## Application integration

The local Node classifier service and HTTP endpoint were exercised with a generated harmless PE fixture. The actual Stage 0 static analyzer, Stage 1 DCT converter, Stage 2 production checkpoint inference, and Stage 3 fusion scorer completed. The result exposed the neural score separately from static evidence and identified it as uncalibrated. The static label remained authoritative, while the bounded neural score nudge was recorded separately. This is a safe integration smoke test only; the fixture has no malware label and contributes no performance evidence. Upload tests also covered absent input, unsupported extension, forged PE magic, empty/oversized input, auth rejection, fail-closed behavior when auth is unconfigured, explicit local-only bypass, simulated fallback with no neural score in the API response, conversion failure, and subprocess timeout behavior. Simulated inference indicators are excluded from the static result. No uploaded binary was executed.

## Reproduction

From the research repository root, in a compatible Keras 3/TensorFlow 2 environment:

```bash
python -m research.verify_model \
  "/path/to/ThreatVision Final/backend/python_scripts/model/threatvision_v01.keras" \
  --sha256 1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca \
  --profile production-224-v1 \
  --display-path "ThreatVision Final/backend/python_scripts/model/threatvision_v01.keras" \
  --output docs/audits/production-checkpoint-verification.json
```

The research verifier checks the hash and serialized shape before loading, uses safe deserialization, probes harmless synthetic tensors, validates output shape/range/finiteness, and records repeated-call deltas, timings and runtime versions. The production model passed this run. A separate [`recovered-256-v1` result](recovered-256-checkpoint-verification.json) records the recovered checkpoint's `[0,255]` synthetic probe contract; it is not interchangeable with this production profile.

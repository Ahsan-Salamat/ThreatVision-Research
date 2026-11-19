# Production preprocessing parity record

**Execution date:** 19 November 2026  
**Result:** **PASS for current application-to-research implementation parity.** This does not establish historical training parity or malware-detection performance.

## Scope and method

The companion application's `backend/python_scripts/convert_to_bigram_dct.py` and `research/preprocessing.py` were run on the same three deterministic, harmless byte fixtures: a locally generated minimal PE fixture, a repeated byte range, and a boundary-pair pattern. The generated PE contains a harmless `RET` byte but was never executed.

For each fixture, the comparison records SHA-256 values, shape, dtype, and maximum absolute difference for the byte stream, overlapping bigram counts, the matrix after suppressing `(0,0)`, max-normalized counts, uint8 grayscale quantization, the normalized DCT output, 224×224 resized image, and final float32 NHWC model tensor. Each stage matched exactly across all three fixtures. The maximum absolute difference was **0.0** at every stage.

The production checkpoint was also loaded with `compile=False, safe_mode=True` after checking its registered SHA-256. The application-built and research-built model inputs were each passed through that same real checkpoint for all three fixtures. All corresponding outputs were identical (maximum absolute difference **0.0**) and finite. Their meaning remains an **uncalibrated sigmoid score**; these harmless fixtures do not measure classifier performance.

The detailed per-fixture and per-stage evidence, including both implementation hashes, checkpoint hash, fixture hashes, tensor hashes and synthetic model outputs, is in [`production-preprocessing-parity.json`](production-preprocessing-parity.json).

## Reproduction

From the research repository root, using the existing `threatvision` environment:

```bash
KERAS_BACKEND=tensorflow python -m research.preprocessing_parity \
  --checkpoint /path/to/threatvision_v01.keras \
  --checkpoint-sha256 1e8f713db5aa0e42bb55addb02281a700028fc9fbca784b908c77a1b9cf6aaca \
  --output docs/audits/production-preprocessing-parity.json
```

The companion converter path defaults to the sibling application checkout. Use `--converter` if it is elsewhere. The script checks the checkpoint hash before loading it and only processes generated harmless fixtures.

## Preprocessing contract and limits

The current serving path counts overlapping adjacent byte pairs in a 256×256 matrix, suppresses the zero-byte pair `(0,0)`, divides remaining counts by their maximum, converts to uint8, applies an orthonormal 2D DCT-II, log-compresses coefficient magnitudes with `log1p`, rescales to uint8, and resizes to 224×224. The model caller converts that image to float32, divides by 255, and adds batch and channel axes. The saved model then applies a learned grayscale-to-three-channel convolution followed by `Rescaling(scale=2, offset=-1)`. No extra external normalization is applied.

The separate recovered checkpoint expects 256×256 float32 values in `[0,255]`. Its engineering-only PE probe resizes the current 224×224 representation to 256×256 and rescales it to `[0,255]`; this does **not** reconstruct its historical training pipeline. A recovered notebook describes a different placement of scaling relative to the learned channel adapter. The exact training-time preprocessing for either checkpoint remains unverified.

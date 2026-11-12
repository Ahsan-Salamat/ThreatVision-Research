# Methodology

## Scope and attribution

ThreatVision uses an established byte-bigram and frequency-domain representation described by Mohammed et al. (2021) [5]. The project implements and integrates this method; it does not claim it as original. This document separates the implemented preprocessing steps from the scientific hypotheses that remain to be tested.

## Byte-pair frequency matrix

Represent an input file as ordered bytes `B=(b₁,b₂,…,bₙ)`, where `bᵢ ∈ {0,…,255}` and `n ≥ 2`. The implementation counts adjacent pairs:

`M(u,v) = Σᵢ₌₁ⁿ⁻¹ 𝟙(bᵢ = u ∧ bᵢ₊₁ = v)`, for `u,v ∈ {0,…,255}`.

This gives `M ∈ ℝ²⁵⁶ˣ²⁵⁶`. The matrix records transition frequencies; it is not described as a conditional-probability transition matrix because the implementation does not row-normalize the counts.

## Null suppression, normalization, and quantization

The implementation sets `M(0,0)=0` to suppress a repeated-null pattern associated with PE alignment padding. This is an engineering heuristic, not a general property of every file. It may also remove genuine transitions and should be isolated by ablation.

If `max(M)>0`, the counts are divided by their maximum and quantized:

`Mₙₒᵣₘ(u,v)=M(u,v)/maxₓ,ᵧ M(x,y)`

`G(u,v)=floor(255 · Mₙₒᵣₘ(u,v))`.

`G` is an 8-bit grayscale matrix of shape 256 × 256.

## Orthonormal 2D DCT-II and compression

The transformation uses a two-pass orthonormal 2D DCT-II. For indices `p,q ∈ {0,…,255}`:

`F(p,q)=α(p)α(q) Σₓ₌₀²⁵⁵ Σᵧ₌₀²⁵⁵ G(x,y) cos[π(2x+1)p/512] cos[π(2y+1)q/512]`,

where `α(0)=√(1/256)` and `α(k)=√(2/256)` for `k>0`. The implementation applies the transform sequentially along each dimension. It maps coefficient magnitudes using `D(p,q)=log(1+|F(p,q)|)`, rescales the result to 8-bit grayscale, and resamples the 256 × 256 image to 224 × 224 with area interpolation. This produces the model's single-channel input tensor, normalized to `[0,1]`.

## Static analysis and model input

The separate static-analysis path extracts PE headers and sections, imports, section and global entropy, strings, hashes, and selected opcode features. The neural model receives only the transformed image. It does not receive the static features as a learned fused tensor; fusion occurs later in the heuristic scorer.

The sigmoid output is reported as a neural score, not a calibrated probability. Static-analysis criteria determine the final malware/benign label; neural inference can adjust the numeric threat score by at most five points. The rule weights and thresholds have not been calibrated against an independent labeled evaluation set.

## Interpretation limits

The frequency image does not directly encode program intent. Packing, compression, padding, file format, and source distribution can influence byte patterns. Prior work has shown that static malware classifiers can learn packer-related signals that do not generalize to unseen packers [2]. The available pilot shows different score changes for overlays on two source files, but each overlay changes multiple properties. Whether this model uses entropy or another shortcut remains untested. A controlled evaluation is proposed in [Future research](future-research.md).

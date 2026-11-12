# System Architecture

## Application overview

ThreatVision uses a React 18/Vite/Tailwind client, a Node.js/Express API, and Python analysis scripts. The web client submits a file to the API. The server validates selected magic bytes, assigns a scan job, and invokes Python processing stages. The client presents the scan dossier and can store scan metadata in Supabase PostgreSQL.

## Processing workflow

1. **Upload guard:** checks recognized signatures such as `MZ`, `%PDF`, or `PK`.
2. **Static analysis:** parses PE headers and sections, extracts imports, calculates entropy, searches strings, calculates hashes, and disassembles selected `.text` content for heuristic opcode indicators.
3. **Preprocessing:** counts adjacent bytes into a 256 × 256 bigram matrix, suppresses `(0,0)`, normalizes and quantizes it, applies 2D DCT-II and log-magnitude compression, and resamples the image.
4. **Neural inference:** sends a 224 × 224 grayscale spectrogram to the deployed MobileNetV2-based Keras artifact and records a scalar output.
5. **Fusion:** weights static indicators, applies the bounded neural score adjustment, and determines the final label from static criteria.
6. **Reporting:** returns a dossier containing the label, risk score, indicators, hashes, static-analysis details, and generated feature image; the frontend may persist metadata to Supabase.

The implementation trace gives this sequence. It is described sequentially here rather than as a concurrent workflow.

## Decision logic

Documented static component weights are dangerous imports (0.40), entropy (0.20), PE anomalies (0.20), strings (0.10), and opcode patterns (0.03), normalized over static inputs. The CNN has zero weight in the final classification rule. It can adjust the numerical threat score by a maximum of five points. Static conditions and a benign score floor control the binary verdict. These are project rules, not independently calibrated decision thresholds.

## Reporting interface and non-implemented features

The dashboard presents threat indicators, scan metadata, and the DCT image. A radial-gradient overlay shown in the UI is illustrative only; it is not computed from neural gradients. The family labels are heuristic profiles derived from static properties, not learned multi-class predictions. These features are not described as scientifically validated explanations or attribution.

## Operational and publication boundary

The application stores temporary scan artifacts in per-job folders and schedules their cleanup. Supabase holds scan metadata. This repository includes documentation and approved figure assets only; it excludes application source, model weights, malware binaries, private data, credentials, and internal audit documents. See the public file allowlist at the repository root.

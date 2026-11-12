# System Architecture

## Application overview

ThreatVision uses a React 18/Vite/Tailwind client, a Node.js/Express API, and Python analysis scripts. The client submits a file to the API. The server checks selected file signatures, assigns a scan job, and invokes Python processing stages. The client presents a scan dossier and can store scan metadata in Supabase PostgreSQL.

## Processing workflow

1. **Upload guard:** checks signatures such as `MZ`, `%PDF`, or `PK`.
2. **Static analysis:** parses PE headers and sections, extracts imports, calculates entropy, searches strings, calculates hashes, and disassembles selected `.text` content for heuristic opcode indicators.
3. **Preprocessing:** counts adjacent bytes in a 256 × 256 bigram matrix, suppresses `(0,0)`, normalizes and quantizes the matrix, applies a 2D DCT-II and log-magnitude compression, and resamples the image.
4. **Neural inference:** sends the transformed 224 × 224 grayscale image to the deployed MobileNetV2-based Keras artifact and records a scalar score.
5. **Fusion:** weights static indicators, applies the bounded CNN score adjustment, and determines the final label from static criteria.
6. **Reporting:** returns a dossier containing the label, threat score, indicators, hashes, static-analysis details, and feature image; the frontend may persist metadata to Supabase.

The documented execution order is sequential. The upload path can accept non-PE files, but the static scorer is PE-focused and the CNN's intended domain is Windows PE triage. PDF and random-byte probes described elsewhere are outside that intended domain.

## Decision logic

Documented static component weights are dangerous imports (0.40), entropy (0.20), PE anomalies (0.20), strings (0.10), and opcode patterns (0.03), normalized over static inputs. The CNN has no authority in the final classification rule and can adjust the numeric threat score by at most five points. Static conditions and a benign score floor control the binary verdict. These are project rules, not independently calibrated thresholds.

## Reporting interface and illustrative elements

The dashboard presents threat indicators, scan metadata, and the DCT image. Its radial-gradient overlay is illustrative; it is not computed from neural gradients. Family labels are heuristic profiles derived from static properties, not learned multi-class predictions.

## Repository contents

This public repository contains written documentation and two illustrative feature images. It does not contain the application source, model weights, malware binaries, private datasets, or credentials. Redistribution rights for the two feature images remain to be confirmed.

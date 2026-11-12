# Figures

Figures 1–5 describe the implemented workflow; Figure 6 presents proposed research. Figures 1–6 are Mermaid diagrams authored for this repository. The two PNGs in `assets/` are illustrative feature images from the project materials, not performance charts or labeled evaluation examples. Their redistribution rights have not been confirmed.

## Figure 1. System architecture

```mermaid
flowchart LR
    A[Submitted file] --> B[Magic-byte upload filter]
    B --> C[Node.js and Express orchestrator]
    C --> D[Static PE analysis]
    D --> E[Byte-pair matrix and DCT-II]
    E --> F[MobileNetV2 inference]
    F --> G[Heuristic scorer]
    D --> G
    G --> H[Threat score and risk tier]
    G --> I[Static-authoritative final label]
    H --> J[React analyst dashboard]
    I --> J
```

*Caption: The application runs upload validation, static analysis, and the visual inference path before fusion. Static criteria determine the final binary label; the CNN can change the numeric score by no more than five points.*

## Figure 2. Binary preprocessing and frequency transformation

```mermaid
flowchart TD
    A[Raw byte sequence with at least two bytes] --> B[Count adjacent byte pairs]
    B --> C[256 x 256 frequency matrix M]
    C --> D[Suppress null-byte pair count]
    D --> E[Normalize by maximum and quantize to G]
    E --> F[Orthonormal 2D DCT-II]
    F --> G[Log-magnitude compression]
    G --> H[Rescale to 8-bit image]
    H --> I[Area resampling to 224 x 224]
    I --> J[Normalize and add channel dimension]
```

*Caption: Implemented byte-to-image process. Suppressing `(0,0)` is an engineering heuristic; its contribution has not been tested by an ablation.*

## Figure 3. Deployed neural model architecture

```mermaid
flowchart TD
    A[224 x 224 x 1 input] --> B[Training-time flip and rotation layers]
    B --> C[Learned 1 x 1 grayscale-to-RGB adapter]
    C --> D[Rescale 0..1 to -1..1]
    D --> E[ImageNet MobileNetV2 backbone]
    E --> F[Global average pooling: 1280]
    F --> G[Dropout 0.4]
    G --> H[Dense 128, ReLU]
    H --> I[Dropout 0.2]
    I --> J[Dense 1, sigmoid]
    J --> K[Advisory malware score]
```

*Caption: Topology recorded for `threatvision_v01.keras`. The checkpoint and its weights are not distributed here; the diagram makes no performance claim.*

## Figure 4. Static analysis and neural-advisory scoring

```mermaid
flowchart LR
    A[Imports, entropy, PE anomalies, strings, opcodes] --> B[Weighted static score]
    A --> C[Static decision criteria]
    D[DCT spectrogram] --> E[MobileNetV2 score]
    B --> F[0-100 threat score]
    E -->|at most +/- 5 points| F
    C --> G[Final malware or benign label]
    F --> H[Risk tier]
    G --> I[Scan dossier]
    H --> I
```

*Caption: Static criteria control the binary label. CNN inference can nudge the numeric score but cannot override that label.*

## Figure 5. End-to-end inference and reporting workflow

```mermaid
sequenceDiagram
    actor Analyst
    participant UI as React client
    participant API as Express API
    participant Static as Static PE stage
    participant Vision as DCT and MobileNetV2 stages
    participant Fuse as Fusion scorer
    participant DB as Supabase metadata store
    Analyst->>UI: Submit file
    UI->>API: Multipart upload
    API->>API: Validate signature and assign job
    API->>Static: Extract PE indicators
    Static-->>API: Static evidence
    API->>Vision: Transform bytes and run inference
    Vision-->>API: Feature image and CNN score
    API->>Fuse: Apply static rules and bounded score nudge
    Fuse-->>API: Final label and threat score
    API-->>UI: Return scan dossier
    UI->>DB: Persist scan metadata
    UI-->>Analyst: Display findings
```

*Caption: Sequential workflow as documented for the application. It does not imply concurrent analysis branches or validated detection performance.*

## Figure 6. Proposed research process

```mermaid
flowchart TD
    A[Lawful datasets with documented provenance] --> B[Review labels and deduplicate]
    B --> C[Group by family, source, and time]
    C --> D[Freeze time-aware partitions]
    D --> E[Control entropy, packing, and file format]
    E --> F[Compare static, image, byte, and hybrid baselines]
    F --> G[Ablate transforms and signal groups]
    G --> H[Pre-register metrics and thresholds]
    H --> I[Report calibration, intervals, and subgroup errors]
    I --> J[Assess robustness and explanation stability]
    J --> K[Publish safe metadata and reproducibility materials]
```

*Caption: Proposed study design only. None of these experiments has been completed or validated for ThreatVision.*

## Illustrative feature images

The following project images show feature appearance only. They are not labeled malware/benign examples and do not show model outputs or performance. Redistribution permission for these images has not been confirmed.

![Illustrative high-entropy feature image; no class label or model result is implied.](../assets/high-entropy-example.png)

*Caption: Example feature image identified in the project materials as high entropy. The caption does not imply a malware label or a model score.*

![Illustrative structured feature image; no class label or model result is implied.](../assets/structured-example.png)

*Caption: Example structured feature image from the project materials. The caption does not imply a malware label or a model score.*

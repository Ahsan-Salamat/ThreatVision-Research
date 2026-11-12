# Scientific Figures

The Mermaid source below is intended to render on GitHub. Figures 1–5 describe the audited implementation; Figure 6 is explicitly proposed research. The example spectrograms in `assets/` are feature outputs supplied in the project handoff. They are illustrative inputs only and are not labeled model-performance examples. Confirm rights and captions before public release.

## Figure 1. System architecture

```mermaid
flowchart LR
    A[Submitted file] --> B[Magic-byte upload filter]
    B --> C[Node.js and Express orchestrator]
    C --> D[Static PE analysis]
    D --> E[Byte-pair matrix and DCT-II]
    E --> F[MobileNetV2 inference]
    F --> G[Multi-signal scorer]
    G --> H[Threat score and risk tier]
    G --> I[Static-authoritative final label]
    H --> J[React analyst dashboard]
    I --> J
```

*Caption: Audited application stages as listed by the implementation trace. The final binary label comes from static criteria; neural inference provides a bounded score adjustment.*

## Figure 2. Binary preprocessing and frequency transformation

```mermaid
flowchart TD
    A[Raw bytes b1 ... bn, n >= 2] --> B[Count adjacent byte pairs]
    B --> C[256 x 256 frequency matrix M]
    C --> D[Suppress M(0,0)]
    D --> E[Normalize by maximum and quantize to G]
    E --> F[Orthonormal 2D DCT-II]
    F --> G[Log magnitude: log(1 + abs(F))]
    G --> H[Rescale to 8-bit image]
    H --> I[Area resampling to 224 x 224]
    I --> J[Normalize and add channel dimension]
```

*Caption: Implemented byte-to-image process. Null suppression is a heuristic and should be evaluated by ablation.*

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

*Caption: Topology recorded for `threatvision_v01.keras`. This figure makes no performance claim.*

## Figure 4. Static analysis and neural-advisory scoring

```mermaid
flowchart LR
    A[Imports, entropy, PE anomalies, strings, opcodes] --> B[Weighted static score]
    A --> C[Static decision criteria]
    D[DCT spectrogram] --> E[MobileNetV2 probability]
    B --> F[0-100 threat score]
    E -->|at most +/- 5 points| F
    C --> G[Final malware or benign label]
    F --> H[Risk tier]
    G --> I[Scan dossier]
    H --> I
```

*Caption: Static criteria have full label authority. The CNN does not determine the final malware/benign verdict.*

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
    API->>API: Validate magic bytes and assign job
    API->>Static: Parse PE and extract static indicators
    Static-->>API: Static evidence JSON
    API->>Vision: Transform bytes and run inference
    Vision-->>API: Spectrogram and advisory score
    API->>Fuse: Apply static rules and bounded score nudge
    Fuse-->>API: Final label and threat score
    API-->>UI: Return scan dossier
    UI->>DB: Persist scan metadata
    UI-->>Analyst: Display findings
```

*Caption: Sequential workflow described in the implementation trace; the diagram does not imply concurrent branches.*

## Figure 6. Proposed research process

```mermaid
flowchart TD
    A[Lawful datasets with documented provenance] --> B[Audit labels and deduplicate]
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

*Caption: Proposed methodology only. ThreatVision has not completed these experiments.*

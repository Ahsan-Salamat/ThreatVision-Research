# Figures

Figures 1–5 describe the implemented workflow; Figure 6 presents proposed research. All six Mermaid diagrams were authored for this repository. The README also embeds four SVG figures; no application screenshot is included.

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
    A[224 x 224 x 1 input] --> B[Flip and rotation layers]
    B --> C[Learned 1 x 1 grayscale-to-RGB adapter]
    C --> D[Affine rescaling: 2x minus 1]
    D --> E[MobileNetV2 backbone]
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
    A[Recover checkpoint and preprocessing provenance] --> B[Verify a simple statistical baseline]
    B --> C[Run paired controlled perturbations]
    C --> D[Compare raw bigram and DCT representations]
    D --> E[Evaluate static-only and combined systems on shared splits]
    E --> F[Report operating-point intervals and subgroup errors]
    F --> G{Are current lawful data suitable?}
    G -->|Yes| H[Continue controlled evaluation]
    G -->|No| I[Plan data reconstruction with documented rights]
```

*Caption: Proposed study design only. None of these experiments has been completed or validated for ThreatVision.*

## README SVG figures

The README embeds four self-contained SVG figures in `../figures/`:

1. [System overview](../figures/system-overview.svg): conceptual static and neural evidence paths with static-led labeling. Branches do not imply concurrent execution.
2. [Preprocessing explanation](../figures/preprocessing-explained.svg): synthetic byte sequence and schematic matrix example; it is not an observed feature map or inference result.
3. [Diagnostic response](../figures/diagnostic-response.svg): neural scores read from the private remediation CSV for two source files labeled benign PE and their overlay derivatives. The plot is descriptive and does not imply calibrated probabilities or independent samples.
4. [Proposed research roadmap](../figures/research-roadmap.svg): proposed steps, none represented as completed work.

No approved application-interface screenshot was found among the project assets inspected. The available logos and feature-image examples are not UI screenshots. Add a screenshot only after author approval, privacy review, and confirmation of redistribution rights.

The Mermaid diagrams above remain editable textual descriptions of the original workflow, preprocessing, model, scoring, reporting sequence, and proposed study. The README SVGs provide a compact visual rendering for the repository landing page.

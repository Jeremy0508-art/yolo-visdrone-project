# IEEE Method Design Notes

## Purpose

This document records candidate method upgrades for the IEEE Transactions route. It is deliberately separated from the manuscript: ideas here are hypotheses until verified by real experiments.

Current evidence shows that:

- 960 input resolution is the strongest source of improvement.
- YOLO11n-P2-960 is the best current nano-scale trade-off.
- YOLO11n-P2-CA-960 does not outperform YOLO11n-P2-960.
- YOLO11n-P2-TOFC-960 improves aggregate VisDrone mAP over YOLO11n-P2-960, but it is weaker on the current small-object diagnostic metrics.
- UAVDT contradicts the static P2 trend: YOLO11n-P2-960 is weaker than YOLO11n-960, YOLOv8n-960, and YOLO11s-960 under the completed 960-input setting.
- YOLO11s-960 is much stronger in absolute accuracy, so the final paper must focus on lightweight trade-offs rather than absolute superiority.

Therefore, the IEEE method cannot be built around a claim that CoordAttention or a static P2 branch is the decisive contribution. A stronger method should target the specific weakness that remains: tiny/dense object localization in the shallow high-resolution branch, while avoiding over-amplification of shallow noise when the dataset scale distribution does not favor P2.

## Baseline for New Design

The primary local baseline for new design remains:

```text
YOLO11n-P2-960
```

because it is stronger than the completed nano alternatives on VisDrone aggregate metrics:

- YOLO11n-960 on mAP50 and mAP50-95.
- YOLOv8n-960 on mAP50 and mAP50-95.
- YOLO11n-P2-CA-960 on mAP50 and mAP50-95.

However, UAVDT shows that YOLO11n-P2-960 is not a safe cross-dataset final method. Any IEEE-oriented method must compare against both YOLO11n-960 and YOLO11n-P2-960, not only against the original YOLO11n.

## Candidate A: Tiny Object Feature Calibration (TOFC)

### Motivation

The P2 branch introduces high-resolution shallow features, but shallow features also contain more background noise and weaker semantic information. A small calibration block after the P2 fusion stage may help suppress background response while preserving edge/texture cues for tiny targets.

### Possible Placement

In `configs/models/yolo11n_p2.yaml`, the P2 output is produced around the shallow head path before the four-scale `Detect` layer. Candidate placement:

```text
P2 C3k2 output -> TOFC -> Detect(P2, P3, P4, P5)
```

### Candidate Block

Lightweight block idea:

1. Depthwise 3x3 convolution for local texture/edge calibration.
2. Pointwise 1x1 convolution for channel mixing.
3. Lightweight spatial gate from average and max pooled maps.
4. Residual connection.

Expected advantage:

- Small parameter increase.
- Directly targets P2 high-resolution branch.
- Easier to explain than adding generic attention everywhere.

Risk:

- If placed only on P2, it may improve recall but hurt precision due to shallow noise.
- Needs scale-wise metrics to prove tiny/small object benefit.

Required ablations:

| Model | Purpose |
| --- | --- |
| YOLO11n-P2-960 | Direct baseline |
| YOLO11n-P2-TOFC-960 | TOFC contribution |
| YOLO11n-P2-TOFC-no-spatial-960 | Spatial gate ablation |
| YOLO11n-P2-TOFC-no-depthwise-960 | Local calibration ablation |

## Candidate B: Scale-Aware High-Resolution Fusion (SAHRF)

### Motivation

P2 improves high-resolution details, but very small objects may need both shallow spatial detail and deeper semantic context. A scale-aware fusion block can recalibrate P2 using downsampled or projected P3 information rather than treating P2 independently.

### Possible Placement

```text
P2 feature + projected P3 feature -> SAHRF -> Detect P2 branch
```

### Candidate Block

1. Project P2 and P3 to the same channel count.
2. Upsample P3 to P2 resolution.
3. Learn a lightweight fusion gate:

```text
F = alpha * P2 + (1 - alpha) * upsample(P3)
```

4. Feed fused feature to the P2 detection branch.

Expected advantage:

- More methodologically meaningful than a generic attention block.
- Directly addresses semantic weakness of shallow P2 features.

Risk:

- More invasive to Ultralytics YAML graph.
- Might increase memory and latency at 960 resolution.
- Requires careful indexing in the model YAML.

Required ablations:

| Model | Purpose |
| --- | --- |
| YOLO11n-P2-960 | Direct baseline |
| YOLO11n-P2-SAHRF-960 | Fusion contribution |
| YOLO11n-P2-SAHRF-fixed-960 | Learned gate vs fixed fusion |
| YOLO11n-P2-SAHRF-P2-only-960 | Context branch contribution |

## Candidate C: Small-Object Preserving Training Policy (SOPT)

### Motivation

The earlier SmallObjAug run improved over YOLO11n but did not beat P2/CA. Instead of treating augmentation as a final method, it can become a controlled training-policy component after deeper parameter search.

Possible changes:

- Earlier mosaic close.
- Conservative scale range.
- Reduced random erasing.
- Copy-paste tuned for small/medium boxes.
- Optional image sampling weighted by small-object density.

Expected advantage:

- No architectural risk.
- Can be combined with P2-960 or a new module.

Risk:

- Prior SmallObjAug result was not strong, so this cannot be the main innovation unless retuning shows stable gains.

Required ablations:

| Model | Purpose |
| --- | --- |
| YOLO11n-P2-960 default train | Direct baseline |
| YOLO11n-P2-960 + SOPT-v1 | Training policy gain |
| YOLO11n-P2-TOFC-960 default train | Architecture only |
| YOLO11n-P2-TOFC-960 + SOPT-v1 | Architecture + training policy interaction |

## Recommended First Implementation

Previous recommendation was Candidate A: TOFC. That run is now complete and should be treated as an aggregate-accuracy calibration ablation, not as a proven small-object method.

## Candidate D: Scale-Aware P2 Gate

### Motivation

Completed UAVDT evidence shows that a static P2 branch can hurt when the dataset does not demand the same shallow high-resolution emphasis as VisDrone. The next method should keep the useful P2 path but make the high-resolution response adaptive.

### Placement

```text
P2 C3k2 output -> ScaleAwareP2Gate -> Detect(P2, P3, P4, P5)
```

### Candidate Block

Implemented block:

1. Depthwise local context extracts shallow texture cues.
2. Channel gate estimates feature-level usefulness.
3. Spatial gate estimates local saliency.
4. A learnable bounded gain modulates the local context.
5. The gain is initialized to zero, so the block starts as identity.

Expected advantage:

- Keeps the first epoch close to the static P2 model.
- Allows P2 to adapt instead of forcing every dataset to use the same shallow detail emphasis.
- Adds only a small parameter overhead relative to YOLO11n-P2-960.

Risk:

- The identity-initialized gate may learn too little if the gradient signal is weak.
- It may improve aggregate metrics without solving the small-object diagnostic weakness.
- It still needs full VisDrone and UAVDT validation before any paper claim is allowed.

Required ablations:

| Model | Purpose |
| --- | --- |
| YOLO11n-960 | Resolution-matched baseline |
| YOLO11n-P2-960 | Static P2 baseline |
| YOLO11n-P2-ScaleGate-960 | Adaptive P2 candidate |
| YOLO11n-P2-TOFC-960 | Calibration ablation context |
| YOLO11s-960 | Capacity upper reference |

Recommended next implementation: Candidate D, ScaleAwareP2Gate.

Reason:

1. It is directly motivated by the completed UAVDT failure mode.
2. It is simple enough to implement in the current custom-module system.
3. It can be inserted after the P2 branch without redesigning the entire neck.
4. It keeps nano-scale complexity close to the existing P2-family models.

Proposed first test:

```text
YOLO11n-P2-ScaleGate-960, 100 epochs, VisDrone, seed 42
```

Then run:

```text
YOLO11n-P2-ScaleGate-960, 100 epochs, UAVDT, seed 42
```

Do not revise the IEEE abstract, conclusion, or title until both runs are complete and audited.

## Current Implementation Status

An initial TOFC implementation has been added for structural validation:

| Artifact | Status |
| --- | --- |
| `src/models/attention/tiny_object_feature_calibration.py` | Implemented |
| `src/models/register.py` registration | Implemented |
| `configs/models/yolo11n_p2_tofc.yaml` | Implemented |
| `configs/train/yolo11n_p2_tofc_960.yaml` | Implemented |
| `src/models/attention/scale_aware_p2_gate.py` | Implemented |
| `configs/models/yolo11n_p2_scalegate.yaml` | Implemented |
| `configs/train/yolo11n_p2_scalegate_960.yaml` | Implemented |
| `configs/train/yolo11n_p2_scalegate_960_uavdt.yaml` | Implemented |

Local model-build check passed without training:

| Model config | Layers | Parameters |
| --- | ---: | ---: |
| `configs/models/yolo11n_p2.yaml` | 30 | 2,893,672 |
| `configs/models/yolo11n_p2_tofc.yaml` | 31 | 2,895,762 |
| `configs/models/yolo11n_p2_scalegate.yaml` | 31 | 2,895,715 |
| `configs/models/yolo11n_p2_coordatt.yaml` | 32 | 2,903,704 |

The TOFC candidate adds about 2,090 parameters over YOLO11n-P2. The ScaleGate candidate adds about 2,043 parameters over YOLO11n-P2. These are structural results only; no ScaleGate accuracy claim is allowed until real training runs are completed.

## Acceptance Criteria

TOFC is worth continuing only as a secondary ablation unless later evidence changes the current reading. ScaleGate is worth continuing only if at least one of the following is true:

1. mAP50-95 improves over YOLO11n-P2-960 by a meaningful margin.
2. Small-object scale-wise Recall/AP improves while total mAP is not meaningfully worse.
3. UAVDT degradation relative to YOLO11n-960 is reduced compared with static YOLO11n-P2-960.
4. FPS remains close to YOLO11n-P2-960 and clearly below YOLO11s complexity.

If ScaleGate fails these gates, do not force it into the IEEE paper.

## Writing Implication

The current writing implication is no longer TOFC-centered.

TOFC has completed one VisDrone run and is useful as an aggregate-calibration
ablation, but its small-object diagnostics are weaker than YOLO11n-P2-960 and
it does not solve the UAVDT static-P2 boundary. It should therefore stay out of
the title and final contribution list unless later evidence changes the
decision protocol.

If ScaleGate passes the method-selection gates, a defensible method name can
become:

> ScaleGate-YOLO11n: Adaptive High-Resolution Prediction for Lightweight UAV
> Object Detection

If ScaleGate only improves VisDrone but not UAVDT, the paper should be framed
as a VisDrone-centered method with explicit cross-dataset limitations, or
redirected to a lower-risk venue. If ScaleGate fails the VisDrone and UAVDT
gates, do not force a module paper. Use the completed evidence to design a
second-cycle adaptive high-resolution module, such as cross-scale P2/P3
consistency or explicit scale-conditioned feature selection, and keep the
current manuscript as the evidence foundation rather than the final claim.

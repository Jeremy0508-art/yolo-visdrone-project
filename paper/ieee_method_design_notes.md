# IEEE Method Design Notes

## Purpose

This document records candidate method upgrades for the IEEE Transactions route. It is deliberately separated from the manuscript: ideas here are hypotheses until verified by real experiments.

Current evidence shows that:

- 960 input resolution is the strongest source of improvement.
- YOLO11n-P2-960 is the best current nano-scale trade-off.
- YOLO11n-P2-CA-960 does not outperform YOLO11n-P2-960.
- YOLO11s-960 is much stronger in absolute accuracy, so the final paper must focus on lightweight trade-offs rather than absolute superiority.

Therefore, the IEEE method cannot be built around a claim that CoordAttention is the decisive contribution. A stronger method should target the specific weakness that remains: tiny/dense object localization in the shallow high-resolution branch, while keeping the nano-scale efficiency advantage.

## Baseline for New Design

The safest current base is:

```text
YOLO11n-P2-960
```

because it is stronger than:

- YOLO11n-960 on mAP50 and mAP50-95.
- YOLOv8n-960 on mAP50 and mAP50-95.
- YOLO11n-P2-CA-960 on mAP50 and mAP50-95.

Any IEEE-oriented method must compare against YOLO11n-P2-960, not only against YOLO11n.

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

Start with Candidate A: TOFC.

Reason:

1. It is simple enough to implement in the current custom-module system.
2. It can be inserted after the P2 branch without redesigning the entire neck.
3. It directly targets the weakness introduced by shallow high-resolution features.
4. It provides a clearer IEEE method claim than CoordAttention.

Proposed first test:

```text
YOLO11n-P2-TOFC-960, 100 epochs, VisDrone, seed 42
```

Do not run UAVDT until the first VisDrone test proves that TOFC is not harmful.

## Current Implementation Status

An initial TOFC implementation has been added for structural validation:

| Artifact | Status |
| --- | --- |
| `src/models/attention/tiny_object_feature_calibration.py` | Implemented |
| `src/models/register.py` registration | Implemented |
| `configs/models/yolo11n_p2_tofc.yaml` | Implemented |
| `configs/train/yolo11n_p2_tofc_960.yaml` | Implemented |

Local model-build check passed without training:

| Model config | Layers | Parameters |
| --- | ---: | ---: |
| `configs/models/yolo11n_p2.yaml` | 30 | 2,893,672 |
| `configs/models/yolo11n_p2_tofc.yaml` | 31 | 2,895,762 |
| `configs/models/yolo11n_p2_coordatt.yaml` | 32 | 2,903,704 |

The TOFC candidate adds about 2,090 parameters over YOLO11n-P2, making it lighter than the existing CoordAttention variant. This is only a structural result; no accuracy claim is allowed until a real training run is completed.

## Acceptance Criteria

TOFC is worth continuing only if at least one of the following is true:

1. mAP50-95 improves over YOLO11n-P2-960 by a meaningful margin.
2. Small-object scale-wise Recall/AP improves while total mAP is not meaningfully worse.
3. FPS remains close to YOLO11n-P2-960 and clearly below YOLO11s complexity.

If TOFC fails all three, do not force it into the IEEE paper.

## Writing Implication

If TOFC works, the method name can become:

> HRFC-YOLO11n: High-Resolution Feature Calibration YOLO11n

If TOFC fails, the paper should avoid naming a new architecture and instead become a controlled study of high-resolution lightweight YOLO variants for UAV traffic-scene small-object detection, likely targeting a less competitive venue.

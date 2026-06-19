# IEEE Literature Comparison Protocol

Status: planning protocol. This is not a result table.

This protocol defines how recent literature should be used in the IEEE manuscript without mixing incompatible reported results with locally reproduced experiments.

## Core Rule

The final IEEE manuscript must separate:

1. **Reproduced local experiments**: results trained or validated in this repository with traceable configs, run directories, logs, weights, and metric tables.
2. **Reported literature context**: results or claims reported by other papers, used for background and novelty positioning only unless evaluation settings are directly comparable.

Do not merge these two categories into one ranked table.

## Allowed Table Types

| Table Type | Allowed Contents | Forbidden Contents |
| --- | --- | --- |
| Main reproduced results | Local VisDrone/UAVDT runs with audited metrics | Literature-reported numbers |
| Ablation table | Matched local variants such as input size, P2, CA, TOFC, augmentation | Cross-paper methods with different training settings |
| Literature context table | Method names, year, base detector, key idea, dataset used, reported split if known | Ranking claims such as "ours is best" unless directly reproduced |
| Reproduced external-method table | Only methods reproduced locally under documented settings | Methods whose code/data/split cannot be reproduced |

## Comparison Eligibility Gates

| Gate | Requirement |
| --- | --- |
| Dataset | Same dataset and split, or clearly marked as different. |
| Metric | Same metric definition, including mAP threshold range and validation/test protocol. |
| Input size | Same or explicitly reported input resolution. |
| Training protocol | Comparable epochs, augmentation, pretraining, and optimizer details, or clearly marked as not comparable. |
| Model capacity | Parameters/FLOPs or model scale reported when claiming lightweight advantage. |
| Reproducibility | Code/config available or local reproduction performed. |
| Evidence trace | Local table/log for reproduced results; publisher paper for reported-only context. |

## Current Literature Context Candidates

These entries are intended for related-work context and novelty pressure. They are not local reproduced results.

| Work | Seed Key | Year | Base / Focus | Current Use |
| --- | --- | ---: | --- | --- |
| TPH-YOLOv5 | `zhu2021tph_yolov5` | 2021 | Drone detection with additional prediction heads and Transformer prediction head | Close high-resolution/head-design prior |
| SOD-YOLO | `li2024sod_yolo` | 2024 | Improved YOLOv8 for UAV small objects | Recent UAV YOLOv8 prior |
| SOD-YOLOv8 | `khalili2024sod_yolov8` | 2024 | Aerial and traffic small-object YOLOv8 | T-ITS-relevant traffic/aerial prior |
| SMA-YOLO | `qu2025sma_yolo` | 2025 | Parameter-free attention and multi-scale fusion for UAV small objects | Recent multi-scale YOLOv8 prior |
| MASF-YOLO | `lu2025masf_yolo` | 2025 | YOLO11-based multi-scale aggregation and adaptive fusion | Very close YOLO11 novelty-pressure prior; preprint status |
| SRTSOD-YOLO | `xu2025srtsod_yolo` | 2025 | YOLO11-based real-time UAV small-object detection | Strong recent YOLO11 prior with UAVDT/VisDrone context |

## How to Write the Related Work

Use a structure like:

1. UAV datasets and traffic-scene benchmarks.
2. Feature pyramids and high-resolution detection heads.
3. Lightweight YOLO and UAV small-object detectors.
4. Attention and feature calibration.
5. Positioning of this work.

The positioning paragraph should state:

> Unlike reported-only comparisons across different training protocols, this manuscript focuses on locally reproduced lightweight YOLO baselines, controlled P2/input-size/attention ablations, and scale-wise diagnostics. Recent UAV small-object YOLO methods are discussed as related work and novelty pressure unless reproduced under the same experimental setting.

## Do Not Use

Do not write:

- "Our method outperforms SOD-YOLO / SMA-YOLO / SRTSOD-YOLO" unless those methods are reproduced locally or directly comparable under identical public protocol.
- "State-of-the-art" unless official or directly comparable evidence exists.
- "Better than reported results in the literature" if the split, input size, metric, and training settings differ.

## Next Actions

1. Decide which, if any, recent methods can realistically be reproduced.
2. Keep the final Results section centered on local reproduced baselines.
3. Use the literature context table in Related Work or Discussion, not as the main results ranking.
4. If a reported-only numerical comparison is included, label it clearly and add a paragraph explaining comparability limits.

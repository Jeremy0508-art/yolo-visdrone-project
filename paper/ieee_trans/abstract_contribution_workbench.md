# IEEE Abstract and Contribution Workbench

Status: planning draft. This is not the final IEEE abstract.

This workbench keeps the English abstract and contribution statements aligned with the evidence boundary in `paper/ieee_claim_boundary.md`.

## Current Evidence-Bounded Abstract Skeleton

Use this structure only if the paper is drafted before TOFC, UAVDT, and full scale-wise evidence are complete.

> Object detection in unmanned aerial vehicle (UAV) imagery is challenging because traffic participants and other scene objects often appear with small scales, dense layouts, occlusion, and large viewpoint variation. This work studies lightweight YOLO-based detection for UAV aerial scenes using VisDrone2019-DET as the primary benchmark. A YOLO11n-based high-resolution detection branch is evaluated together with input-resolution scaling, CoordAttention, and small-object-oriented augmentation settings. All reported results are traced to local training logs, validation outputs, and model artifacts. The current evidence shows that high-resolution input and P2 prediction branches provide the main gains within the nano-scale YOLO11n setting, while larger-capacity YOLO11s remains stronger in absolute accuracy. The study therefore positions the method around lightweight accuracy-speed-complexity trade-offs rather than universal superiority over larger detectors.

Do not submit this as-is. It is a safe draft skeleton for advisor discussion before the remaining IEEE experiments are complete.

## Locked Enhanced Abstract Skeleton

Use this only after the corresponding evidence exists.

> Object detection in UAV traffic scenes remains difficult for lightweight detectors because small objects are easily degraded by feature downsampling and dense occlusion. To address this problem, this paper proposes [FINAL METHOD NAME], a lightweight YOLO11n-based detector that combines a high-resolution P2 prediction branch with [VALIDATED MODULE]. The method is evaluated on VisDrone2019-DET and [SECOND DATASET], with matched baselines, ablation studies, scale-wise analysis, and speed-complexity measurements. Experimental results show that [FINAL METHOD] achieves [REAL METRIC] on [DATASET] and improves [REAL SCALE-WISE METRIC] over [MATCHED BASELINE], while maintaining [REAL FPS/PARAMETER TRADE-OFF]. Cross-dataset experiments further [STATE ONLY IF SUPPORTED]. These results demonstrate [EVIDENCE-BOUNDED CONCLUSION].

Locked placeholders:

| Placeholder | Unlock Evidence |
| --- | --- |
| `[FINAL METHOD NAME]` | Main method selected from real results. |
| `[VALIDATED MODULE]` | TOFC or another module has complete training and ablation evidence. |
| `[SECOND DATASET]` | UAVDT or another dataset is converted, validated, trained, and audited. |
| `[REAL METRIC]` | Exact value from audited result tables. |
| `[REAL SCALE-WISE METRIC]` | `paper/tables/ieee_scale_results_visdrone.csv`; wording must be recall/precision unless AP-specific evaluation is added. |
| `[REAL FPS/PARAMETER TRADE-OFF]` | Refreshed speed and complexity table for the final model. |

## Current Contribution Candidates

| Contribution | Current Status | Safe Wording |
| --- | --- | --- |
| Reproducible VisDrone YOLO baseline suite | Usable now | "A reproducible VisDrone validation suite is organized for YOLO11n, YOLOv5n, YOLOv8n, YOLO11s, and P2/CA variants." |
| High-resolution input and P2 branch analysis | Usable now | "The effect of input resolution and high-resolution P2 prediction is analyzed under nano-scale YOLO11n settings." |
| CoordAttention in P2 fusion | Usable as ablation | "CoordAttention is evaluated as an auxiliary attention component; current evidence does not make it the primary gain source." |
| TOFC module | Locked | Do not state as a validated contribution until full results exist. |
| UAVDT cross-dataset validation | Locked | Do not state as generalization evidence until conversion and training complete. |
| Scale-wise small-object recall/precision claim | Usable for completed VisDrone models | Use exact recall/precision values from `paper/tables/ieee_scale_results_visdrone.csv`; do not call them AP. |

## Suggested Final Contribution Format

After locked evidence is complete, the final IEEE introduction should use three or four concise contributions:

1. A lightweight high-resolution YOLO architecture or TOFC-enhanced architecture for UAV small-object detection.
2. A controlled ablation of input resolution, P2 prediction, attention/calibration, and augmentation under matched settings.
3. A multi-dataset validation on VisDrone and UAVDT with speed, complexity, and scale-wise metrics.
4. An evidence-bounded analysis of lightweight trade-offs and failure cases in dense UAV traffic scenes.

If TOFC does not improve the matched baseline, contribution 1 should be reframed as a systematic high-resolution lightweight YOLO analysis rather than a new module paper.

## Forbidden Abstract Wording Before Evidence

Avoid these phrases until the corresponding gates are complete:

- "state-of-the-art"
- "generalizes to UAVDT"
- "significantly improves small-object AP"
- "outperforms larger detectors"
- "robust across datasets"
- "TOFC improves detection performance"
- "official VisDrone test-dev result"

## Current Best Narrative

The current safest narrative is:

> The project is a reproducible and evidence-bounded study of lightweight YOLO design choices for UAV small-object detection. It shows that high-resolution input and P2 prediction are more defensible gain sources than treating CoordAttention as the main improvement, and it prepares the additional TOFC, UAVDT, and scale-wise gates required for a serious IEEE Transactions attempt.

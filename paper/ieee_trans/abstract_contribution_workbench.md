# IEEE Abstract and Contribution Workbench

Status: planning draft. This is not the final IEEE abstract.

This workbench keeps the English abstract and contribution statements aligned with the evidence boundary in `paper/ieee_claim_boundary.md`.

## Current Evidence-Bounded Abstract Skeleton

Use this structure for advisor discussion after the completed CSGate evidence gate. It remains non-final because the exact IEEE target, author metadata, and final submission package are not confirmed.

> Object detection in unmanned aerial vehicle (UAV) traffic imagery is challenging for lightweight detectors because small road users and vehicles are easily weakened by repeated feature downsampling, dense occlusion, and scale variation. This work audits high-resolution prediction in YOLO11n-family detectors on VisDrone2019-DET and UAVDT under traceable training, validation, speed, and scale-diagnostic protocols. The completed evidence shows that high-resolution input and a static P2 branch can improve VisDrone small-object diagnostics, but UAVDT exposes a cross-dataset validity boundary: the same static P2 design is weaker than the resolution-matched YOLO11n baseline and other completed references. A first adaptive candidate, ScaleAwareP2Gate, is completed but remains mixed/negative evidence under the predeclared decision audit. Motivated by that failure mode, CrossScaleP2P3ConsistencyGate conditions P2 detail on adjacent P3 semantics. The completed CSGate evidence improves VisDrone aggregate accuracy and small-object recall and repairs part of the UAVDT static-P2 degradation, but remains below the strongest UAVDT baselines and does not dominate every small-object diagnostic. The final claim should therefore be a bounded cross-scale adaptation method rather than a state-of-the-art or cross-dataset superiority claim.

Do not submit this as-is. It is a safe post-CSGate advisor skeleton; final wording still needs target-journal, author, reference, and page-budget confirmation.

## Locked Final Abstract Skeleton

Use this only after the corresponding evidence exists.

> Object detection in UAV traffic scenes remains difficult for lightweight detectors because small objects are easily degraded by feature downsampling, dense occlusion, and scale variation. To address this problem, this paper proposes [FINAL METHOD NAME], a lightweight YOLO11n-based detector that combines high-resolution P2 prediction with [VALIDATED ADAPTIVE MODULE]. The method is evaluated on VisDrone2019-DET and UAVDT against YOLO11n, YOLOv8n, YOLO11s, static P2, and calibration ablations under matched training settings. Experimental results show that [FINAL METHOD] achieves [REAL PRIMARY METRIC] on [PRIMARY DATASET], improves [REAL SCALE-WISE METRIC] over [MATCHED P2 OR YOLO11N BASELINE], and maintains [REAL FPS/PARAMETER TRADE-OFF]. Cross-dataset experiments on UAVDT further [STATE ONLY IF SUPPORTED BY AUDITED SCALEGATE RESULTS]. These results demonstrate [EVIDENCE-BOUNDED CONCLUSION].

Locked placeholders:

| Placeholder | Unlock Evidence |
| --- | --- |
| `[FINAL METHOD NAME]` | Main method selected from real results. |
| `[VALIDATED ADAPTIVE MODULE]` | CSGate or a later adaptive-P2 module passes the method-selection gates. |
| `[REAL METRIC]` | Exact value from audited result tables. |
| `[REAL SCALE-WISE METRIC]` | `paper/tables/ieee_scale_results_visdrone.csv`; wording must be recall/precision unless AP-specific evaluation is added. |
| `[REAL FPS/PARAMETER TRADE-OFF]` | Refreshed speed and complexity table for the final model. |

## Current Contribution Candidates

| Contribution | Current Status | Safe Wording |
| --- | --- | --- |
| Reproducible VisDrone YOLO baseline suite | Usable now | "A reproducible VisDrone validation suite is organized for YOLO11n, YOLOv5n, YOLOv8n, YOLO11s, and P2/CA variants." |
| High-resolution input and P2 branch analysis | Usable now | "The effect of input resolution and high-resolution P2 prediction is analyzed under nano-scale YOLO11n settings." |
| CoordAttention in P2 fusion | Usable as ablation | "CoordAttention is evaluated as an auxiliary attention component; current evidence does not make it the primary gain source." |
| TOFC module | Usable only as caveated ablation | "TOFC improves aggregate VisDrone nano-scale metrics but does not beat P2-only on the current small-object diagnostics." |
| UAVDT cross-dataset validation | Usable as boundary evidence | "UAVDT shows that the static P2 trend does not transfer under the completed setting." |
| ScaleAwareP2Gate module | Completed mixed/negative evidence | "ScaleAwareP2Gate is an identity-initialized adaptive P2 gate that did not pass the predeclared main-method acceptance routes." |
| CrossScaleP2P3ConsistencyGate module | Completed bounded method-candidate evidence | "CSGate conditions P2 detail on adjacent P3 semantics, improves VisDrone aggregate accuracy/small recall, and partially repairs UAVDT static-P2 degradation, but it is not a universal superiority claim." |
| Scale-wise small-object recall/precision claim | Usable for completed VisDrone models | Use exact recall/precision values from `paper/tables/ieee_scale_results_visdrone.csv`; do not call them AP. |

## Suggested Final Contribution Format

After locked evidence is complete, the final IEEE introduction should use three or four concise contributions:

1. A lightweight adaptive high-resolution YOLO architecture for UAV small-object detection, if CSGate or a later adaptive module passes the gates.
2. A controlled ablation of input resolution, P2 prediction, attention/calibration, and augmentation under matched settings.
3. A multi-dataset validation on VisDrone and UAVDT with speed, complexity, and scale-wise metrics.
4. An evidence-bounded analysis of lightweight trade-offs and failure cases in dense UAV traffic scenes.

ScaleGate did not pass the gates; contribution 1 can now be framed around CSGate only with the bounded evidence in `paper/ieee_csgate_method_decision_audit.md`.

## Forbidden Abstract Wording Before Evidence

Avoid these phrases until the corresponding gates are complete:

- "state-of-the-art"
- "generalizes to UAVDT"
- "significantly improves small-object AP"
- "outperforms larger detectors"
- "robust across datasets"
- "TOFC improves detection performance"
- "ScaleGate is the proposed method"
- "CSGate is state-of-the-art"
- "CSGate is robust across datasets"
- "official VisDrone test-dev result"

## Current Best Narrative

The current safest narrative is:

> The project has moved from a reproducible high-resolution YOLO study into a bounded adaptive high-resolution method paper. Completed VisDrone and UAVDT results expose the weakness of static P2. ScaleAwareP2Gate is completed but rejected as the main method, while CSGate passes the predeclared cross-dataset repair and small-object diagnostic routes. The final abstract and contribution list should present CSGate as a partial cross-scale repair mechanism, with explicit limitations against YOLO11n-960, YOLOv8n-960, and YOLO11s-960 on UAVDT.

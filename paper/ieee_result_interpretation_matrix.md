# IEEE Result Interpretation Matrix

Status: evidence-bounded writing matrix. This is not final manuscript prose.

This document defines how the current and future experiment results should affect the IEEE Transactions manuscript narrative. It does not add new numbers. All listed metrics come from audited local tables and generated interpretation reports.

## Source Evidence

| Evidence Type | Source |
| --- | --- |
| Main validation metrics | `paper/tables/main_comparison_for_paper.csv` |
| Speed and complexity | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` |
| Experiment registry | `paper/tables/ieee_experiment_registry.csv`, `paper/ieee_experiment_registry_audit.md` |
| Scale-wise recall/precision | `paper/tables/ieee_scale_results_visdrone.csv`, `paper/ieee_scale_result_interpretation.md` |
| Local scale-bin AP | `paper/tables/ieee_scale_ap_results_visdrone.csv`, `paper/ieee_scale_ap_interpretation.md` |
| Claim boundary | `paper/ieee_claim_boundary.md` |
| Method decision rules | `paper/ieee_method_selection_protocol.md` |

## Current Evidence Reading

| Result Relation | Evidence-Bounded Reading | Safe Manuscript Use | Avoid |
| --- | --- | --- | --- |
| YOLO11n-640 vs YOLO11n-960 | Increasing input resolution from 640 to 960 substantially improves the YOLO11n baseline on VisDrone validation: best mAP50 `0.32153` to `0.42136`, best mAP50-95 `0.18238` to `0.25067`. | High-resolution input is an important factor for UAV small-object detection in the completed VisDrone experiments. | Do not attribute this gain to P2 or attention. |
| YOLO11n-960 vs YOLO11n-P2-960 | P2 gives a modest aggregate gain at the same 960 input: best mAP50 `0.42136` to `0.42361`, best mAP50-95 `0.25067` to `0.25552`. | P2 is the current best completed nano-scale trade-off and the primary fallback method if TOFC does not pass. | Do not describe the aggregate gain as large. |
| YOLO11n-P2-960 vs YOLO11n-P2-CA-960 | CoordAttention does not improve the current aggregate best metrics over P2-960: best mAP50-95 `0.25174` vs `0.25552`. It increases small recall relative to YOLO11n-960 but has lower local small-bin AP50 than P2-960. | Treat CoordAttention as an ablation that changes scale-wise behavior, not as the main contribution. | Do not put CoordAttention in the title as a proven primary improvement unless later evidence changes. |
| YOLO11n-P2-CA-640 vs SmallObjAug | SmallObjAug underperforms the corresponding P2-CA 640 setting in current evidence: best mAP50 `0.32780` vs `0.33073`, best mAP50-95 `0.18699` vs `0.19044`. | Use as a negative ablation showing that simple small-object-oriented augmentation does not automatically help. | Do not present SmallObjAug as a successful improvement. |
| YOLO11n-P2-960 vs YOLOv8n-960 | P2-960 is slightly stronger than YOLOv8n-960 in best mAP50 and best mAP50-95: `0.42361`/`0.25552` vs `0.42016`/`0.25121`. | Use YOLOv8n-960 as a fair high-resolution lightweight reference, not as a weak baseline. | Do not claim broad superiority over all YOLO families. |
| YOLO11n-P2-960 vs YOLO11s-960 | YOLO11s-960 remains much stronger in absolute accuracy: best mAP50-95 `0.29812` vs `0.25552`. | Frame the paper around lightweight accuracy-speed-complexity trade-off. | Do not claim the nano model outperforms larger-capacity detectors. |
| Scale-wise recall/precision | YOLO11n-P2-960 improves small-object recall over YOLO11n-960 by `0.029865`, while medium/large bins show trade-offs. | Say P2 improves scale-wise small-object recall in the local VisDrone analysis. | Do not say all scales improve. |
| Local scale-bin AP | YOLO11n-P2-960 improves local small-bin AP50 over YOLO11n-960 by `0.017664` and local small-bin mAP50-95 by `0.015245`. | Use as local scale-bin AP diagnostic evidence. | Do not call this official AP-small, COCO AP-small, or VisDrone official AP-small. |
| TOFC candidate | TOFC now has a complete VisDrone run. It improves aggregate best metrics over YOLO11n-P2-960: best mAP50 `0.42837` vs `0.42361`, best mAP50-95 `0.26054` vs `0.25552`. However, it is weaker than P2-960 on the current small-object diagnostics: small recall `0.430828` vs `0.450124`, local small-bin AP50 `0.229853` vs `0.247659`. | Use TOFC as an aggregate-accuracy and efficiency trade-off candidate or ablation. It should not replace P2-960 as a small-object diagnostic winner unless later evidence changes. | Do not claim TOFC improves small-object diagnostics over YOLO11n-P2-960. |
| UAVDT cross-dataset route | UAVDT config, setup notes, and converter exist, but raw data/conversion/results are pending. | Mention UAVDT only as a planned cross-dataset validation gate. | Do not claim generalization beyond VisDrone. |
| VisDrone test-dev | No official returned test-dev metrics are available. | Keep all current quantitative claims on validation-set evidence. | Do not imply official challenge ranking or official test-dev performance. |

## Manuscript Narrative Branches

| Branch | Trigger | Manuscript Route |
| --- | --- | --- |
| TOFC aggregate route | TOFC improves aggregate best mAP50/mAP50-95 over YOLO11n-P2-960 but does not improve small-object diagnostics | TOFC can be discussed as an aggregate-accuracy calibration ablation; title/abstract should avoid claiming small-object diagnostic superiority |
| TOFC small-object route fails | TOFC small recall and local small-bin AP50 are below YOLO11n-P2-960 | Keep P2-960 as the stronger small-object diagnostic variant |
| UAVDT trends agree with VisDrone | UAVDT YOLO11n-P2 improves over UAVDT YOLO11n under the same protocol | Limited cross-dataset support for P2-style design |
| UAVDT trends contradict VisDrone | UAVDT results do not support the same trend | Use UAVDT as limitation/negative evidence; remove generalization claims |
| YOLO11s remains dominant | Larger model has higher accuracy and small-object diagnostics | Keep deployment/trade-off framing; avoid best-performance framing |

## Abstract and Conclusion Rules

Update abstract and conclusion only after:

1. Final method route is selected from completed evidence.
2. `paper/tables/main_comparison_for_paper.csv` includes every final model row used in the text.
3. Speed and complexity rows exist for every model described as lightweight or efficient.
4. Scale-wise and local AP diagnostic claims are checked against the latest generated reports.
5. `python tools/run_ieee_audits.py` passes with zero missing planning artifacts.

## Forbidden Shortcuts

- Do not average or infer metric values from figures.
- Do not copy partial epoch results into tables.
- Do not mix reproduced local results and literature-only reported numbers in the same fairness table.
- Do not use "state-of-the-art" unless same-split comparable evidence is available.
- Do not describe local scale-bin AP as official AP-small.

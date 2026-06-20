# IEEE Claim Boundary and Evidence Rules

This document defines what can and cannot be claimed during the IEEE Transactions route. It is a working guardrail for the future English manuscript, advisor brief, cover letter, README updates, and result tables.

## Current Safe Claims

| Claim | Current Status | Evidence |
| --- | --- | --- |
| The project has completed a VisDrone2019-DET YOLO-format experimental pipeline | Allowed | `configs/dataset/visdrone.yaml`, existing `runs/detect/` directories, `paper/tables/` |
| YOLO11n, YOLO11n-P2, YOLO11n-P2-CA, 960-input variants, SmallObjAug, YOLOv5n, YOLOv8n, and YOLO11s comparisons have local evidence | Allowed when numbers are copied only from audited tables | `paper/tables/main_comparison_for_paper.csv`, `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` |
| 960 input improves the completed YOLO11n/P2 setting on VisDrone validation metrics | Allowed only with exact table values and matching run evidence | `paper/tables/main_comparison_for_paper.csv`, corresponding `runs/detect/*/results.csv` |
| P2 adds a high-resolution prediction branch and changes model complexity | Allowed as a structural statement | `configs/models/yolo11n_p2.yaml`, `paper/tables/model_complexity.csv` |
| Completed VisDrone models have full scale-wise recall/precision evidence | Allowed only as recall/precision wording, not AP wording | `paper/tables/ieee_scale_results_visdrone.csv`, `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` |
| Completed VisDrone models have local scale-bin AP evidence | Allowed only as local scale-bin AP wording, not official COCO/VisDrone AP-small wording | `paper/tables/ieee_scale_ap_results_visdrone.csv`, `paper/ieee_scale_ap_interpretation.md` |
| TOFC is a completed VisDrone aggregate-mAP candidate | Allowed only with exact VisDrone validation values and the small-object diagnostic caveat | `runs/detect/yolo11n_p2_tofc_960_visdrone/results.csv`, `paper/tables/main_comparison_for_paper.csv`, `paper/tables/ieee_scale_results_visdrone.csv`, `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| The IEEE route requires stronger evidence than the paused CEA route | Allowed as a planning statement | `paper/IEEE_TRANS_SUBMISSION_PLAN.md`, `paper/ieee_required_experiment_gap.md` |

## Locked Claims

| Do Not Claim Yet | Why It Is Locked | Evidence Needed to Unlock |
| --- | --- | --- |
| TOFC improves small-object recall or local small-bin AP over YOLO11n-P2-960 | Current synced evidence contradicts this: TOFC has lower small recall and local small-bin AP50 than YOLO11n-P2-960 | New completed evidence with the same evaluation protocol |
| The method generalizes beyond VisDrone | No second dataset results are complete | Converted UAVDT dataset plus baseline/main-model results and integrity audit |
| The method is SOTA | Current comparisons are local YOLO-family baselines and literature seed notes | Same-split reproduced or directly comparable literature/SOTA results |
| The method outperforms larger models | Existing YOLO11s-960 is stronger in absolute accuracy | A clearly defined accuracy-speed-complexity claim, not an absolute superiority claim |
| Official VisDrone test-dev performance is available | The previous official platform workflow was blocked | Official returned metrics and submission archive evidence |
| Multi-seed robustness is demonstrated | Most current results are single-seed runs | Mean/std over repeated seeds for key baseline and final model |
| Official AP-small improvement is proven directly | Current AP-style evidence is local scale-bin AP, not official COCO/VisDrone AP-small | Use an official or fully compatible evaluator, or explicitly limit wording to local scale-bin AP |

## Wording Rules

Use these safer formulations before all locked evidence is available:

- Prefer "candidate module", "planned validation", "current VisDrone validation evidence", and "accuracy-speed-complexity trade-off".
- Avoid "state-of-the-art", "generalizes", "consistently improves", "significantly outperforms", and "robust across datasets" unless the corresponding evidence gate is complete.
- When comparing with YOLO11s or other larger models, state that larger-capacity models can achieve higher absolute accuracy and frame the project around lightweight trade-offs.
- When discussing CoordAttention, describe the observed result honestly and avoid making it the central contribution unless later evidence supports it.
- When using literature-only results, mark them as reported results and do not merge them into directly reproduced experiment tables.
- When using the completed scale-wise VisDrone output, describe it as scale-wise recall/precision evidence.
- When using the completed local AP diagnostic, describe it as local scale-bin AP. Do not call it official AP-small evidence.

## Evidence Trace Required for Every IEEE Table Row

Each result row used in an IEEE manuscript table must trace to:

1. Training or validation command/configuration.
2. Run directory.
3. `results.csv` or validation metric output.
4. `args.yaml` or equivalent configuration record.
5. Weight file used for validation/speed testing.
6. Metric extraction script or manually audited table source.
7. Hardware and software environment if the row includes speed, latency, FPS, or memory.

Rows without this trace can remain in planning notes, but must not appear as final manuscript evidence.

## Immediate Claim Audit Tasks

| Task | Output |
| --- | --- |
| Add an automated IEEE claim scanner before writing the English manuscript | `tools/check_ieee_claims.py` |
| Keep Phase 1 artifact readiness current | `tools/check_ieee_phase1_artifacts.py` -> `paper/ieee_phase1_artifact_audit.md` |
| Create claim-to-evidence mapping after new results arrive | `paper/ieee_claim_audit.md` |
| Re-run manuscript claim audit before advisor sharing and before submission | Updated audit reports under `paper/` |

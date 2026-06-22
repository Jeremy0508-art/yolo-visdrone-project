# IEEE Transactions Manuscript Blueprint

Status: planning draft, not a submission manuscript.

This blueprint converts the current YOLO-VisDrone project into an IEEE Transactions narrative without inventing missing results. It should be revised after ScaleGate and any later second-cycle method experiments are complete.

## Target Framing

Primary target: IEEE Transactions on Intelligent Transportation Systems.

Working theme:

> Lightweight UAV traffic-object detection under dense small-object scale variation.

The paper should not be framed as "a lightweight model beats all larger detectors." The defensible framing is:

> A systematic lightweight YOLO study and method upgrade for UAV aerial small-object detection, emphasizing high-resolution prediction, scale-aware feature calibration, and accuracy-speed-complexity trade-offs.

After the completed UAVDT boundary result, the preferred IEEE route is no longer to package a static P2 result. The active method route is to test an adaptive high-resolution P2 mechanism, currently ScaleAwareP2Gate.

## Candidate Titles

Use the final title only after the final method is selected from real results.

| Route | Candidate Title | Use Condition |
| --- | --- | --- |
| Current evidence route | High-Resolution Lightweight YOLO for Small Object Detection in UAV Traffic Scenes | Use only if no new module becomes the final contribution. |
| TOFC route | TOFC-YOLO11n: Tiny-Object Feature Calibration for Lightweight UAV Traffic Object Detection | Use only if TOFC improves validated metrics and speed/complexity remains acceptable. |
| Adaptive P2 route | Scale-Aware High-Resolution Prediction for Lightweight UAV Object Detection | Use only if ScaleGate or a later adaptive method passes the VisDrone/UAVDT gates. |
| Conservative analysis route | Revisiting High-Resolution Feature Branches for Lightweight UAV Object Detection | Use if method gains are modest but analysis is strong. |

## Contribution Boundary

| Contribution Candidate | Manuscript Status | Required Evidence |
| --- | --- | --- |
| A reproducible YOLO11n/YOLOv5n/YOLOv8n/YOLO11s comparison on VisDrone | Can be used now with exact audited values | `paper/tables/main_comparison_for_paper.csv`, run directories |
| P2 and 960-input analysis for lightweight YOLO11n | Can be used now with careful wording | Completed VisDrone runs and complexity/speed tables |
| CoordAttention analysis | Can be discussed as an ablation, not a primary gain source | Completed P2-CA results and honest interpretation |
| TOFC as a method contribution | Not selected under current evidence | Completed VisDrone evidence exists, but small-object diagnostics and cross-dataset evidence do not support it as the final method |
| ScaleAwareP2Gate as a method contribution | Locked until completed runs | Complete VisDrone and UAVDT ScaleGate runs, refreshed speed, complexity, and scale diagnostics |
| Cross-dataset validation for static P2 | Ready as boundary evidence | Completed UAVDT rows in `paper/tables/ieee_uavdt_results_for_paper.csv` |
| Small-object-specific improvement claim | Partially ready | Current VisDrone scale-wise recall/precision and local scale-bin AP are ready for completed models; final-method evidence remains pending |
| IEEE-level generalization claim | Locked | Complete second-dataset evidence that supports a positive final-method claim |

## Abstract Blueprint

The abstract should contain four parts: problem, method, results, and conclusion. Draft only after final evidence exists.

Safe abstract structure:

1. Problem: UAV traffic-object detection faces dense small objects, occlusion, viewpoint variation, and real-time constraints.
2. Method: describe only the selected final method. If TOFC is not validated, do not name it as a final contribution.
3. Results: report exact VisDrone and cross-dataset numbers only from audited tables.
4. Conclusion: state the accuracy-speed-complexity trade-off and limitations without overclaiming SOTA.

Do not write "state-of-the-art", "generalizes", or "significantly improves" unless the corresponding gates in `paper/ieee_claim_boundary.md` are complete.

## Section Plan

### 1. Introduction

Purpose:
- Establish the T-ITS scenario: UAV-assisted traffic monitoring and dense aerial object detection.
- Explain why small objects are difficult: limited pixels, occlusion, high density, scale variation, and category ambiguity.
- Position lightweight YOLO models as practical but limited under high-altitude scenes.
- State evidence-bounded contributions.

Expected contribution list after full experiments:

1. A lightweight high-resolution detection architecture or adaptive P2 mechanism for UAV small-object detection.
2. A systematic study of P2 branch, input resolution, attention/fusion, and small-object augmentation under matched settings.
3. Cross-dataset validation on VisDrone and UAVDT, used either as positive support or as a documented validity boundary.
4. Efficiency and scale-wise analysis linking accuracy gains to small-object behavior.

Until locked evidence is complete, mark contributions 3 and 4 as planned, not final.

### 2. Related Work

Recommended subsections:
- UAV traffic and aerial object detection datasets.
- Small object detection and scale-aware evaluation.
- Feature pyramids and high-resolution prediction branches.
- Lightweight YOLO detectors.
- Attention and feature calibration modules.

Input material:
- `paper/ieee_related_work_matrix.csv`
- `paper/ieee_dataset_strategy.md`
- `paper/ieee_target_journal_analysis.md`

### 3. Method

Possible structure:
- Overview of baseline YOLO11n and lightweight constraints.
- High-resolution P2 prediction branch.
- CoordAttention and TOFC as calibration ablations.
- ScaleAwareP2Gate or later adaptive-P2 method, if validated.
- Training/inference pipeline.
- Complexity discussion.

Current safe rule:
- TOFC may be described as a completed VisDrone calibration ablation, not as the final method.
- ScaleAwareP2Gate may be described as a candidate design and formula-level method, but not as a result-bearing method until completed runs exist.

### 4. Experiments

Required subsections:
- Datasets: VisDrone and UAVDT after UAVDT is complete.
- Implementation details: epochs, input sizes, optimizer behavior, seeds, hardware, software.
- Main results: reproduced baselines and final method.
- Ablations: P2, input size, attention/fusion, augmentation, TOFC if valid.
- Scale-wise analysis: small/medium/large or custom size bins.
- Efficiency: parameters, GFLOPs, weight size, latency, FPS, and optionally memory.
- Qualitative analysis and failure cases.

Rows without local traceability must remain out of final tables.

### 5. Discussion

Purpose:
- Explain why higher input resolution and shallow high-resolution branches help.
- Discuss why larger models can still win in absolute accuracy.
- Separate practical lightweight value from absolute SOTA claims.
- Analyze failure cases such as tiny distant objects, dense occlusion, and class ambiguity.

### 6. Conclusion

Keep concise and evidence-bounded:
- Summarize validated design findings.
- State deployment trade-offs.
- Mention limitations and future work only if not used to cover missing required experiments.

## Minimum Tables for IEEE Draft

| Table | Source | Status |
| --- | --- | --- |
| Dataset statistics | Existing VisDrone stats plus UAVDT conversion evidence | Partially ready |
| Main comparison on VisDrone | `paper/tables/main_comparison_for_paper.csv` | Ready for current evidence route |
| Cross-dataset comparison | `paper/tables/ieee_uavdt_results_for_paper.csv` | Ready for completed baselines; ScaleGate locked |
| Ablation study | Existing VisDrone rows plus TOFC and future ScaleGate | Partially ready |
| Scale-wise recall/precision | `paper/tables/ieee_scale_results_visdrone.csv` | Ready for completed VisDrone models |
| Local scale-bin AP | `paper/tables/ieee_scale_ap_results_visdrone.csv` | Ready for completed VisDrone models; do not describe as official AP-small/AP-medium/AP-large |
| Speed and complexity | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` | Ready for existing models |

## Minimum Figures for IEEE Draft

| Figure | Source | Status |
| --- | --- | --- |
| Method overview | Existing overview can be redrawn in English | Pending final method |
| ScaleAwareP2Gate schematic | `paper/figures/method/scalegate_schematic.png` | Design-ready, result-locked |
| Training/validation curves | Existing completed runs | Ready for existing models |
| Accuracy-speed-complexity plot | Existing tables, plus new final method later | Partially ready |
| Scale-wise recall plot | `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` | Ready for completed VisDrone models |
| Local scale-bin AP plot | `paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png` | Ready for completed VisDrone models; label as local scale-bin AP |
| Qualitative comparison | Existing visualizations, may need English captions | Partially ready |
| Failure case taxonomy | Existing failure cases plus English labels | Partially ready |

## Immediate Writing Tasks

1. Convert this blueprint into a non-final IEEE outline after the target journal is confirmed.
2. Add `paper/ieee_trans/evidence_to_sections.csv`.
3. Add a table/figure plan with source files and status.
4. Wait for completed ScaleGate evidence and method-selection review before drafting a final-looking `main.tex`.

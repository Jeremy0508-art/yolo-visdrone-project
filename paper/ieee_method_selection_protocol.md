# IEEE Method Selection Protocol

Status: decision protocol. This is not manuscript text.

This document defines how to choose the final method route for the IEEE Transactions manuscript after TOFC and any later experiments are available. It prevents post-hoc metric cherry-picking.

## Current Evidence-Based Ranking

The current completed VisDrone evidence supports the following interpretation:

| Candidate | Aggregate Result | Small-Object Diagnostic | Efficiency/Complexity | Current Role |
| --- | --- | --- | --- | --- |
| YOLO11n-960 | Best mAP50 0.42136, best mAP50-95 0.25067 | Small recall 0.420259; local small-bin AP50 0.229995 | 2.592 M params, 6.5 GFLOPs | Resolution-matched nano baseline |
| YOLO11n-P2-960 | Best mAP50 0.42361, best mAP50-95 0.25552 | Small recall 0.450124; local small-bin AP50 0.247659 | 2.894 M params, 10.7 GFLOPs | Current best nano-scale trade-off |
| YOLO11n-P2-CA-960 | Best mAP50 0.41996, best mAP50-95 0.25174 | Small recall 0.455089; local small-bin AP50 0.239473 | 2.904 M params, 10.7 GFLOPs | Attention ablation, not current main method |
| YOLO11n-P2-TOFC-960 | Best mAP50 0.42837, best mAP50-95 0.26054 | Small recall 0.430828; local small-bin AP50 0.229853 | 2.896 M params, 10.8 GFLOPs, 44.23 FPS | Aggregate-accuracy candidate; not a small-object diagnostic winner |
| YOLOv8n-960 | Best mAP50 0.42016, best mAP50-95 0.25121 | Small recall 0.422516; local small-bin AP50 0.237713 | 3.013 M params, 8.2 GFLOPs | External lightweight reference |
| YOLO11s-960 | Best mAP50 0.48901, best mAP50-95 0.29812 | Small recall 0.492703; local small-bin AP50 0.302540 | 9.432 M params, 21.6 GFLOPs | Larger-capacity upper reference |

Current route after TOFC:

> TOFC gives the best completed nano-scale aggregate mAP on VisDrone, but YOLO11n-P2-960 remains stronger on the current small-object diagnostic metrics. The IEEE manuscript should not present TOFC as a clear small-object enhancement. A defensible route is to discuss TOFC as an aggregate calibration ablation while keeping the main claim centered on high-resolution lightweight trade-offs.

## Primary Comparison Baseline

Any candidate final method must be compared primarily against:

```text
YOLO11n-P2-960
```

Reason:

- It is stronger than YOLO11n-960 on best mAP50 and best mAP50-95.
- It is stronger than YOLOv8n-960 on best mAP50 and best mAP50-95.
- It is stronger than YOLO11n-P2-CA-960 on best mAP50, best mAP50-95, and local small-bin AP50.
- It remains stronger than TOFC on small-object recall and local small-bin AP50, even though TOFC has higher aggregate best mAP.

Comparing a new method only against YOLO11n-960 would be too weak for IEEE.

## Metric Priority

Use this priority order when deciding whether a candidate becomes the final method:

1. Best mAP50-95 on VisDrone validation.
2. Local small-bin AP50/mAP50-95 and small-object recall.
3. Precision/recall balance and mAP50.
4. Parameters, GFLOPs, weight size, latency, and FPS.
5. Cross-dataset consistency after UAVDT is available.

Do not choose the final method based on a single metric if the other metrics clearly contradict it.

## TOFC Acceptance Rules

TOFC can become the final proposed method only if the completed run satisfies one of these evidence-backed routes:

| Route | Required Evidence | Manuscript Implication |
| --- | --- | --- |
| A: balanced gain | TOFC improves best mAP50-95 over YOLO11n-P2-960 and does not reduce local small-bin AP50 | TOFC can be the main method |
| B: small-object gain | TOFC improves local small-bin AP50 or small recall over YOLO11n-P2-960, while aggregate mAP50-95 is not worse enough to undermine the trade-off | TOFC can be framed as a small-object trade-off module |
| C: efficiency gain | TOFC matches P2 accuracy closely while keeping lower complexity than P2-CA and acceptable latency | TOFC can be framed as a lightweight calibration alternative |

If none of these routes is supported, TOFC should remain a failed or negative ablation and must not be forced into the paper title.

Current TOFC reading:

- Aggregate evidence is positive: best mAP50-95 improves from 0.25552 for YOLO11n-P2-960 to 0.26054 for YOLO11n-P2-TOFC-960.
- Small-object diagnostic evidence is negative relative to P2-960: small recall drops from 0.450124 to 0.430828, and local small-bin AP50 drops from 0.247659 to 0.229853.
- Efficiency evidence is mixed but acceptable for an ablation: TOFC records 2.896 M parameters, 10.8 GFLOPs, and 44.23 FPS under the current local speed protocol.
- Therefore, TOFC does not pass the small-object Route B and should not be titled as the small-object improvement. It can be retained as an aggregate-accuracy calibration ablation or secondary candidate while the manuscript avoids overclaiming.

## CoordAttention Decision

CoordAttention should not be the central method claim under current evidence:

- P2-CA-960 has higher small recall than P2-960: 0.455089 vs 0.450124.
- P2-CA-960 has lower best mAP50-95 than P2-960: 0.25174 vs 0.25552.
- P2-CA-960 has lower local small-bin AP50 than P2-960: 0.239473 vs 0.247659.

Safe wording:

> CoordAttention changes the precision-recall and scale-wise behavior, but it is not the primary source of the current best nano-scale trade-off.

## YOLO11s Boundary

YOLO11s-960 remains stronger in absolute accuracy and small-object diagnostics:

- Best mAP50-95: 0.29812 vs 0.25552 for YOLO11n-P2-960.
- Small recall: 0.492703 vs 0.450124 for YOLO11n-P2-960.
- Local small-bin AP50: 0.302540 vs 0.247659 for YOLO11n-P2-960.

Therefore, the final paper must not claim that the nano-scale method outperforms larger-capacity detectors. The valid comparison is deployment-oriented trade-off, not absolute superiority.

## Decision Outcomes

| Outcome | Condition | Paper Route |
| --- | --- | --- |
| TOFC passes Route A | Balanced aggregate and small-object gains | TOFC-centered method paper |
| TOFC passes Route B | Small-object gain with acceptable aggregate trade-off | Small-object calibration trade-off paper |
| TOFC passes Route C only | Efficiency or complexity benefit without clear accuracy gain | Lightweight calibration analysis, not strong method claim |
| TOFC fails all routes | No defensible gain over P2-960 | P2 high-resolution analysis paper or lower-risk venue |
| UAVDT trend contradicts VisDrone | No cross-dataset consistency | Remove generalization claim; treat UAVDT as limitation |

## Required Update After TOFC

Completed after syncing the TOFC run:

1. Add TOFC to `paper/tables/main_comparison_for_paper.csv`.
2. Refresh speed and complexity rows.
3. Re-run scale-wise recall/precision for TOFC.
4. Re-run local scale-bin AP for TOFC.
5. Run `python tools/run_ieee_audits.py`.
6. Update this protocol with exact TOFC values.

Remaining decision:

7. Decide whether TOFC enters the title, abstract, method name, and contribution list. Under the current evidence, TOFC should not be the small-object claim in the title.

## Current Decision

Current decision after TOFC result:

> YOLO11n-P2-TOFC-960 is the best completed nano-scale aggregate-mAP candidate on VisDrone, but YOLO11n-P2-960 remains stronger on the current small-object diagnostic metrics. The manuscript should frame TOFC cautiously as a calibration ablation or aggregate-accuracy candidate, not as a proven small-object superiority module.

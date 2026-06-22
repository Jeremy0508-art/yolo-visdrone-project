# IEEE Reviewer Response Preparation Plan

Status: response-preparation workbench, not a rebuttal.

This document prepares likely IEEE reviewer questions and evidence-bounded response strategies. It should be updated after the final manuscript, ScaleGate or later adaptive-method result, and exact target journal are settled.

## Response Principles

1. Answer every reviewer point with evidence, not intention.
2. Separate reproduced local results from literature-reported results.
3. Do not create new numerical claims during response writing unless the underlying run, table, and audit are complete.
4. If a requested experiment cannot be completed, state the limitation and revise claims downward.
5. Keep the response consistent with `paper/ieee_claim_boundary.md` and `paper/ieee_reviewer_risk_register.md`.

## Likely Reviewer Questions and Prepared Responses

| Reviewer Question | Evidence to Use | Possible Response Direction | Additional Work If Needed |
| --- | --- | --- | --- |
| Why is this suitable for T-ITS rather than a generic computer-vision venue? | `paper/ieee_tits_scope_fit_checklist.md`, traffic-scene qualitative figures, VisDrone/UAVDT framing | Emphasize UAV-assisted traffic sensing, road users, dense traffic-like scenes, and deployment constraints. | Add clearer traffic-scene examples and strengthen the introduction/application discussion. |
| What is the real novelty beyond P2, 960 input, and common attention modules? | ScaleGate evidence if complete; method-selection protocol; ablation tables | If ScaleGate passes the gates, present adaptive P2 modulation as the validated contribution; if not, frame as boundary analysis or redesign. | Complete ScaleGate VisDrone/UAVDT runs; if weak, launch a second-cycle adaptive design instead of overclaiming. |
| Why does CoordAttention not consistently improve the 960-input P2 model? | `main_comparison_for_paper.csv`, scale-wise tables | Acknowledge that CoordAttention shifts recall/precision behavior and is an ablation, not the primary improvement. | Add a concise failure/interpretation paragraph instead of claiming universal CA benefit. |
| Are improvements meaningful or just random seed variation? | Existing seed 42 logs; future multi-seed runs if available | State current evidence is single-run unless repeated; use cautious wording. | Run seeds 43/44 for YOLO11n-960 and final method if compute allows. |
| Does the method generalize beyond VisDrone? | Completed UAVDT baseline/static-P2 table; ScaleGate UAVDT only after complete | State that static P2 does not transfer under current UAVDT evidence. Claim adaptive-method robustness only if ScaleGate or later method supports it. | Complete ScaleGate UAVDT run and apply the post-result protocol. |
| Why not compare with more recent UAV small-object methods? | `paper/ieee_related_work_matrix.csv`, final fair comparison table | Separate reproduced baselines from literature-only reported methods and explain evaluation mismatch. | Add reproducible methods where code/data are stable, or make a literature-only context table. |
| How is small-object improvement measured? | `ieee_scale_results_visdrone.csv`, `ieee_scale_ap_results_visdrone.csv`, protocols | Explain GT scale grouping and local scale-bin AP definition; avoid calling it official AP-small. | Add an official-compatible AP-small evaluator if required. |
| Why does YOLO11s-960 outperform the lightweight model? | Main results, speed/complexity tables | Present YOLO11s as a capacity reference; argue lightweight trade-off, not absolute superiority. | Add a clearer deployment-cost discussion and maybe memory measurement. |
| Are the speed numbers fair? | `speed_results.csv`, benchmark protocol | State hardware, warm-up, sample count, and wall-clock timing protocol. | Repeat speed tests for final weights and include hardware details. |
| Can the code and results be reproduced? | GitHub repository, `paper/commands.md`, audits, configs | Point to configs, commands, logs, tables, and guarded result-integration protocol. | Clean final command list and release policy after advisor approval. |

## Response Evidence Map

| Evidence Type | Source |
| --- | --- |
| Main VisDrone metrics | `paper/tables/main_comparison_for_paper.csv` |
| Model complexity | `paper/tables/model_complexity.csv` |
| Speed / latency / FPS | `paper/tables/speed_results.csv` |
| Scale-wise recall/precision | `paper/tables/ieee_scale_results_visdrone.csv` |
| Local scale-bin AP | `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| Claim boundaries | `paper/ieee_claim_boundary.md` |
| T-ITS scope fit | `paper/ieee_tits_scope_fit_checklist.md` |
| Result intake rules | `paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md` |
| ScaleGate result gate | `paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md` |
| Method-selection rules | `paper/ieee_method_selection_protocol.md` |
| Server status | `paper/ieee_server_progress_report.md`, `paper/ieee_server_status_snapshot.md` |

## Draft Response Language Snippets

Use only if consistent with the final manuscript.

### Lightweight Trade-Off

> We agree that the larger YOLO11s model provides higher absolute accuracy. The objective of this work is not to claim that a nano-scale model dominates larger-capacity detectors, but to analyze and improve the accuracy-efficiency trade-off of lightweight UAV traffic-scene detectors under matched evaluation settings.

### CoordAttention Boundary

> We have revised the manuscript to treat CoordAttention as an ablation component. The completed experiments show that CoordAttention changes the precision-recall and scale-wise behavior, but it is not the main source of aggregate improvement under the 960-input P2 setting.

### Local Scale-Bin AP Boundary

> We clarify that the reported scale-bin AP is a local diagnostic computed from YOLO-format labels and prediction scale bins. It is not reported as official COCO AP-small or official VisDrone AP-small.

### Generalization Boundary

> We have limited the generalization claim to the datasets for which complete evidence is available. The completed UAVDT results show that the static P2 branch does not provide a transferable improvement under the current setting, so we use UAVDT as a validity-boundary test and only make adaptive-method claims when the corresponding complete results support them.

### Adaptive P2 Novelty Boundary

> We agree that a static P2 head and generic attention modules alone are incremental. The adaptive component is therefore evaluated under a separate evidence gate. We present ScaleAwareP2Gate as the final contribution only if it improves the matched baselines under aggregate, scale-wise, efficiency, and UAVDT checks; otherwise it remains an exploratory ablation and the manuscript claims are revised downward.

## Revision Package Checklist

When reviewer comments arrive:

| Item | Action |
| --- | --- |
| Response letter | Create a point-by-point response with reviewer numbering. |
| Revised manuscript diff | Track changes or provide a change summary as required by the target journal. |
| New experiment evidence | Add run directories, logs, tables, and audits before citing values. |
| Updated claim audit | Run `python tools/run_ieee_audits.py` and inspect `paper/ieee_claim_audit.md`. |
| Updated public repository | Push only polished, non-sensitive reproducibility materials. |
| Advisor review | Get advisor approval before resubmission. |

## Current Limitation

This response plan is preparatory. It cannot replace missing evidence for ScaleGate or any later adaptive method, official AP-small, or multi-seed stability.

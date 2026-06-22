# IEEE Route Next Actions

Status: current planning note. This file tracks the English IEEE route without treating the Chinese CEA route as abandoned. The two manuscript routes are parallel: the CEA route remains available for Chinese-journal submission, while the IEEE route requires a stronger method, broader evidence, and stricter claim control.

## Current Status

The English route has moved beyond packaging the static P2 result. Completed VisDrone and UAVDT evidence shows that high-resolution P2 prediction is useful in some VisDrone small-object diagnostics, but the static P2 trend does not transfer cleanly to UAVDT. The current method candidate is `ScaleAwareP2Gate`, which is implemented and running on the server but remains result-locked.

## Completed So Far

| Item | Status | Artifact |
| --- | --- | --- |
| IEEE master plan and target analysis | Done | `paper/IEEE_TRANS_SUBMISSION_PLAN.md`, `paper/ieee_target_journal_analysis.md` |
| Major-revision roadmap and core argument | Done | `paper/MAJOR_REVISION_ROADMAP.md`, `paper/reframed_core_argument.md` |
| VisDrone baseline/ablation evidence | Done | `paper/tables/main_comparison_for_paper.csv` |
| VisDrone speed/complexity evidence | Done for completed models | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` |
| VisDrone scale-wise diagnostics | Done for completed models | `paper/tables/ieee_scale_results_visdrone.csv`, `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| UAVDT conversion and four comparison runs | Done | `paper/tables/ieee_uavdt_results_for_paper.csv` |
| Static-P2 validity-boundary interpretation | Done | `paper/ieee_result_interpretation_matrix.md` |
| ScaleAwareP2Gate implementation | Done structurally | `src/models/attention/scale_aware_p2_gate.py`, `configs/models/yolo11n_p2_scalegate.yaml` |
| ScaleGate server queue | Launched | `paper/ieee_scalegate_server_launch_audit.md` |
| ScaleGate paper-use gate | Active, locked | `paper/ieee_scalegate_result_gate_audit.md` |
| ScaleGate method-decision gate | Active, locked | `paper/ieee_scalegate_method_decision_audit.md` |
| ScaleGate post-result dynamic runbook | Ready | `paper/ieee_scalegate_post_result_runbook.md` |
| ScaleGate guarded intake script | Ready | `tools/intake_ieee_scalegate_results.ps1` |
| IEEE advisor-review draft | Compiled, not final | `paper/ieee_trans/main_draft.tex`, `paper/ieee_trans/main_draft.pdf` |
| Advisor-draft shareability audit | Ready with author placeholders pending | `paper/ieee_draft_shareability_audit.md` |
| Non-result task closure audit | Ready | `paper/ieee_non_result_closure_audit.md` |
| IEEE goal readiness audit | Ready | `paper/ieee_goal_readiness_audit.md` |
| Audit/dashboard system | Active | `tools/run_ieee_audits.py`, `paper/ieee_submission_dashboard.md` |

## Tasks Not Waiting For New Results

1. Keep the IEEE draft wording evidence-bounded and avoid ScaleGate performance claims.
2. Keep target-journal, front-matter, citation, and metadata workbenches current.
3. Expand and verify related work only from reliable publisher/arXiv metadata.
4. Maintain the result-gate scripts and dashboard after any table or manuscript edit.
5. Preserve the CEA route as a parallel manuscript route, not as an old or abandoned project.
6. Run `python tools/check_ieee_draft_shareability.py` before sharing `paper/ieee_trans/main_draft.pdf`.
7. Run `python tools/check_ieee_non_result_closure.py` after non-result manuscript or audit edits; it should report zero missing items before pausing local work.
8. Run `python tools/check_ieee_goal_readiness.py` to confirm the local rest status is separated from true submission readiness.

## Tasks Waiting For ScaleGate Results

1. Wait for `yolo11n_p2_scalegate_960_visdrone` and `yolo11n_p2_scalegate_960_uavdt` to reach 100 epochs.
2. Prefer `tools/intake_ieee_scalegate_results.ps1` for guarded sync; it exits without copying if remote runs are incomplete.
3. Refresh `paper/ieee_scalegate_post_result_runbook.md` and follow only the allowed next command block.
4. Run `python tools/check_ieee_scalegate_result_gate.py`.
5. Refresh ScaleGate speed, complexity, scale-wise recall/precision, and local scale-bin AP.
6. Run `python tools/check_ieee_scalegate_method_decision.py`.
7. Apply `paper/ieee_method_selection_protocol.md` before changing title, abstract, contributions, conclusion, or cover letter.

## Do Not Do Yet

- Do not use partial ScaleGate metrics in any paper-facing result table.
- Do not claim ScaleGate improves VisDrone or fixes UAVDT before the result gate opens.
- Do not create final `paper/ieee_trans/main.tex` before target journal, final method route, references, and metadata are confirmed.
- Do not launch a second-cycle method from partial ScaleGate trends.

## Current Rest Point

The result-independent local package is now guarded by `paper/ieee_non_result_closure_audit.md` and `paper/ieee_goal_readiness_audit.md`. If they report `CLOSED_EXCEPT_RESULT_AND_MANUAL_GATES` and `RESTABLE_WAITING_FOR_EXPERIMENT_RESULTS`, the remaining work is intentionally limited to ScaleGate completion plus advisor/manual metadata confirmation. While the server is running, do not introduce new paper claims from partial results.

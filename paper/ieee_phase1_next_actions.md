# IEEE Route Next Actions

Status: current planning note. This file tracks the English IEEE route without treating the Chinese CEA route as abandoned. The two manuscript routes are parallel: the CEA route remains available for Chinese-journal submission, while the IEEE route requires a stronger method, broader evidence, and stricter claim control.

## Current Status

The English route has moved beyond packaging the static P2 result. Completed VisDrone and UAVDT evidence shows that high-resolution P2 prediction is useful in some VisDrone small-object diagnostics, but the static P2 trend does not transfer cleanly to UAVDT. `ScaleAwareP2Gate` is completed and rejected as the main method under the predeclared audit. The current method candidate is `CrossScaleP2P3ConsistencyGate`, which has complete VisDrone/UAVDT evidence and can be used only as a bounded partial-repair route.

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
| ScaleAwareP2Gate implementation and runs | Done; rejected as main method | `src/models/attention/scale_aware_p2_gate.py`, `configs/models/yolo11n_p2_scalegate.yaml`, `paper/ieee_scalegate_method_decision_audit.md` |
| CSGate implementation and runs | Done; bounded method candidate | `src/models/attention/cross_scale_p2_p3_gate.py`, `configs/models/yolo11n_p2_csgate.yaml`, `paper/ieee_csgate_method_decision_audit.md` |
| CSGate full100 UAVDT config | Done | `configs/train/yolo11n_p2_csgate_960_uavdt_full100.yaml` |
| ScaleGate paper-use gate | Open for mixed/negative evidence | `paper/ieee_scalegate_result_gate_audit.md` |
| ScaleGate method-decision gate | Done; reject main-method route | `paper/ieee_scalegate_method_decision_audit.md` |
| CSGate paper-use gate | Open for post-result integration | `paper/ieee_csgate_result_gate_audit.md` |
| CSGate method-decision gate | Done; accepts bounded routes B and C | `paper/ieee_csgate_method_decision_audit.md` |
| ScaleGate post-result dynamic runbook | Ready | `paper/ieee_scalegate_post_result_runbook.md` |
| ScaleGate guarded intake script | Ready | `tools/intake_ieee_scalegate_results.ps1` |
| IEEE advisor-review draft | Compiled, not final | `paper/ieee_trans/main_draft.tex`, `paper/ieee_trans/main_draft.pdf` |
| Advisor-draft shareability audit | Ready with author placeholders pending | `paper/ieee_draft_shareability_audit.md` |
| Non-result task closure audit | Ready | `paper/ieee_non_result_closure_audit.md` |
| IEEE goal readiness audit | Ready | `paper/ieee_goal_readiness_audit.md` |
| Audit/dashboard system | Active | `tools/run_ieee_audits.py`, `paper/ieee_submission_dashboard.md` |

## Tasks Not Waiting For New Results

1. Keep the IEEE draft wording evidence-bounded and avoid ScaleGate positive main-method claims.
2. Keep target-journal, front-matter, citation, and metadata workbenches current.
3. Expand and verify related work only from reliable publisher/arXiv metadata.
4. Maintain the result-gate scripts and dashboard after any table or manuscript edit.
5. Preserve the CEA route as a parallel manuscript route, not as an old or abandoned project.
6. Run `python tools/check_ieee_draft_shareability.py` before sharing `paper/ieee_trans/main_draft.pdf`.
7. Run `python tools/check_ieee_non_result_closure.py` after non-result manuscript or audit edits; it should report zero missing items before pausing local work.
8. Run `python tools/check_ieee_goal_readiness.py` to confirm the local rest status is separated from true submission readiness.

## Tasks Waiting For Manual Or Advisor Decisions

1. Confirm the exact IEEE Transactions target with the advisor.
2. Decide whether the bounded CSGate route is strong enough for that target or whether another method cycle is needed.
3. Confirm author order, affiliations, funding, code/data release policy, and acknowledgments.
4. Verify the final bibliography metadata and create final `references.bib`.
5. Review page budget and figure/table selection before creating final `main.tex`.

## Do Not Do Yet

- Do not use partial or early-stopped metrics in any paper-facing result table.
- Do not claim ScaleGate improves VisDrone or fixes UAVDT as a main-method result.
- Do not claim CSGate is SOTA or robust across datasets.
- Do not create final `paper/ieee_trans/main.tex` before target journal, final method route, references, and metadata are confirmed.
- Do not launch another method cycle unless the advisor agrees the bounded CSGate route is insufficient for the selected target.

## Current Rest Point

The result-independent local package is guarded by `paper/ieee_non_result_closure_audit.md` and `paper/ieee_goal_readiness_audit.md`. CSGate results are complete and integrated as bounded evidence. The remaining work is no longer waiting for this server run; it is focused on advisor decision, final target selection, final manuscript packaging, and possible next-cycle method design if the bounded CSGate route is judged insufficient.

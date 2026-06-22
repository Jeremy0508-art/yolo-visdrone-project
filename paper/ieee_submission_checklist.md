# IEEE Transactions Submission Checklist

Status: active checklist for the English IEEE route. This is not a submission-ready checklist yet; it defines what must be true before the project can become a formal IEEE Transactions submission.

## Scope And Ethics

| Item | Status | Evidence / Action |
| --- | --- | --- |
| Chinese CEA route preserved | Ready | CEA package remains a parallel route, not an abandoned project |
| Exact IEEE journal selected | Pending | Advisor must confirm T-ITS, TGRS, or another target |
| Target scope fit | Partial | Current framing is UAV-assisted traffic small-object detection; refine after final journal choice |
| Duplicate-submission risk checked | Pending | Do not submit Chinese and English versions simultaneously without advisor/publisher clearance |
| Original contribution defined | Pending ScaleGate evidence | Static P2 is not enough; final method depends on ScaleGate or a second-cycle design |
| All claims evidence-backed | Active gate | `paper/ieee_claim_boundary.md`, `paper/ieee_scalegate_result_gate_audit.md` |
| Non-result local tasks closed | Ready when audit is clean | `paper/ieee_non_result_closure_audit.md` |
| Rest/submission readiness separated | Ready when audit is clean | `paper/ieee_goal_readiness_audit.md` |

## Experiments

| Item | Status | Evidence / Action |
| --- | --- | --- |
| VisDrone baseline and ablations | Ready | Existing `runs/` and `paper/tables/` artifacts |
| UAVDT baseline/static-P2 comparison | Ready | `paper/tables/ieee_uavdt_results_for_paper.csv` |
| Static-P2 cross-dataset interpretation | Ready as boundary evidence | UAVDT blocks a transferable static-P2 superiority claim |
| ScaleGate VisDrone run | Pending server completion | Use only after 100 epochs and guarded sync |
| ScaleGate UAVDT run | Pending server completion | Use only after 100 epochs and guarded sync |
| ScaleGate result gate | Locked | `paper/ieee_scalegate_result_gate_audit.md` |
| ScaleGate method-decision gate | Locked | `paper/ieee_scalegate_method_decision_audit.md` |
| Scale-wise recall/precision | Ready for completed models | Refresh after ScaleGate weights are synced |
| Local scale-bin AP | Ready for completed models | Refresh after ScaleGate weights are synced |
| Speed/complexity | Ready for completed models | Refresh after ScaleGate weights are synced |
| Multi-seed stability | Conditional | Needed only if ScaleGate becomes a strong final method candidate |

## Manuscript

| Item | Status | Evidence / Action |
| --- | --- | --- |
| IEEEtran local draft build | Ready for advisor review | `paper/ieee_trans/main_draft.pdf` |
| Final IEEE `main.tex` | Locked | Do not create until `paper/ieee_trans/main_tex_preflight.md` passes |
| English abstract | Draft only | Final abstract must wait for final method route and exact metrics |
| Related work | Ready as outline, needs final verification | `paper/ieee_trans/related_work_outline.md`, `paper/ieee_trans/references_seed.bib` |
| Method section | Partially ready | ScaleGate structure and formulas are ready; performance claims locked |
| Results section | Partially ready | Completed VisDrone/UAVDT evidence ready; ScaleGate rows pending |
| Discussion and limitations | Partially ready | Must keep YOLO11s capacity boundary and UAVDT validity boundary |
| Cover letter | Workbench only | Final letter waits for target, authors, and final evidence |
| Non-result closure audit | Ready if zero missing | Confirms local non-result artifacts are in place and remaining blockers are result/manual gates |
| Goal readiness audit | Ready if zero missing | Confirms local work can pause without confusing that state with submission readiness |

## Submission Package

| Item | Status | Evidence / Action |
| --- | --- | --- |
| Main PDF | Pending final manuscript | Current PDF is advisor-review only |
| Source package | Pending | Include `.tex`, `.bib`, figures, generated tables after final route |
| Verified references | Pending final BibTeX | Seed metadata is audited but final `references.bib` is not created |
| Author metadata | Pending manual confirmation | Names, affiliations, funding, acknowledgments |
| Data/code availability statement | Pending manual confirmation | Coordinate GitHub release and dataset instructions |
| Suggested reviewers | Pending | Only if the selected journal requests them |

## Current Gate

The project is not ready for IEEE Transactions submission. The next hard gate is completion of the two ScaleGate runs, guarded sync, `paper/ieee_scalegate_result_gate_audit.md`, `paper/ieee_scalegate_method_decision_audit.md`, and method-selection review. `paper/ieee_non_result_closure_audit.md` records whether the local non-result work can be paused cleanly, and `paper/ieee_goal_readiness_audit.md` records the difference between local rest readiness and true submission readiness. Until then, the manuscript may be improved as an advisor-review draft, but final claims must stay locked.

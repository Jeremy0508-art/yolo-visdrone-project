# IEEE Transactions Submission Checklist

Status: active checklist for the English IEEE route. This is not a submission-ready checklist yet; it defines what must be true before the project can become a formal IEEE Transactions submission.

## Scope And Ethics

| Item | Status | Evidence / Action |
| --- | --- | --- |
| Chinese CEA route preserved | Ready | CEA package remains a parallel route, not an abandoned project |
| Exact IEEE journal selected | Pending | Advisor must confirm T-ITS, TGRS, or another target |
| Target scope fit | Partial | Current framing is UAV-assisted traffic small-object detection; refine after final journal choice |
| Duplicate-submission risk checked | Pending | Do not submit Chinese and English versions simultaneously without advisor/publisher clearance |
| Original contribution defined | Ready with bounded CSGate caveat | Static P2 and ScaleGate are insufficient; CSGate is the current partial-repair candidate |
| All claims evidence-backed | Active gate | `paper/ieee_claim_boundary.md`, `paper/ieee_csgate_method_decision_audit.md` |
| Non-result local tasks closed | Ready when audit is clean | `paper/ieee_non_result_closure_audit.md` |
| Rest/submission readiness separated | Ready when audit is clean | `paper/ieee_goal_readiness_audit.md` |

## Experiments

| Item | Status | Evidence / Action |
| --- | --- | --- |
| VisDrone baseline and ablations | Ready | Existing `runs/` and `paper/tables/` artifacts |
| UAVDT baseline/static-P2 comparison | Ready | `paper/tables/ieee_uavdt_results_for_paper.csv` |
| Static-P2 cross-dataset interpretation | Ready as boundary evidence | UAVDT blocks a transferable static-P2 superiority claim |
| ScaleGate VisDrone/UAVDT runs | Complete; rejected as main method | `paper/ieee_scalegate_method_decision_audit.md` |
| CSGate VisDrone/UAVDT runs | Complete; bounded method candidate | `paper/ieee_csgate_method_decision_audit.md` |
| ScaleGate result gate | Open | `paper/ieee_scalegate_result_gate_audit.md` |
| CSGate result gate | Open | `paper/ieee_csgate_result_gate_audit.md` |
| Scale-wise recall/precision | Ready for completed models | Includes CSGate and ScaleGate rows |
| Local scale-bin AP | Ready for completed models | Includes CSGate and ScaleGate rows |
| Speed/complexity | Ready for completed models | Includes CSGate and ScaleGate rows |
| Multi-seed stability | Conditional | Needed only if advisor wants to strengthen the bounded CSGate claim |

## Manuscript

| Item | Status | Evidence / Action |
| --- | --- | --- |
| IEEEtran local draft build | Ready for advisor review | `paper/ieee_trans/main_draft.pdf` |
| Final IEEE `main.tex` | Locked | Do not create until `paper/ieee_trans/main_tex_preflight.md` passes |
| English abstract | Draft only | Final abstract must wait for target journal and manual metadata; exact metrics are audited in current draft |
| Related work | Ready as outline, needs final verification | `paper/ieee_trans/related_work_outline.md`, `paper/ieee_trans/references_seed.bib` |
| Method section | Ready for advisor draft | ScaleGate is negative/mixed evidence; CSGate is bounded method candidate |
| Results section | Ready for advisor draft | Completed VisDrone/UAVDT evidence includes ScaleGate and CSGate |
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

The project is not ready for IEEE Transactions submission. The experiment gate is closed for the current ScaleGate/CSGate route, but the final hard gates are target-journal confirmation, author/funding/code-data metadata, verified `references.bib`, page-budget decisions, and final source-package assembly. `paper/ieee_goal_readiness_audit.md` records the difference between local rest readiness and true submission readiness.

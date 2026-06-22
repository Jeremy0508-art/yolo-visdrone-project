# IEEE Manuscript Assembly Checklist

Status: planning and assembly guide. This is not the final IEEE manuscript.

This checklist defines when each draft component can be moved into a future IEEEtran `main.tex`. It is meant to prevent incomplete experiments from leaking into final-facing claims.

## Assembly Principle

The manuscript should be assembled in this order:

1. Evidence tables and audit reports.
2. Results and discussion paragraphs.
3. Method naming and contribution list.
4. Abstract and conclusion.
5. Cover letter and submission metadata.

The abstract, title, and conclusion must be written last because they are the most likely places to overclaim.

## Current Manuscript Inputs

| Input | Status | Use in Future `main.tex` |
| --- | --- | --- |
| `manuscript_blueprint.md` | Ready | Section structure and contribution boundary |
| `section_draft_pack.md` | Ready | Evidence-bounded English paragraphs |
| `scalegate_method_section_draft.md` | Ready as mixed/negative ablation text | Formula-level ScaleAwareP2Gate description with completed rejection boundary |
| `csgate_method_section_draft.md` | Ready as result-locked design text | Formula-level CSGate description; no performance claim |
| `novelty_positioning_workbench.md` | Ready | Contribution positioning against recent UAV YOLO work |
| `abstract_contribution_workbench.md` | Ready | Safe abstract skeleton and locked placeholders |
| `title_abstract_index_terms_workbench.md` | Ready | T-ITS front-matter constraints and locked title/index-term options |
| `submission_metadata_workbench.md` | Ready | Author, funding, code/data, and submission-system metadata checklist |
| `../ieee_front_matter_audit.md` | Ready with one pending final-length item | T-ITS title, abstract, index-term, and metadata guard |
| `../ieee_dataset_license_audit.md` | Ready as planning | Dataset citation, license, and repository-release boundary notes |
| `../ieee_dataset_compliance_audit.md` | Ready with final human confirmation pending | Dataset/code-release boundary guard before final package assembly |
| `cover_letter_workbench.md` | Ready | Cover letter skeleton and ethics/claim boundaries |
| `related_work_outline.md` | Ready | Related-work structure |
| `page_budget_plan.md` | Ready | T-ITS Regular Paper page budget and main-paper table/figure selection |
| `references_seed.bib` | Ready for planning | Seed citations only; verify metadata before final BibTeX |
| `../ieee_number_trace_audit.md` | Ready | Numeric trace audit for the current English draft pack |
| `../ieee_main_draft_number_audit.md` | Ready | Decimal-number trace audit for the current advisor-review draft |
| `../ieee_draft_shareability_audit.md` | Ready with author placeholders pending | Advisor-review draft can be shared as non-final; not a submission package |
| `../ieee_non_result_closure_audit.md` | Ready | Confirms non-result local work is closed except experiment/manual gates |
| `tables/visdrone_main_results.tex` | Ready for current evidence route | Main VisDrone table |
| `tables/speed_complexity.tex` | Ready for existing models | Refresh after final model |
| `tables/scale_recall_precision.tex` | Ready for completed VisDrone models | Recall/precision only |
| `tools/evaluate_scale_ap.py` | Ready as optional evaluator | Full local scale-bin AP output is available |
| `figure_source_manifest.md` | Ready | Candidate figure source tracking |
| `../IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md` | Ready | Required sync, speed, scale-diagnostic, and manuscript-update steps after ScaleGate finishes |
| `../ieee_scalegate_post_result_runbook.md` | Ready | Current-state command gate for ScaleGate result intake |
| `../../tools/intake_ieee_scalegate_results.ps1` | Ready | Safe single entry point for ScaleGate status refresh, guarded sync, optional diagnostics, and audit refresh |
| `../../tools/set_ieee_scalegate_scale_target.py` | Ready | Enables ScaleGate scale diagnostics only after local complete-run artifacts exist |
| `../ieee_scalegate_result_gate_audit.md` | Ready | Generated lock for whether ScaleGate rows, diagnostics, speed, and claims may enter paper-facing text |
| `../ieee_scalegate_method_decision_audit.md` | Ready | Generated A/B/C acceptance-route decision; ScaleGate is rejected as the main method |

## Section Unlock Matrix

| Section | Current Draft Source | Current Status | Unlock Condition for Final `main.tex` |
| --- | --- | --- | --- |
| Title | `manuscript_blueprint.md` | Locked | Final method route selected from real results |
| Abstract | `main_draft.tex`, `title_abstract_index_terms_workbench.md` | Ready for current draft | Static-P2 UAVDT decision complete; final abstract still waits for ScaleGate or second-cycle method decision |
| Introduction | `section_draft_pack.md` | Partially ready | Contributions rewritten after final method selection and ScaleGate decision |
| Related Work | `related_work_outline.md`, `references_seed.bib` | Partially ready | Citation metadata verified; 25-row matrix reviewed |
| Method Overview | `section_draft_pack.md`, `scalegate_method_section_draft.md`, `csgate_method_section_draft.md` | Partially ready | Final architecture selected from completed audited evidence |
| P2 Branch Description | `section_draft_pack.md` | Ready | Use as structural description with complexity values |
| CoordAttention Description | `section_draft_pack.md` | Ready as ablation | Keep wording auxiliary unless later evidence changes |
| TOFC Description | `section_draft_pack.md` | Ready as ablation with caveat | Keep as completed VisDrone calibration candidate, not final method |
| ScaleAwareP2Gate Description | `scalegate_method_section_draft.md` | Ready as completed mixed/negative evidence | Use only as an ablation/failure-mode discussion, not as the proposed method |
| CSGate Description | `csgate_method_section_draft.md` | Ready as structure; result-locked | Use structure and formula only until completed VisDrone/UAVDT runs are synced and audited |
| Dataset/Implementation | `section_draft_pack.md` | Partially ready | Add verified server environment and UAVDT conversion statistics |
| VisDrone Results | `section_draft_pack.md`, generated tables | Ready for existing evidence | Copy exact values from generated tables only |
| UAVDT Results | `tables/uavdt_results.tex` | Ready as validity-boundary evidence | Do not claim transferable P2 improvement |
| Scale-wise Analysis | `section_draft_pack.md`, `scale_recall_precision.tex` | Ready for recall/precision | Do not call this AP-small unless AP evaluator is added |
| Local Scale-Bin AP Analysis | `tools/evaluate_scale_ap.py`, `scale_bin_ap.tex` | Ready as local diagnostic | Do not describe as official COCO or VisDrone AP-small |
| Efficiency Analysis | `section_draft_pack.md`, `speed_complexity.tex` | Ready for existing models | Refresh after final method weights arrive |
| Discussion | `main_draft.tex` | Ready for current draft | UAVDT outcome added as dataset-validity boundary; revise again after ScaleGate result |
| Conclusion | `main_draft.tex` | Ready for current draft | Keep cautious; final wording depends on ScaleGate result, target journal, and advisor route |
| Cover Letter | `cover_letter_workbench.md` | Locked | Target journal, article type, author metadata, and final evidence are confirmed |

## Result Intake Checklist

When a new completed run arrives from the server:

1. Copy only complete run artifacts.
2. Verify `results.csv`, `args.yaml`, `weights/best.pt`, and a matching log.
3. Update or regenerate source CSV files under `paper/tables/`.
4. Regenerate IEEE table drafts with `tools/export_ieee_tables.py`.
5. Re-run scale-wise evaluation if the new run is a final-method candidate.
6. Re-run speed and complexity measurements for the new weight.
7. Run `python tools/run_ieee_audits.py`.
8. Run `python tools/check_ieee_main_draft_numbers.py` after editing `main_draft.tex` numeric text.
9. Run `python tools/check_ieee_draft_shareability.py` before sharing a refreshed advisor-review PDF.
10. Update `section_draft_pack.md` only after the audit confirms the new evidence.
11. Update abstract and conclusion last.

For ScaleGate specifically, the result gate is open but the method-decision
audit rejects it as the main method. ScaleGate metrics may be used only as
mixed/negative ablation evidence. For CSGate, wait for complete VisDrone and
UAVDT runs before exporting rows, regenerating diagnostics, refreshing speed,
or changing the title, abstract, contribution list, or conclusion.

## Final `main.tex` Creation Gate

Create `paper/ieee_trans/main.tex` only when all of the following are true:

| Gate | Current Status | Evidence Needed |
| --- | --- | --- |
| Target IEEE Transactions journal selected | Pending | Advisor confirms T-ITS, TGRS, or another exact journal |
| Page budget plan reviewed | Ready as planning | `page_budget_plan.md`; update after final ScaleGate/result selection |
| Front matter audit passes | Ready as planning | Final abstract length remains pending until final evidence exists |
| Final main method selected | Pending CSGate evidence | Choose CSGate, a later method, or boundary-analysis route from real metrics |
| ScaleGate paper-use gate | Ready for mixed/negative evidence | `../ieee_scalegate_result_gate_audit.md` reports `OPEN_FOR_POST_RESULT_INTEGRATION` |
| ScaleGate method-decision audit | Ready; rejected as main method | `../ieee_scalegate_method_decision_audit.md` reports no accepted route |
| VisDrone final result table complete | Ready for current evidence | Existing generated table, refreshed after final model |
| Cross-dataset evidence available | Ready for static-P2 and ScaleGate boundary; pending for CSGate | UAVDT completed rows exported for existing routes; CSGate UAVDT queued |
| Speed/complexity refreshed for final model | Pending CSGate evidence | Refresh after final method weights arrive |
| Number trace audit passes | Ready for current draft pack | Zero non-ready numeric claims before moving draft text into `main.tex` |
| Main draft number audit passes | Ready for current advisor draft | `../ieee_main_draft_number_audit.md` has zero missing decimal traces |
| Advisor-draft shareability check passes | Ready with author placeholders pending | `../ieee_draft_shareability_audit.md` has no missing issues |
| Non-result closure audit passes | Ready if zero missing | `../ieee_non_result_closure_audit.md` reports no missing result-independent items |
| Claim audit passes | Pending | `paper/ieee_claim_audit.md` after final-facing files exist |
| Reference metadata verified | Pending | Final `references.bib` from verified entries |
| Dataset/code release boundary verified | Pending final human confirmation | `../ieee_dataset_compliance_audit.md` plus advisor/institution review |

## Figure Assembly Rules

- Use English labels only.
- Do not use screenshots from the CEA Word document.
- Do not include figures whose captions imply unverified improvements.
- Keep qualitative figures tied to the exact model and weight used.
- Regenerate method overview only after the final architecture is selected.

## Safe Current Manuscript Route

Given the current UAVDT evidence, the safe IEEE route before ScaleGate completion is:

> A reproducible high-resolution lightweight YOLO study for UAV small-object detection, centered on P2 prediction, input resolution, scale-wise recall/precision, accuracy-efficiency trade-offs, and dataset-validity boundaries.

If ScaleGate or a later adaptive method is validated, the stronger route can be reconsidered:

> An adaptive high-resolution lightweight YOLO detector for UAV traffic small-object detection, validated through VisDrone, UAVDT, scale-wise analysis, and efficiency measurements.

Both routes require honest comparison against YOLO11s-960.

## Daily Resume Procedure

Use this sequence when resuming after an interruption:

1. `git status --short`
2. `python tools/run_ieee_audits.py`
3. Inspect `paper/ieee_submission_dashboard.md`
4. Inspect `paper/ieee_front_matter_audit.md` before moving title/abstract/index terms
5. Inspect `paper/ieee_number_trace_audit.md` before moving any numerical paragraph
6. Inspect `paper/ieee_main_draft_number_audit.md` before sharing `main_draft.pdf`
7. Inspect `paper/ieee_draft_shareability_audit.md` before sharing `main_draft.pdf`
8. Inspect `paper/ieee_non_result_closure_audit.md` before pausing local work while experiments run
9. Inspect `paper/ieee_dataset_compliance_audit.md` before drafting data/code availability wording
10. Check server status only if SSH access is stable
11. Integrate complete results only through `paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md` and `paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md`

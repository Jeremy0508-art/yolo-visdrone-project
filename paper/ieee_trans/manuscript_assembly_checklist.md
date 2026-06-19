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
| `abstract_contribution_workbench.md` | Ready | Safe abstract skeleton and locked placeholders |
| `title_abstract_index_terms_workbench.md` | Ready | T-ITS front-matter constraints and locked title/index-term options |
| `submission_metadata_workbench.md` | Ready | Author, funding, code/data, and submission-system metadata checklist |
| `../ieee_front_matter_audit.md` | Ready with one pending final-length item | T-ITS title, abstract, index-term, and metadata guard |
| `cover_letter_workbench.md` | Ready | Cover letter skeleton and ethics/claim boundaries |
| `related_work_outline.md` | Ready | Related-work structure |
| `page_budget_plan.md` | Ready | T-ITS Regular Paper page budget and main-paper table/figure selection |
| `references_seed.bib` | Ready for planning | Seed citations only; verify metadata before final BibTeX |
| `../ieee_number_trace_audit.md` | Ready | Numeric trace audit for the current English draft pack |
| `tables/visdrone_main_results.tex` | Ready for current evidence route | Main VisDrone table |
| `tables/speed_complexity.tex` | Ready for existing models | Refresh after final model |
| `tables/scale_recall_precision.tex` | Ready for completed VisDrone models | Recall/precision only |
| `tools/evaluate_scale_ap.py` | Ready as optional evaluator | Full local scale-bin AP output is available |
| `figure_source_manifest.md` | Ready | Candidate figure source tracking |

## Section Unlock Matrix

| Section | Current Draft Source | Current Status | Unlock Condition for Final `main.tex` |
| --- | --- | --- | --- |
| Title | `manuscript_blueprint.md` | Locked | Final method route selected from real results |
| Abstract | `abstract_contribution_workbench.md`, `title_abstract_index_terms_workbench.md` | Locked | TOFC/UAVDT decision complete; exact numbers audited |
| Introduction | `section_draft_pack.md` | Partially ready | Contributions rewritten after final method selection |
| Related Work | `related_work_outline.md`, `references_seed.bib` | Partially ready | Citation metadata verified; 25-row matrix reviewed |
| Method Overview | `section_draft_pack.md` | Partially ready | Final architecture selected; TOFC included only if validated |
| P2 Branch Description | `section_draft_pack.md` | Ready | Use as structural description with complexity values |
| CoordAttention Description | `section_draft_pack.md` | Ready as ablation | Keep wording auxiliary unless later evidence changes |
| TOFC Description | `section_draft_pack.md` | Locked | Full TOFC run, speed, complexity, and scale-wise outputs exist |
| Dataset/Implementation | `section_draft_pack.md` | Partially ready | Add verified server environment and UAVDT conversion statistics |
| VisDrone Results | `section_draft_pack.md`, generated tables | Ready for existing evidence | Copy exact values from generated tables only |
| UAVDT Results | none | Locked | Converted dataset plus completed baseline/method runs |
| Scale-wise Analysis | `section_draft_pack.md`, `scale_recall_precision.tex` | Ready for recall/precision | Do not call this AP-small unless AP evaluator is added |
| Local Scale-Bin AP Analysis | `tools/evaluate_scale_ap.py`, `scale_bin_ap.tex` | Ready as local diagnostic | Do not describe as official COCO or VisDrone AP-small |
| Efficiency Analysis | `section_draft_pack.md`, `speed_complexity.tex` | Ready for existing models | Refresh after final method weights arrive |
| Discussion | `section_draft_pack.md` | Partially ready | Add TOFC/UAVDT outcomes and limitations |
| Conclusion | `section_draft_pack.md` | Locked | Write last after all accepted evidence is known |
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
8. Update `section_draft_pack.md` only after the audit confirms the new evidence.
9. Update abstract and conclusion last.

## Final `main.tex` Creation Gate

Create `paper/ieee_trans/main.tex` only when all of the following are true:

| Gate | Current Status | Evidence Needed |
| --- | --- | --- |
| Target IEEE Transactions journal selected | Pending | Advisor confirms T-ITS, TGRS, or another exact journal |
| Page budget plan reviewed | Ready as planning | `page_budget_plan.md`; update after final TOFC/UAVDT result selection |
| Front matter audit passes | Ready as planning | Final abstract length remains pending until final evidence exists |
| Final main method selected | Pending | TOFC or fallback route chosen from real metrics |
| VisDrone final result table complete | Ready for current evidence | Existing generated table, refreshed after final model |
| Cross-dataset evidence available | Pending | UAVDT conversion and completed runs |
| Speed/complexity refreshed for final model | Pending | New rows after final-model weights arrive |
| Number trace audit passes | Ready for current draft pack | Zero non-ready numeric claims before moving draft text into `main.tex` |
| Claim audit passes | Pending | `paper/ieee_claim_audit.md` after final-facing files exist |
| Reference metadata verified | Pending | Final `references.bib` from verified entries |

## Figure Assembly Rules

- Use English labels only.
- Do not use screenshots from the CEA Word document.
- Do not include figures whose captions imply unverified improvements.
- Keep qualitative figures tied to the exact model and weight used.
- Regenerate method overview only after the final architecture is selected.

## Safe Current Manuscript Route

If TOFC does not become a validated improvement, the safe IEEE route is:

> A reproducible high-resolution lightweight YOLO study for UAV small-object detection, centered on P2 prediction, input resolution, scale-wise recall/precision, and accuracy-efficiency trade-offs.

If TOFC does become a validated improvement, the stronger route is:

> A TOFC-enhanced lightweight YOLO11n detector for UAV traffic small-object detection, validated through VisDrone, cross-dataset evidence, scale-wise analysis, and efficiency measurements.

Both routes require honest comparison against YOLO11s-960.

## Daily Resume Procedure

Use this sequence when resuming after an interruption:

1. `git status --short`
2. `python tools/run_ieee_audits.py`
3. Inspect `paper/ieee_submission_dashboard.md`
4. Inspect `paper/ieee_front_matter_audit.md` before moving title/abstract/index terms
5. Inspect `paper/ieee_number_trace_audit.md` before moving any numerical paragraph
6. Check server status only if SSH access is stable
7. Integrate complete results only through `paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md`

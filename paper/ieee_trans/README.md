# IEEE Transactions Manuscript Workspace

This directory is reserved for the future IEEE Transactions English manuscript.

The manuscript should not be drafted as a direct translation of the CEA Chinese manuscript. The CEA manuscript remains part of the Chinese-journal route, while this directory keeps the separate IEEE English-journal route. The IEEE manuscript should be created only after the core IEEE evidence gates are satisfied:

1. Target journal direction is confirmed.
2. UAVDT or another second dataset is converted and validated.
3. The final main method is selected from real experiment results.
4. Scale-wise small-object metrics are available.
5. Claims are traceable to logs, CSV files, or official evaluation results.

## Planned Files

| File | Purpose | Status |
| --- | --- | --- |
| `manuscript_blueprint.md` | Evidence-bounded IEEE manuscript plan | Ready |
| `abstract_contribution_workbench.md` | Safe and locked abstract/contribution wording | Ready |
| `title_abstract_index_terms_workbench.md` | T-ITS title, abstract, and index terms workbench | Ready |
| `submission_metadata_workbench.md` | Author, funding, code/data, and submission metadata worksheet | Ready |
| `related_work_outline.md` | IEEE related-work section outline and citation logic | Ready |
| `novelty_positioning_workbench.md` | Novelty pressure and contribution-positioning guardrail | Ready |
| `section_draft_pack.md` | Evidence-bounded English section drafts for future IEEE manuscript assembly | Ready |
| `scalegate_method_section_draft.md` | Formula-level ScaleAwareP2Gate description with completed mixed/negative claim lock | Ready |
| `csgate_method_section_draft.md` | Formula-level CSGate second-cycle method description with result lock | Ready |
| `manuscript_assembly_checklist.md` | Gates and order for assembling a future IEEEtran manuscript | Ready |
| `main_tex_preflight.md` | Preflight checklist before creating final-facing IEEEtran `main.tex` | Ready |
| `page_budget_plan.md` | T-ITS Regular Paper page budget and main-paper table/figure selection plan | Ready |
| `references_seed.bib` | Seed bibliography for IEEE planning | Ready |
| `citation_plan.md` | Citation role mapping and verification notes | Ready |
| `evidence_to_sections.csv` | Claim/content-to-evidence mapping for sections | Ready |
| `table_figure_plan.md` | IEEE table and figure plan with readiness gates | Ready |
| `figure_source_manifest.md` | Figure candidates, source paths, and evidence boundaries | Ready |
| `main_draft.tex` | Evidence-bounded IEEE draft for advisor review; not submission-ready | Ready |
| `../ieee_draft_shareability_audit.md` | Generated check that the advisor-review PDF has no unsupported claims or obvious placeholders beyond approved pending metadata | Ready |
| `../ieee_main_draft_number_audit.md` | Generated trace check for decimal values in `main_draft.tex` | Ready |
| `../ieee_non_result_closure_audit.md` | Generated check that non-result local work is closed except experiment/manual gates | Ready |
| `../ieee_goal_readiness_audit.md` | Generated high-level check that separates local rest readiness from true submission readiness | Ready |
| `uavdt_result_integration.md` | UAVDT sync/export/manuscript gate for cross-dataset results | Ready |
| `post_uavdt_rewrite_checklist.md` | Ordered rewrite checklist after complete UAVDT results are audited | Ready |
| `reproducibility_notes.md` | Build, table-generation, audit, and evidence-flow notes for the IEEE draft | Ready |
| `../MAJOR_REVISION_ROADMAP.md` | Shared major-revision roadmap for converting reports into paper-style manuscripts | Ready |
| `../reframed_core_argument.md` | Shared core argument for Chinese and English manuscript rewriting | Ready |
| `../dual_track_reframed_manuscript_strategy.md` | Chinese-journal and English-extension narrative alignment | Ready |
| `../tables/reframed_evidence_matrix.csv` | Evidence matrix that maps existing results to paper claims and boundaries | Ready |
| `../major_revision_completion_audit.md` | Completion audit for the major-revision design-layer rewrite and PDF build check | Ready |
| `../ieee_uavdt_integration_audit.md` | Completion audit for UAVDT result sync, table export, interpretation, and PDF checks | Ready |
| `../IEEE_TRANS_METHOD_REDESIGN_PLAN.md` | New adaptive-method route after the static P2 boundary was identified | Ready |
| `../IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md` | Exact sync, table, scale-diagnostic, speed, and manuscript-update steps used for ScaleGate integration | Ready |
| `../IEEE_CSGATE_POST_RESULT_PROTOCOL.md` | Exact sync, table, diagnostic, speed, and manuscript-update steps after CSGate finishes | Ready |
| `../ieee_scalegate_post_result_runbook.md` | Generated current-state command gate for ScaleGate result intake | Ready |
| `../../tools/intake_ieee_scalegate_results.ps1` | Single guarded ScaleGate result-intake entry point | Ready |
| `../../tools/set_ieee_scalegate_scale_target.py` | Guarded helper for enabling ScaleGate scale diagnostics after complete local sync | Ready |
| `../ieee_scalegate_result_gate_audit.md` | Generated paper-use gate for ScaleGate runs, tables, diagnostics, speed, and draft claims | Ready |
| `../ieee_scalegate_method_decision_audit.md` | Generated A/B/C acceptance-route decision; ScaleGate is rejected as the main method | Ready |
| `../IEEE_SECOND_CYCLE_METHOD_BACKLOG.md` | Evidence-triggered backup method designs if ScaleGate is not strong enough | Ready |
| `../../tools/intake_ieee_csgate_results.ps1` | Single guarded CSGate result-intake entry point | Ready |
| `../../tools/set_ieee_scale_target.py` | Generic helper for enabling scale diagnostics after complete local sync | Ready |
| `main.tex` | IEEEtran manuscript source | Pending |
| `references.bib` | IEEE-style bibliography | Pending |
| `figures/` | English manuscript figures | Pending |
| `tables/` | Generated LaTeX table drafts and source manifest | Ready |
| `cover_letter_workbench.md` | Evidence-bounded cover letter planning skeleton | Ready |
| `cover_letter_draft.md` | Final cover letter draft | Pending |

## Local Draft Compilation

The advisor-review draft can be compiled from the project root with the repo-local Tectonic binary:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\build_paper_pdf.ps1 -TexFile paper\ieee_trans\main_draft.tex -OutDir paper\ieee_trans
```

The files `IEEEtran.cls`, `IEEEtran.bst`, `cite.sty`, `TS1cmr.fd`, and `cmsy7.pfb` are kept locally so that the IEEE draft can compile even when Tectonic cannot download missing template or font resources.

## Related External Audits

| File | Purpose |
| --- | --- |
| `../ieee_tits_scope_fit_checklist.md` | T-ITS scope and traffic-sensing framing checklist |
| `../ieee_tits_author_requirements_audit.md` | Official-source T-ITS submission, abstract, keyword, and page-format requirements |
| `../ieee_front_matter_audit.md` | Generated guard for T-ITS title, abstract, index terms, and metadata workbenches |
| `../ieee_number_trace_audit.md` | Numeric trace audit for values in `section_draft_pack.md` |
| `../ieee_main_draft_number_audit.md` | Numeric trace audit for decimal values in `main_draft.tex` |
| `../ieee_reference_metadata_readiness_audit.md` | Stricter planning-stage check for seed BibTeX metadata readiness |
| `../ieee_scalegate_result_gate_audit.md` | Generated lock that prevents partial ScaleGate evidence from entering paper-facing claims |
| `../ieee_scalegate_method_decision_audit.md` | Generated method-selection guardrail after the ScaleGate result gate opens |
| `../ieee_csgate_result_gate_audit.md` | Generated lock that prevents partial CSGate evidence from entering paper-facing claims |
| `../ieee_csgate_method_decision_audit.md` | Generated method-selection guardrail after the CSGate result gate opens |
| `../ieee_result_interpretation_matrix.md` | Evidence-bounded result-reading matrix for IEEE manuscript wording |
| `../ieee_result_interpretation_matrix_audit.md` | Generated check for the IEEE result interpretation matrix |
| `../ieee_evidence_map_audit.md` | Generated check for the IEEE evidence-to-section map |
| `../ieee_manuscript_assembly_audit.md` | Generated check for IEEE manuscript assembly inputs and final-source locks |
| `../ieee_draft_shareability_audit.md` | Generated advisor-review draft shareability check |
| `../ieee_non_result_closure_audit.md` | Generated rest-point audit for non-result local tasks |
| `../ieee_dataset_license_audit.md` | Dataset license, citation, and repository-release boundary notes |
| `../ieee_dataset_compliance_audit.md` | Generated check for dataset boundary, seed citations, and submission-metadata wording |
| `../datasets/uavdt_conversion_readiness_audit.md` | Generated local audit and synthetic conversion smoke test for UAVDT preparation |
| `../ieee_server_resume_runbook.md` | Safe server restart, launch, monitoring, and sync procedure for IEEE experiments |
| `../IEEE_TRANS_METHOD_REDESIGN_PLAN.md` | ScaleAwareP2Gate design, claim gates, and required experiment matrix |
| `../IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md` | Post-result integration protocol for completed ScaleGate runs |
| `../IEEE_CSGATE_POST_RESULT_PROTOCOL.md` | Post-result integration protocol for CSGate complete runs |
| `../ieee_scalegate_post_result_runbook.md` | Current-state runbook for the next allowed ScaleGate intake command |
| `../../tools/intake_ieee_scalegate_results.ps1` | Safe wrapper for status refresh, guarded sync, optional diagnostics, and audit refresh |
| `../../tools/intake_ieee_csgate_results.ps1` | Safe wrapper for CSGate status refresh, guarded sync, optional diagnostics, and audit refresh |
| `../../tools/set_ieee_scale_target.py` | Generic scale-diagnostic target enabler for post-result model rows |
| `../IEEE_SECOND_CYCLE_METHOD_BACKLOG.md` | Failure-mode-driven second-cycle method backlog after ScaleGate |
| `../ieee_goal_readiness_audit.md` | High-level rest/submission readiness audit for the IEEE objective |
| `../ieee_submission_dashboard.md` | Current IEEE readiness dashboard |

## Current Rule

Do not add a final-looking IEEE manuscript until experiments support the main claims. Placeholder drafts are allowed only if clearly marked as planning drafts.

`main_draft.tex` is the current advisor-review draft. It must not be renamed to `main.tex` until the CSGate result gate, target-journal metadata, and final method route are resolved through `main_tex_preflight.md`.

## Local Audit Command

From the project root, refresh all local IEEE planning audits and generated table drafts with:

```powershell
python tools\run_ieee_audits.py
```

This command does not launch training and does not connect to the server.

After result-independent edits, check `../ieee_non_result_closure_audit.md` and `../ieee_goal_readiness_audit.md`. A `CLOSED_EXCEPT_RESULT_AND_MANUAL_GATES` closure plus `OPEN_SECOND_CYCLE_EXPERIMENTS` status means the local non-result work can pause cleanly while CSGate results and advisor/manual metadata remain pending.

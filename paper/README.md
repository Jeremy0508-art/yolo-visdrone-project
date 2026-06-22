# Paper Workspace

This directory contains the paper-facing materials for the YOLO VisDrone project.

The repository-level overview is maintained in `../README.md`. Use this file for paper-specific navigation, evidence rules, and rebuild commands.

## Current Paper Routes

This project currently keeps two active paper routes:

1. A Chinese-journal route for venues such as 《计算机工程与应用》.
2. An IEEE Transactions English-journal route.

The two routes share the same reproducible experiment evidence, but they are maintained as separate manuscripts because their audience, language, template, narrative structure, and submission requirements differ.

Current IEEE dashboard:

```text
paper/ieee_submission_dashboard.md
```

Current IEEE manuscript workspace:

```text
paper/ieee_trans/
```

Do not treat the CEA PDF or Word draft as the IEEE submission manuscript. A final IEEE `main.tex` should be created only after the gates in `paper/ieee_trans/main_tex_preflight.md` pass.

Do not treat the CEA materials as abandoned or merely historical. They remain part of the Chinese-journal submission route and should be updated when the Chinese submission package is resumed.

## Major-Revision Framing

The current manuscript direction has been reframed from a progress-report style module comparison into a paper-style study of high-resolution prediction for lightweight UAV small-object detection. The shared core argument is:

```text
High-resolution input and shallow P2 prediction can improve lightweight YOLO small-object diagnostics, but the benefit must be discussed together with computational cost, object scale, model capacity, and cross-dataset validity boundaries.
```

The major-revision control files are:

| File | Purpose |
| --- | --- |
| `MAJOR_REVISION_ROADMAP.md` | Why the old report-style manuscript must be rewritten and how the new paper structure works |
| `reframed_core_argument.md` | Shared central claim for the Chinese-journal and English-extension manuscripts |
| `dual_track_reframed_manuscript_strategy.md` | How the Chinese and English routes share evidence while keeping different manuscript narratives |
| `tables/reframed_evidence_matrix.csv` | Maps completed experiments to supported claims, unsupported claims, and manuscript roles |
| `major_revision_completion_audit.md` | Records the completed design-layer rewrite, PDF build check, and remaining UAVDT integration gates |
| `ieee_uavdt_integration_audit.md` | Records synced UAVDT evidence, paper-facing values, validity-boundary interpretation, and PDF checks |

## IEEE Route Files

| File | Purpose |
| --- | --- |
| `IEEE_TRANS_SUBMISSION_PLAN.md` | Master plan for the IEEE Transactions route |
| `ieee_submission_dashboard.md` | One-page readiness dashboard for the IEEE route |
| `ieee_target_journal_analysis.md` | Target-journal fit analysis, with T-ITS as the leading direction |
| `ieee_tits_scope_fit_checklist.md` | T-ITS-specific scope and manuscript-framing checklist |
| `ieee_tits_author_requirements_audit.md` | Official-source T-ITS submission, abstract, keyword, and page-format checklist |
| `ieee_required_experiment_gap.md` | Experiment and evidence gaps for an IEEE-level paper |
| `ieee_method_design_notes.md` | Candidate method notes, including TOFC |
| `ieee_method_selection_protocol.md` | Decision protocol for selecting the final method after real results arrive |
| `ieee_result_interpretation_matrix.md` | Evidence-bounded result-reading matrix for IEEE manuscript wording |
| `ieee_result_interpretation_matrix_audit.md` | Generated check for the IEEE result interpretation matrix |
| `ieee_claim_boundary.md` | Claim rules and locked/allowed wording |
| `ieee_reviewer_risk_register.md` | Reviewer-risk register and mitigation plan |
| `ieee_trans_response_plan.md` | Preparatory response plan for likely IEEE reviewer concerns |
| `ieee_reference_gap_report.md` | Reference coverage and pending recent-method citation gaps |
| `ieee_reference_metadata_readiness_audit.md` | Generated stricter planning-stage check for seed BibTeX metadata readiness |
| `ieee_literature_comparison_protocol.md` | Rules for separating reproduced and reported-only literature comparisons |
| `ieee_dataset_license_audit.md` | Dataset license, citation, and repository-release boundary notes |
| `ieee_dataset_compliance_audit.md` | Generated check for dataset boundary, seed citations, and submission-metadata wording |
| `ieee_server_resume_runbook.md` | Safe server restart, launch, monitoring, and sync procedure for IEEE experiments |
| `IEEE_RESULT_INTEGRATION_PROTOCOL.md` | Rules for syncing complete server-side results |
| `ieee_scale_result_interpretation.md` | Scale-wise recall/precision interpretation |
| `ieee_scale_ap_interpretation.md` | Local scale-bin AP diagnostic interpretation |
| `ieee_phase1_artifact_audit.md` | Generated audit for IEEE planning and evidence artifacts |
| `ieee_number_trace_audit.md` | Generated trace audit for numerical claims in the English draft pack |
| `ieee_trans/README.md` | Navigation for the IEEE manuscript workspace |
| `ieee_trans/title_abstract_index_terms_workbench.md` | T-ITS title, abstract, and index terms planning |
| `ieee_trans/submission_metadata_workbench.md` | Author, funding, code/data, and submission metadata worksheet |
| `ieee_front_matter_audit.md` | Generated audit for T-ITS title, abstract, index terms, and metadata guards |
| `ieee_evidence_map_audit.md` | Generated check for the IEEE evidence-to-section map |
| `ieee_trans/cover_letter_workbench.md` | IEEE cover-letter planning skeleton |
| `ieee_trans/section_draft_pack.md` | Evidence-bounded English section drafts |
| `ieee_trans/manuscript_assembly_checklist.md` | Gates and order for assembling a future IEEE manuscript |
| `ieee_manuscript_assembly_audit.md` | Generated check for IEEE manuscript assembly inputs and final-source locks |
| `ieee_trans/page_budget_plan.md` | T-ITS Regular Paper page budget and table/figure selection plan |
| `ieee_trans/main_tex_preflight.md` | Preflight checklist before creating final-facing `main.tex` |
| `ieee_trans/tables/` | Generated IEEE LaTeX table drafts |

## Dual-Route Coordination

| File | Purpose |
| --- | --- |
| `DUAL_SUBMISSION_STRATEGY.md` | Boundary document for keeping the Chinese-journal route and IEEE English-journal route active without mixing manuscripts or inventing evidence |

## Current Evidence Artifacts

| Artifact | Purpose |
| --- | --- |
| `tables/main_comparison_for_paper.csv` | Main VisDrone validation results and completed baselines |
| `tables/model_complexity.csv` | Parameters, GFLOPs, and weight size |
| `tables/speed_results.csv` | Wall-clock speed and Ultralytics timing results |
| `tables/ieee_scale_results_visdrone.csv` | Scale-wise recall/precision for completed VisDrone models |
| `tables/ieee_scale_ap_results_visdrone.csv` | Local scale-bin AP diagnostics for completed VisDrone models |
| `tables/ieee_literature_context.csv` | Reported-literature context table without performance ranking |
| `figures/scale_analysis/ieee_scale_recall_visdrone.png` | Scale-wise recall figure |
| `figures/scale_analysis/ieee_scale_ap50_visdrone.png` | Local scale-bin AP50 figure |
| `commands.md` | Reproducibility commands |

## Dataset Preparation Audits

| Artifact | Purpose |
| --- | --- |
| `datasets/uavdt_setup.md` | UAVDT source, layout, class mapping, and conversion instructions |
| `datasets/uavdt_operational_checklist.md` | Step-by-step UAVDT placement, conversion, preview, training, and sync checklist |
| `datasets/uavdt_conversion_readiness_audit.md` | Generated local audit and synthetic conversion smoke test for the UAVDT conversion chain |

## Chinese-Journal / CEA Materials

The CEA route materials remain available for the Chinese-journal manuscript, template migration, manual formatting review, and submission preparation:

```text
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
paper/cea_template_migration/
paper/CEA_*.md
paper/submission_audit_dashboard.md
```

They should not be used as the IEEE submission source, but they are still valid for the Chinese-journal submission track.

## Evidence Rule

Paper-facing numbers should be traceable to one of:

- `paper/tables/`
- `runs/`
- `runs/logs/`
- an official VisDrone result returned by the evaluation server

The current IEEE planning materials are organized around validation-set metrics, speed/complexity measurements, scale-wise recall/precision, local scale-bin AP diagnostics, per-class analysis, and qualitative figures.

Additional baseline workflows such as YOLOv8n/YOLO11s are recorded in the project configs and command notes. Paper tables are updated from audited logs and exported result files.

## IEEE Audit and Table Refresh

```powershell
python tools/run_ieee_audits.py
```

This command refreshes IEEE planning audits, generated table drafts, scale-wise interpretations, and the IEEE submission dashboard. It does not launch training and does not connect to the server.

Generated IEEE table drafts are stored in:

```text
paper/ieee_trans/tables/
```

## Chinese LaTeX/PDF Preview

The generic LaTeX draft below belongs to the Chinese-journal preparation route:

```text
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
```

It can be rebuilt with the project-local Tectonic helper:

```powershell
.\tools\build_paper_pdf.ps1
```

For the IEEE route, do not create or compile `paper/ieee_trans/main.tex` until `paper/ieee_trans/main_tex_preflight.md` passes.

## Additional Paper Helpers

Paper-preview and audit helpers are available:

```powershell
.\tools\build_paper_pdf.ps1
python tools/run_paper_audits.py
python tools/build_advisor_review_package.py
```

# IEEE Transactions Manuscript Workspace

This directory is reserved for the future IEEE Transactions English manuscript.

The manuscript should not be drafted as a direct translation of the CEA Chinese manuscript. It should be created only after the core IEEE evidence gates are satisfied:

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
| `section_draft_pack.md` | Evidence-bounded English section drafts for future IEEE manuscript assembly | Ready |
| `manuscript_assembly_checklist.md` | Gates and order for assembling a future IEEEtran manuscript | Ready |
| `main_tex_preflight.md` | Preflight checklist before creating final-facing IEEEtran `main.tex` | Ready |
| `page_budget_plan.md` | T-ITS Regular Paper page budget and main-paper table/figure selection plan | Ready |
| `references_seed.bib` | Seed bibliography for IEEE planning | Ready |
| `citation_plan.md` | Citation role mapping and verification notes | Ready |
| `evidence_to_sections.csv` | Claim/content-to-evidence mapping for sections | Ready |
| `table_figure_plan.md` | IEEE table and figure plan with readiness gates | Ready |
| `figure_source_manifest.md` | Figure candidates, source paths, and evidence boundaries | Ready |
| `main.tex` | IEEEtran manuscript source | Pending |
| `references.bib` | IEEE-style bibliography | Pending |
| `figures/` | English manuscript figures | Pending |
| `tables/` | Generated LaTeX table drafts and source manifest | Ready |
| `cover_letter_workbench.md` | Evidence-bounded cover letter planning skeleton | Ready |
| `cover_letter_draft.md` | Final cover letter draft | Pending |

## Related External Audits

| File | Purpose |
| --- | --- |
| `../ieee_tits_scope_fit_checklist.md` | T-ITS scope and traffic-sensing framing checklist |
| `../ieee_tits_author_requirements_audit.md` | Official-source T-ITS submission, abstract, keyword, and page-format requirements |
| `../ieee_front_matter_audit.md` | Generated guard for T-ITS title, abstract, index terms, and metadata workbenches |
| `../ieee_number_trace_audit.md` | Numeric trace audit for values in `section_draft_pack.md` |
| `../ieee_dataset_license_audit.md` | Dataset license, citation, and repository-release boundary notes |
| `../ieee_dataset_compliance_audit.md` | Generated check for dataset boundary, seed citations, and submission-metadata wording |
| `../ieee_server_resume_runbook.md` | Safe server restart, launch, monitoring, and sync procedure for IEEE experiments |
| `../ieee_submission_dashboard.md` | Current IEEE readiness dashboard |

## Current Rule

Do not add a final-looking IEEE manuscript until experiments support the main claims. Placeholder drafts are allowed only if clearly marked as planning drafts.

## Local Audit Command

From the project root, refresh all local IEEE planning audits and generated table drafts with:

```powershell
python tools\run_ieee_audits.py
```

This command does not launch training and does not connect to the server.

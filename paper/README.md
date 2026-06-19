# Paper Workspace

This directory contains the paper-facing materials for the YOLO VisDrone project.

The repository-level overview is maintained in `../README.md`. Use this file for paper-specific navigation, evidence rules, and rebuild commands.

## Current Route

The active paper route is IEEE Transactions preparation. The earlier CEA Chinese-journal route is paused and retained as historical material.

Current IEEE dashboard:

```text
paper/ieee_submission_dashboard.md
```

Current IEEE manuscript workspace:

```text
paper/ieee_trans/
```

Do not treat the old CEA PDF or Word draft as the current submission manuscript. A final IEEE `main.tex` should be created only after the gates in `paper/ieee_trans/main_tex_preflight.md` pass.

## IEEE Route Files

| File | Purpose |
| --- | --- |
| `IEEE_TRANS_SUBMISSION_PLAN.md` | Master plan for the IEEE Transactions route |
| `ieee_submission_dashboard.md` | One-page readiness dashboard for the IEEE route |
| `ieee_target_journal_analysis.md` | Target-journal fit analysis, with T-ITS as the leading direction |
| `ieee_required_experiment_gap.md` | Experiment and evidence gaps for an IEEE-level paper |
| `ieee_method_design_notes.md` | Candidate method notes, including TOFC |
| `ieee_method_selection_protocol.md` | Decision protocol for selecting the final method after real results arrive |
| `ieee_claim_boundary.md` | Claim rules and locked/allowed wording |
| `ieee_reviewer_risk_register.md` | Reviewer-risk register and mitigation plan |
| `IEEE_RESULT_INTEGRATION_PROTOCOL.md` | Rules for syncing complete server-side results |
| `ieee_scale_result_interpretation.md` | Scale-wise recall/precision interpretation |
| `ieee_scale_ap_interpretation.md` | Local scale-bin AP diagnostic interpretation |
| `ieee_phase1_artifact_audit.md` | Generated audit for IEEE planning and evidence artifacts |
| `ieee_trans/README.md` | Navigation for the IEEE manuscript workspace |
| `ieee_trans/section_draft_pack.md` | Evidence-bounded English section drafts |
| `ieee_trans/manuscript_assembly_checklist.md` | Gates and order for assembling a future IEEE manuscript |
| `ieee_trans/main_tex_preflight.md` | Preflight checklist before creating final-facing `main.tex` |
| `ieee_trans/tables/` | Generated IEEE LaTeX table drafts |

## Current Evidence Artifacts

| Artifact | Purpose |
| --- | --- |
| `tables/main_comparison_for_paper.csv` | Main VisDrone validation results and completed baselines |
| `tables/model_complexity.csv` | Parameters, GFLOPs, and weight size |
| `tables/speed_results.csv` | Wall-clock speed and Ultralytics timing results |
| `tables/ieee_scale_results_visdrone.csv` | Scale-wise recall/precision for completed VisDrone models |
| `tables/ieee_scale_ap_results_visdrone.csv` | Local scale-bin AP diagnostics for completed VisDrone models |
| `figures/scale_analysis/ieee_scale_recall_visdrone.png` | Scale-wise recall figure |
| `figures/scale_analysis/ieee_scale_ap50_visdrone.png` | Local scale-bin AP50 figure |
| `commands.md` | Reproducibility commands |

## Legacy CEA Materials

The CEA route materials remain available for reference, formatting history, and earlier Chinese writing drafts:

```text
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
paper/cea_template_migration/
paper/CEA_*.md
paper/submission_audit_dashboard.md
```

They should not be used as the current IEEE submission source.

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

## Legacy LaTeX Preview

The generic LaTeX draft below belongs to the earlier non-IEEE/CEA preparation route:

```text
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
```

It can still be rebuilt for historical reference:

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

For the IEEE route, do not create or compile `paper/ieee_trans/main.tex` until `paper/ieee_trans/main_tex_preflight.md` passes.

## Optional Legacy Helpers

Legacy paper-preview helpers are still available:

```powershell
.\tools\build_paper_pdf.ps1
python tools/run_paper_audits.py
python tools/build_advisor_review_package.py
```

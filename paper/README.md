# Paper Workspace

This directory contains the paper-facing materials for the YOLO VisDrone project.

The repository-level overview is maintained in `../README.md`. Use this file for paper-specific navigation, evidence rules, and rebuild commands.

## Where to Read the Current Paper

Main LaTeX submission candidate:

```text
paper/manuscript_submission_candidate.tex
```

Compiled PDF:

```text
paper/manuscript_submission_candidate.pdf
```

Recommended ways to read it:

1. Open `paper/manuscript_submission_candidate.pdf` for the current paper preview.
2. Edit `paper/manuscript_submission_candidate.tex` for the LaTeX source.
3. Keep the Markdown drafts as earlier writing material and use the LaTeX file as the current submission-oriented baseline.

## Important Files

| File | Purpose |
| --- | --- |
| `CEA_FINAL_SUBMISSION_EXECUTION_PLAN.md` | Highest-priority execution plan for pushing the project to formal 《计算机工程与应用》 submission readiness |
| `CEA_RESULT_INTERPRETATION_MATRIX.md` | Decision matrix for rewriting claims after fair-comparison results are complete |
| `CEA_SECTION_EVIDENCE_MAP.md` | Section-level claim and evidence map for journal manuscript rewriting |
| `CEA_SUBMISSION_RISK_REGISTER.md` | Submission risk register for CEA-facing reviewer questions and mitigation actions |
| `CEA_SUBMISSION_READINESS_100_PLAN.md` | Acceptance-oriented execution plan for reaching formal CEA submission readiness |
| `CEA_FULL_SUBMISSION_EXECUTION_PLAN.md` | Execution plan for reaching 《计算机工程与应用》 journal-submission readiness |
| `CEA_RESULT_INTEGRATION_PROTOCOL.md` | Rules for syncing completed server experiments into paper evidence |
| `CEA_MANUSCRIPT_UPDATE_QUEUE.md` | Ordered manuscript update queue after fair-comparison results finish |
| `post_sync_update_checklist.md` | Generated checklist for manuscript/table updates after completed server-result sync |
| `CEA_MANUSCRIPT_REWRITE_BLUEPRINT.md` | Section-by-section blueprint for expanding the LaTeX candidate into a journal manuscript |
| `cea_server_status_snapshot.md` | Generated read-only snapshot of server fair-comparison progress |
| `cea_server_progress_report.md` | Generated progress summary from the server status history table |
| `CEA_JOURNAL_MASTER_PLAN.md` | Master plan for the 《计算机工程与应用》 journal submission track |
| `CEA_REVIEW_GAP_ANALYSIS.md` | Gap analysis against Chinese YOLO journal-paper writing patterns |
| `CEA_JOURNAL_STYLE_BENCHMARK.md` | Journal-style benchmark checklist for CEA YOLO small-object papers |
| `CEA_JOURNAL_MANUSCRIPT_OUTLINE.md` | Section-by-section outline for expanding the paper into a journal manuscript |
| `advisor_progress_brief.md` | Short Chinese progress brief for advisor communication |
| `advisor_progress_brief_audit.md` | Generated audit for advisor brief freshness and evidence-boundary statements |
| `failure_case_taxonomy.md` | Failure-mode taxonomy for qualitative manuscript discussion |
| `reference_verification_matrix.md` | Candidate reference matrix with verification status and manuscript use |
| `reference_verification_audit.md` | Generated audit linking the reference verification matrix to the LaTeX bibliography |
| `PROJECT_ROADMAP.md` | Main project-to-paper roadmap and current status |
| `CEA_SUBMISSION_PLAN.md` | Earlier journal-strengthening plan and experiment matrix |
| `manuscript_polished.md` | Earlier polished Markdown manuscript draft |
| `manuscript_polished.html` | Browser preview of the polished manuscript |
| `manuscript_submission_candidate.md` | Shorter submission-oriented candidate draft |
| `manuscript_submission_candidate.tex` | Generic LaTeX version of the submission candidate |
| `manuscript_submission_candidate.pdf` | Compiled PDF generated from the LaTeX candidate |
| `draft_journal_intro_related_work.md` | Expanded journal-style introduction and related-work draft |
| `latex_notes.md` | LaTeX compilation and template migration notes |
| `manuscript_tables.md` | Paper-ready Markdown and LaTeX table drafts |
| `selected_figures.md` | Recommended figures for the manuscript body |
| `figure_index.md` | Full figure provenance index |
| `evidence_audit.md` | Paper-facing number and evidence audit |
| `manuscript_number_trace_audit.md` | Generated trace audit for decimal values in the LaTeX manuscript |
| `manuscript_length_audit.md` | Generated audit for journal-oriented manuscript length and structural density |
| `submission_checklist.md` | Pre-submission checklist and template migration notes |
| `submission_readiness_audit.md` | Generated local readiness audit for paper-facing artifacts and pending fair experiments |
| `paper_consistency_audit.md` | Generated consistency audit for manuscript-facing text and paper tables |
| `claim_boundary_audit.md` | Generated audit for unsupported overclaims and partial-result leakage in paper-facing text |
| `manuscript_journal_gap_audit.md` | Generated structural gap audit between the LaTeX candidate and journal manuscript blueprint |
| `tex_reference_audit.md` | Generated LaTeX citation and bibliography consistency audit |
| `tex_figure_audit.md` | Generated LaTeX figure path and float-layout audit |
| `tex_table_source_audit.md` | Generated LaTeX table label and source-provenance audit |
| `section_evidence_map_audit.md` | Generated audit for section-level claim-to-evidence mapping |
| `submission_risk_register_audit.md` | Generated audit for submission risk IDs, evidence paths, and mitigation coverage |
| `repro_commands_audit.md` | Generated audit for reproducibility command coverage |
| `config_inventory_audit.md` | Generated audit for dataset/model/train/server configuration files |
| `text_hygiene_audit.md` | Generated audit for hidden characters and common mojibake fragments in reader-facing text |
| `pdf_text_readability_audit.md` | Generated audit for compiled PDF text extraction and basic readability tokens |
| `submission_material_manifest.md` | Generated index of current submission-facing documents, tables, figures, and audits |
| `submission_audit_dashboard.md` | Generated one-page dashboard summarizing paper-facing audits |
| `references.md` | Reference list draft |
| `commands.md` | Reproducibility commands |
| `experiment_protocol.md` | Experimental protocol and evidence rules |
| `testdev_submission.md` | VisDrone local submission package notes |
| `tables/object_scale_distribution.csv` | Object scale distribution from YOLO-format VisDrone labels |
| `tables/scale_group_results.csv` | Thresholded scale-group validation matching results |
| `tables/accuracy_speed_tradeoff.csv` | Source table for the accuracy-speed-parameter trade-off figure |

## Evidence Rule

Paper-facing numbers should be traceable to one of:

- `paper/tables/`
- `runs/`
- `runs/logs/`
- an official VisDrone result returned by the evaluation server

The current manuscript is organized around validation-set metrics, speed/complexity measurements, scale-group analysis, per-class analysis, and qualitative figures.

Additional baseline workflows such as YOLOv8n/YOLO11s are recorded in the project configs and command notes. Paper tables are updated from audited logs and exported result files.

## Regenerate HTML Preview

```powershell
python tools/render_markdown_preview.py --input paper/manuscript_polished.md --output paper/manuscript_polished.html
```

The current polished manuscript embeds the recommended figures with relative paths under `paper/figures/`, so the HTML preview should show both tables and images.

To preview the shorter submission candidate:

```powershell
python tools/render_markdown_preview.py --input paper/manuscript_submission_candidate.md --output paper/manuscript_submission_candidate.html
```

## LaTeX Draft

Generic LaTeX source:

```text
paper/manuscript_submission_candidate.tex
```

Compiled PDF:

```text
paper/manuscript_submission_candidate.pdf
```

Recommended build command if TeX Live or MiKTeX is installed:

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

Project build helper:

```powershell
.\tools\build_paper_pdf.ps1
```

Run the full paper-facing audit sequence:

```powershell
python tools/run_paper_audits.py
```

Local lightweight build command if `.tools/tectonic/tectonic.exe` exists:

```powershell
cd paper
..\.tools\tectonic\tectonic.exe manuscript_submission_candidate.tex
```

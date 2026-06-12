# Paper Workspace

This directory contains the paper-facing materials for the YOLO VisDrone project.

The repository-level overview is maintained in `../README.md`. Use this file for paper-specific navigation, evidence rules, and rebuild commands.

## Where to Read the Current Paper

Main polished manuscript:

```text
paper/manuscript_polished.md
```

HTML preview:

```text
paper/manuscript_polished.html
```

Recommended ways to read it:

1. In VS Code/Cursor, open `paper/manuscript_polished.md` and use Markdown Preview.
2. Open `paper/manuscript_polished.html` in a browser for a more paper-like view.
3. Keep `paper/manuscript_draft.md` as the earlier full draft and `paper/manuscript_polished.md` as the current writing baseline.

## Important Files

| File | Purpose |
| --- | --- |
| `PROJECT_ROADMAP.md` | Main project-to-paper roadmap and current status |
| `manuscript_polished.md` | Current Chinese conference manuscript draft |
| `manuscript_polished.html` | Browser preview of the polished manuscript |
| `manuscript_submission_candidate.md` | Shorter submission-oriented candidate draft |
| `manuscript_submission_candidate.tex` | Generic LaTeX version of the submission candidate |
| `manuscript_submission_candidate.pdf` | Compiled PDF generated from the LaTeX candidate |
| `latex_notes.md` | LaTeX compilation and template migration notes |
| `manuscript_tables.md` | Paper-ready Markdown and LaTeX table drafts |
| `selected_figures.md` | Recommended figures for the manuscript body |
| `figure_index.md` | Full figure provenance index |
| `evidence_audit.md` | Paper-facing number and evidence audit |
| `submission_checklist.md` | Pre-submission checklist and template migration notes |
| `references.md` | Reference list draft |
| `commands.md` | Reproducibility commands |
| `experiment_protocol.md` | Experimental protocol and evidence rules |
| `testdev_submission.md` | VisDrone local submission package notes |

## Evidence Rule

Do not add a paper-facing number unless it can be traced to:

- `paper/tables/`
- `runs/`
- `runs/logs/`
- an official VisDrone result returned by the evaluation server

The current manuscript reports validation-set results only. Official VisDrone test-dev/test-challenge AP is not reported because the official server has not returned a result.

Additional external baselines such as YOLOv8n/YOLO11s are being prepared or run separately. Their numbers must not be added to the manuscript until the full logs, result files, and table exports are available and audited.

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

Local lightweight build command if `.tools/tectonic/tectonic.exe` exists:

```powershell
cd paper
..\.tools\tectonic\tectonic.exe manuscript_submission_candidate.tex
```

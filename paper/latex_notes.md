# LaTeX Migration Notes

The short submission candidate has been migrated to:

```text
paper/manuscript_submission_candidate.tex
```

## Recommended Compiler

Use XeLaTeX because the manuscript is Chinese and uses `ctexart` with the Windows fontset:

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

Run twice so references, figures, and table labels are resolved.

## Current Local Environment

No local `xelatex` or `pdflatex` command was detected in this environment, so TeX Live/MiKTeX compilation was not available through the standard commands.

Tectonic 0.16.9 was downloaded locally to:

```text
.tools/tectonic/tectonic.exe
```

The `.tools/` directory is ignored by Git and is not uploaded to GitHub. This path documents the local helper used on this workstation, not a repository dependency.

This lightweight LaTeX engine successfully compiled the manuscript to:

```text
paper/manuscript_submission_candidate.pdf
```

The first attempt with the default `ctexart` fontset stalled while downloading Fandol fonts, so the LaTeX source now uses:

```tex
\documentclass[UTF8,a4paper,10.5pt,fontset=windows]{ctexart}
```

This should use Windows Chinese fonts instead of downloading Fandol fonts.

Tectonic fallback command:

```powershell
cd paper
..\.tools\tectonic\tectonic.exe manuscript_submission_candidate.tex
```

Observed warnings:

- Tectonic reports a Fontconfig default config warning on Windows, but PDF generation succeeds.
- Table overfull warnings were reduced by wrapping tables with `\resizebox{\textwidth}{!}{...}`.
- Some underfull line warnings remain and can be addressed during final template polishing.
- One overfull vbox warning remains, likely caused by figure/table placement in the generic `ctexart` preview.
- Windows font paths are used because the source specifies `fontset=windows`.

If TeX Live or MiKTeX is installed later, the same `.tex` file can also be compiled with XeLaTeX:

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

## Figure Paths

The LaTeX file is placed directly under `paper/`, so figure paths use:

```text
figures/...
```

Do not move the `.tex` file into another directory unless the figure paths are updated.

## Next Template Step

When the target conference template is known:

1. Replace the `ctexart` document class with the conference class.
2. Move title, author, abstract, keywords, sections, tables, figures, and references into the template.
3. Keep all numeric values unchanged unless a new value is added to `paper/tables/` and `paper/evidence_audit.md`.

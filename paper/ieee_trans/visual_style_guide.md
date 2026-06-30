# IEEE Figure Visual Style Guide

Status: active style guide for redrawing paper-facing figures.

The goal is to raise the visual quality of the IEEE draft figures without
changing experimental evidence. A figure may be visually redesigned, but any
number, curve, image, or conclusion in it must still be traceable to source
tables, logs, scripts, or model outputs.

## Visual Direction

Use a clean graphical-summary style:

- pastel color blocks;
- thin dark outlines;
- rounded rectangular modules only for diagrams;
- dashed panel boundaries for grouped ideas;
- large readable labels;
- minimal clutter;
- consistent color meaning across all figures.

This follows the advisor-provided style reference while keeping the final
figures suitable for an IEEE paper.

## Palette

Use this palette as the shared default.

| Name | Hex | RGB | Use |
| --- | --- | --- | --- |
| Mist blue | `#e3eef1` | 227, 238, 241 | Background panels |
| Soft rose | `#f8d8da` | 248, 216, 218 | Detect head / warning / limitation |
| Peach | `#f1d0b0` | 241, 208, 176 | Data or input blocks |
| Pale green | `#daebcf` | 218, 235, 207 | Backbone / stable feature blocks |
| Aqua mint | `#d0ede4` | 208, 237, 228 | Feature fusion / CSGate path |
| Steel blue | `#8ab2d1` | 138, 178, 209 | P2 high-resolution / main method highlight |
| Soft orange | `#ebb88a` | 235, 184, 138 | Ablation / ScaleGate caution |
| Deep blue | `#4f71be` | 79, 113, 190 | Final CSGate highlight / selected curve |
| Charcoal | `#243040` | 36, 48, 64 | Text and outlines |
| Light gray | `#f6f7f9` | 246, 247, 249 | Figure background |

## Typography

| Element | Recommendation |
| --- | --- |
| Diagram title | 13-16 pt, bold |
| Module label | 9-11 pt |
| Axis label | 10-12 pt |
| Tick label | 8-10 pt |
| Caption text | handled by LaTeX, not embedded in image |
| Font family | DejaVu Sans or Arial for plotted figures; Times-compatible LaTeX captions |

Rules:

- Do not embed long captions inside figures.
- Keep all labels in English.
- Avoid overly small text that becomes unreadable in a two-column layout.
- Use panel tags `(a)`, `(b)`, `(c)` only when the figure truly has subpanels.

## Diagram Rules

For architecture and method figures:

- Use left-to-right flow.
- Show only the structural components needed for the paper claim.
- Do not draw every YOLO layer.
- Highlight CSGate as a bounded correction, not a universal enhancement.
- Use a separate dashed boundary for evidence gates or claim boundaries.

For quantitative plots:

- Use the same model colors across figures.
- Highlight CSGate with Deep blue.
- Use muted colors for baselines and ablations.
- Avoid rainbow colormaps unless the color scale is the data itself.
- Add direct labels only when they improve readability.

## Model Color Map

| Model | Color |
| --- | --- |
| YOLO11n | `#8ab2d1` |
| YOLO11n-P2 | `#d0ede4` |
| YOLO11n-P2-CA | `#daebcf` |
| YOLOv8n | `#f1d0b0` |
| YOLO11s | `#ebb88a` |
| YOLO11n-P2-TOFC | `#f8d8da` |
| YOLO11n-P2-ScaleGate | `#b7a8d9` |
| YOLO11n-P2-CSGate | `#4f71be` |

## Required Figure Quality Checks

Before a figure enters `main_draft.tex`:

1. Source data or script is recorded in `figure_source_manifest.md`.
2. The figure has English labels only.
3. Text remains readable at one-column or two-column size.
4. Colors are consistent with this guide.
5. No claim is stronger than the table evidence.
6. The PDF compiles after replacement.
7. `python tools/run_ieee_audits.py` passes.

## Figure Output Standards

| Figure Type | Preferred Format | DPI / Size |
| --- | --- | --- |
| Architecture schematic | PNG now, PDF/SVG later if stable | 300 dpi or higher |
| Quantitative plot | PNG for draft, PDF for final package if supported | 300 dpi or higher |
| Qualitative image panel | PNG or JPG copied from source images | avoid compression artifacts |
| Contact sheet / review artifact | Not allowed in final manuscript | n/a |

## Final Packaging Note

Before formal submission, convert key line plots and diagrams to vector PDF if
possible. Keep raster qualitative images as high-resolution PNG/JPG.

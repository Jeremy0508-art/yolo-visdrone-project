# IEEE Table and Figure Plan

Status: planning draft. Do not treat locked items as finished manuscript evidence.

## Tables

| ID | Planned Table | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| T1 | Dataset statistics for VisDrone and UAVDT | VisDrone existing metadata; UAVDT conversion statistics | Locked | UAVDT must be converted and audited first. |
| T2 | Implementation details | Existing configs, args, hardware notes | Partially ready | Needs final method and server environment details. |
| T3 | Main VisDrone comparison | `paper/tables/main_comparison_for_paper.csv` | Ready for existing models | Use exact values only. |
| T4 | UAVDT cross-dataset comparison | `paper/tables/ieee_uavdt_results_for_paper.csv`; `paper/tables/ieee_uavdt_results_status.csv` | Ready | Completed UAVDT rows support the static-P2 validity boundary and the bounded CSGate repair claim. |
| T5 | Ablation study | Existing P2/CA/960/SmallObjAug/TOFC/ScaleGate/CSGate rows | Ready with caveats | Use TOFC and ScaleGate as bounded/mixed ablations; use CSGate only as a partial-repair method candidate. |
| T6 | Scale-wise recall/precision metrics | `paper/tables/ieee_scale_results_visdrone.csv` | Ready for completed VisDrone models | Use recall/precision wording; do not call this AP-small. |
| T6b | Local scale-bin AP diagnostics | `paper/tables/ieee_scale_ap_results_visdrone.csv` | Ready for completed VisDrone models | Local diagnostic only; do not call this official COCO/VisDrone AP-small. |
| T7 | Speed and complexity | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` | Ready for existing models | Must be refreshed after any new final model. |
| T8 | Literature context comparison | `paper/tables/ieee_literature_context.csv`, `paper/ieee_literature_comparison_protocol.md` | Ready as context | Contains no performance ranking; keep reproduced and reported-only results separate. |

## Figures

| ID | Planned Figure | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| F1 | Method overview | English architecture figure for the bounded CSGate route | Ready for advisor draft | Show P2/P3 cross-scale conditioning and keep the caption clear that CSGate is a partial-repair method candidate. |
| F1b | ScaleAwareP2Gate module schematic | `src/models/attention/scale_aware_p2_gate.py`; `paper/ieee_trans/scalegate_method_section_draft.md` | Ready as negative/mixed ablation | Can show local context, channel gate, spatial gate, and bounded residual gain without promoting ScaleGate as the proposed method. |
| F1c | CSGate module schematic | `tools/plot_csgate_schematic.py`; `src/models/attention/cross_scale_p2_p3_gate.py`; `paper/figures/method/csgate_schematic.png` | Ready for advisor draft | Structural figure only; shows cross-scale P2/P3 consistency and bounded residual correction without encoding performance values. |
| F2 | P2/high-resolution branch schematic | Model YAML and existing diagrams | Ready as structural figure | Can be used without claiming accuracy gain beyond evidence. |
| F3 | Training curves | Existing completed run figures | Ready for existing models | Use clear English caption and source run path. |
| F4 | Accuracy-speed trade-off | Existing tables including TOFC, ScaleGate, and CSGate | Ready for advisor draft | Keep YOLO11s as the absolute-accuracy boundary and CSGate as the bounded lightweight repair candidate. |
| F5 | Scale-wise recall plot | `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` | Ready for completed VisDrone models | Generated from full validation, not smoke tests. |
| F5b | Local scale-bin AP50 plot | `paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png` | Ready for completed VisDrone models | Local diagnostic only; not official AP-small. |
| F6 | Qualitative comparison | Existing qualitative images | Partially ready | Captions and class labels should be English and readable. |
| F7 | Failure case taxonomy | Existing failure-case contact sheets | Partially ready | Should highlight dense occlusion, tiny distant objects, and class ambiguity. |

## Formatting Rules for Future IEEE Figures

- Keep captions factual and source-aware.
- Avoid saying "better" or "improved" in figure captions unless the corresponding quantitative table supports it.
- Use English labels only in IEEE figures.
- Record each figure source path and generation command in `paper/ieee_trans/figure_source_manifest.md` before final submission.
- Do not reuse CEA Word-layout screenshots as IEEE figures.

## Immediate Next Actions

1. Keep `paper/ieee_trans/figure_source_manifest.md` updated after selecting or regenerating IEEE figures.
2. Use `tools/export_ieee_tables.py` to regenerate current evidence-backed LaTeX table drafts after any source CSV changes.
3. Leave final-package-only tables out of `main.tex` until target-journal, metadata, and page-budget gates close.
4. Use `paper/ieee_trans/page_budget_plan.md` to decide which ready tables and figures stay in the 10-page T-ITS main paper.

# IEEE Table and Figure Plan

Status: planning draft. Do not treat locked items as finished manuscript evidence.

## Tables

| ID | Planned Table | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| T1 | Dataset statistics for VisDrone and UAVDT | VisDrone existing metadata; UAVDT conversion statistics | Locked | UAVDT must be converted and audited first. |
| T2 | Implementation details | Existing configs, args, hardware notes | Partially ready | Needs final method and server environment details. |
| T3 | Main VisDrone comparison | `paper/tables/main_comparison_for_paper.csv` | Ready for existing models | Use exact values only. |
| T4 | UAVDT cross-dataset comparison | Future UAVDT run outputs | Locked | Required for generalization claims. |
| T5 | Ablation study | Existing P2/CA/960/SmallObjAug rows plus future TOFC | Partially ready | Current evidence supports P2/input-size discussion; TOFC locked. |
| T6 | Scale-wise recall/precision metrics | `paper/tables/ieee_scale_results_visdrone.csv` | Ready for completed VisDrone models | Use recall/precision wording; do not call this AP-small. |
| T6b | Local scale-bin AP diagnostics | `paper/tables/ieee_scale_ap_results_visdrone.csv` | Ready for completed VisDrone models | Local diagnostic only; do not call this official COCO/VisDrone AP-small. |
| T7 | Speed and complexity | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` | Ready for existing models | Must be refreshed after any new final model. |
| T8 | Literature context comparison | `paper/tables/ieee_literature_context.csv`, `paper/ieee_literature_comparison_protocol.md` | Ready as context | Contains no performance ranking; keep reproduced and reported-only results separate. |

## Figures

| ID | Planned Figure | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| F1 | Method overview | Existing CEA overview redrawn in English, or new TOFC overview | Pending final method | Do not finalize before choosing final architecture. |
| F2 | P2/high-resolution branch schematic | Model YAML and existing diagrams | Ready as structural figure | Can be used without claiming accuracy gain beyond evidence. |
| F3 | Training curves | Existing completed run figures | Ready for existing models | Use clear English caption and source run path. |
| F4 | Accuracy-speed trade-off | Existing tables plus future final method | Partially ready | Refresh after TOFC/UAVDT if used. |
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
3. Leave locked tables out of `main.tex` until their evidence exists.
4. Use `paper/ieee_trans/page_budget_plan.md` to decide which ready tables and figures stay in the 10-page T-ITS main paper.

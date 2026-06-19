# T-ITS Regular Paper Page Budget Plan

Status: planning draft. This is not a final page count.

Target route: IEEE Transactions on Intelligent Transportation Systems (T-ITS), Regular Paper.

Official planning constraint: T-ITS suggests 10 IEEE-style pages for Regular Papers. Extra pages are possible within the journal's stated limits and charges, but the working target should stay close to 10 pages before overlength.

## Budget Principle

The final manuscript should not try to include every available table and visualization. The main paper must show:

1. transportation motivation and scope fit,
2. final method or fallback route,
3. reproduced VisDrone evidence,
4. cross-dataset evidence if available,
5. scale-wise small-object diagnostics,
6. speed/complexity trade-off,
7. limitations.

Everything else should move to supplementary material, repository documentation, or be omitted.

## Tentative Section Budget

| Section | Target Pages | Notes |
| --- | ---: | --- |
| Title, abstract, index terms | 0.5 | Abstract must be 150-250 words after final evidence is known. |
| Introduction | 1.0 | Must make UAV-assisted traffic perception visible in the first page. |
| Related Work | 1.0 | Use dense synthesis, not a paper-by-paper list. |
| Method | 1.5 | Include final method overview and only validated components. |
| Experiments setup | 1.0 | Datasets, metrics, implementation, hardware, and reproducibility. |
| Results and ablation | 2.0 | Main VisDrone table, final ablation, cross-dataset table if available. |
| Scale-wise and efficiency analysis | 1.25 | Small-object diagnostics plus speed/complexity trade-off. |
| Qualitative analysis and limitations | 0.75 | One compact qualitative/failure figure at most. |
| Conclusion | 0.25 | Evidence-bounded and short. |
| References | 1.0-1.5 | Must be watched carefully after recent related work is finalized. |

Working total: about 10.0-10.75 pages. If UAVDT and TOFC are both included, reduce qualitative material and merge tables before expanding beyond 10 pages.

## Main-Paper Table Selection

| Priority | Table | Source | Main-Paper Decision | Condition |
| --- | --- | --- | --- | --- |
| Required | Dataset and implementation summary | `paper/ieee_trans/table_figure_plan.md`, setup notes | Include as compact one-column or two-column table | Add UAVDT rows only after conversion. |
| Required | Main reproduced results | `paper/ieee_trans/tables/visdrone_main_results.tex` | Include | Keep exact audited values. |
| Required | Ablation results | Existing main results plus final method rows | Include, possibly merged with main results | Do not include TOFC row until complete. |
| Required | Speed and complexity | `paper/ieee_trans/tables/speed_complexity.tex` | Include | Refresh after final model. |
| Required if available | Cross-dataset results | future UAVDT table | Include | Required for generalization claims. |
| Optional | Scale-wise recall/precision | `paper/ieee_trans/tables/scale_recall_precision.tex` | Include if space allows; otherwise summarize and use figure | Must say recall/precision. |
| Optional | Local scale-bin AP | `paper/ieee_trans/tables/scale_bin_ap.tex` | Prefer figure plus short text; table may move to supplement | Must not be called official AP-small. |
| Optional | Literature context | `paper/ieee_trans/tables/literature_context.tex` | Usually move to Related Work text or supplement | No performance ranking. |

## Main-Paper Figure Selection

| Priority | Figure | Source | Main-Paper Decision | Condition |
| --- | --- | --- | --- | --- |
| Required | Method overview | final English figure | Include | Regenerate after final method is selected. |
| Required | Accuracy-speed or efficiency trade-off | `paper/figures/tradeoff/accuracy_speed_tradeoff.png` | Include if refreshed | Must include final method if used. |
| Required | Scale-wise small-object plot | `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` or AP50 plot | Include one, not both, unless space allows | Caption must match metric definition. |
| Optional | Training curves | existing run figures | Usually omit from main paper | Use only if reviewers need convergence evidence. |
| Optional | PR/confusion matrix | existing run figures | Move to supplement or repository | Too dense for 10-page paper. |
| Optional | Qualitative comparison | curated qualitative images | Include one compact figure if readable | Use English labels and source weight. |
| Optional | Failure cases | curated failure sheet | Include only if it sharpens limitations | Avoid oversized contact sheets. |
| Locked | UAVDT qualitative/scale figures | future UAVDT outputs | Include only after UAVDT is complete | Do not use placeholders. |

## Merge and Compression Rules

- Merge main comparison and ablation when the same rows support both stories.
- Prefer one combined speed/complexity table instead of separate parameter and latency tables.
- Use one scale diagnostic figure plus one compact supporting table, not all scale artifacts.
- Keep literature context in prose unless the final Related Work needs a compact taxonomy table.
- Avoid full-page qualitative contact sheets in the main paper.
- Do not include both training curves and PR curves unless there is a specific reviewer-facing reason.

## Current Main-Paper Candidate Package

This package is safe for the current evidence route but must be revised after TOFC/UAVDT results:

| Slot | Candidate |
| --- | --- |
| Table 1 | Dataset and implementation summary, compact |
| Table 2 | Main VisDrone comparison plus ablation rows |
| Table 3 | Speed and complexity |
| Table 4 | Scale-wise recall/precision or local scale-bin AP summary |
| Figure 1 | Final method overview, pending final method |
| Figure 2 | Accuracy-speed trade-off, refreshed after final method |
| Figure 3 | Scale-wise small-object diagnostic |
| Figure 4 | Qualitative/failure examples, compact and English-labeled |

If UAVDT is completed, reserve one additional table for cross-dataset results and remove either the scale table or qualitative figure from the main paper.

## Checks Before Creating `main.tex`

Before creating a final-facing IEEE source:

1. Re-read `paper/ieee_tits_author_requirements_audit.md`.
2. Rebuild table drafts with `python tools/export_ieee_tables.py`.
3. Confirm `paper/ieee_number_trace_audit.md` has zero non-ready numeric claims.
4. Select no more than four main-paper tables before layout.
5. Select no more than four main-paper figures before layout.
6. Keep TOFC/UAVDT slots locked until real results exist.

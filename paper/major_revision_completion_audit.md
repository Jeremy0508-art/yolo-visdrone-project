# Major Revision Completion Audit

Date: 2026-06-21

## Objective

Convert the current YOLO VisDrone/UAVDT materials from a progress-report style package into a paper-style argument that can support both the Chinese-journal route and the IEEE English-extension route.

This audit covers only the design-layer and manuscript-structure revision. It does not claim final UAVDT results, final journal readiness, or final method selection.

## Completed

| Item | Status | Evidence |
| --- | --- | --- |
| Shared major-revision roadmap | Done | `paper/MAJOR_REVISION_ROADMAP.md` |
| Shared core argument | Done | `paper/reframed_core_argument.md` |
| Dual-route manuscript strategy | Done | `paper/dual_track_reframed_manuscript_strategy.md` |
| Evidence-to-claim matrix | Done | `paper/tables/reframed_evidence_matrix.csv` |
| Project roadmap updated | Done | `paper/PROJECT_ROADMAP.md` |
| Paper workspace README updated | Done | `paper/README.md` |
| IEEE workspace README updated | Done | `paper/ieee_trans/README.md` |
| IEEE preflight updated | Done | `paper/ieee_trans/main_tex_preflight.md` |
| IEEE evidence map updated | Done | `paper/ieee_trans/evidence_to_sections.csv` |
| Post-UAVDT rewrite gate updated | Done | `paper/ieee_trans/post_uavdt_rewrite_checklist.md` |
| IEEE reproducibility notes updated | Done | `paper/ieee_trans/reproducibility_notes.md` |
| IEEE submission dashboard updated | Done | `paper/ieee_submission_dashboard.md` |
| IEEE draft rewritten around the new paper line | Done | `paper/ieee_trans/main_draft.tex` |
| IEEE draft PDF rebuilt | Done | `paper/ieee_trans/main_draft.pdf` |

## Current Paper Line

```text
High-resolution input and shallow P2 prediction can improve lightweight YOLO small-object diagnostics, but the benefit must be discussed together with computational cost, object scale, model capacity, and cross-dataset validity boundaries.
```

This line replaces the earlier model-list narrative. P2, input resolution, CoordAttention, TOFC, SmallObjAug, YOLO11s, and UAVDT now have separate evidence roles rather than being treated as one combined improvement story.

## Verification

| Check | Result |
| --- | --- |
| IEEE tables regenerated | Passed with `python tools/export_ieee_tables.py` |
| IEEE PDF compiled | Passed with `tools/build_paper_pdf.ps1`; output `paper/ieee_trans/main_draft.pdf` |
| PDF page count | 5 pages |
| LaTeX fatal errors | None found |
| Undefined citations/references | None found |
| Overfull table warnings | None found |
| Visible placeholder markers in IEEE draft and generated tables | None found |
| IEEE table audit | 18 ready, 1 pending optional UAVDT table |
| Visual PDF spot check | Pages 1-5 checked; no obvious table/figure overlap |

The remaining LaTeX warnings are font-substitution warnings from the local Tectonic build path and do not affect the current PDF preview.

## UAVDT Boundary

UAVDT was locked out of paper claims during the design-layer rewrite. The full four-run UAVDT set has since been completed, synced, exported, and audited. The completed integration is recorded in `paper/ieee_uavdt_integration_audit.md`.

Current paper-facing UAVDT interpretation:

| Run | Status |
| --- | --- |
| `baseline_yolo11n_960_uavdt` | Complete and synced |
| `yolo11n_p2_960_uavdt` | Complete and synced; weaker than YOLO11n-960 on UAVDT |
| `baseline_yolov8n_960_uavdt` | Complete and synced; stronger than YOLO11n-P2-960 on UAVDT |
| `baseline_yolo11s_960_uavdt` | Complete and synced; strongest UAVDT reference in the current table |

These values support a dataset-validity-boundary conclusion rather than a transferable P2 superiority claim.

## Remaining After UAVDT

1. Confirm exact IEEE target journal with the advisor.
2. Confirm author order, affiliations, funding, conflict-of-interest, and code/data statements.
3. Decide whether to keep the English paper as a validity-boundary / mechanism-analysis paper or redesign a new method.
4. Create final-facing `paper/ieee_trans/main.tex` only after the gates in `paper/ieee_trans/main_tex_preflight.md` pass.

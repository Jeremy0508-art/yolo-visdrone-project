# IEEE UAVDT Integration Audit

Date: 2026-06-21

## Objective

Integrate the completed UAVDT experiments into the IEEE draft without using partial server metrics or unsupported cross-dataset claims.

## Synced Runs

| Model | Local run directory | Evidence status |
| --- | --- | --- |
| YOLO11n-960 | `runs/detect/baseline_yolo11n_960_uavdt` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` present |
| YOLO11n-P2-960 | `runs/detect/yolo11n_p2_960_uavdt` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` present |
| YOLOv8n-960 | `runs/detect/baseline_yolov8n_960_uavdt` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` present |
| YOLO11s-960 | `runs/detect/baseline_yolo11s_960_uavdt` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` present |

## Paper-Facing Values

Source: `paper/tables/ieee_uavdt_results_for_paper.csv`

| Model | P | R | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n-960 | 0.85840 | 0.84102 | 0.88444 | 0.59081 |
| YOLO11n-P2-960 | 0.80931 | 0.81385 | 0.83711 | 0.53905 |
| YOLOv8n-960 | 0.88214 | 0.84659 | 0.88983 | 0.59487 |
| YOLO11s-960 | 0.87458 | 0.87049 | 0.89756 | 0.60819 |

## Interpretation

The UAVDT results do not support a transferable P2 improvement claim under the current setting. YOLO11n-P2-960 is lower than:

- YOLO11n-960 by 0.04733 mAP50 and 0.05176 mAP50-95;
- YOLOv8n-960 by 0.05272 mAP50 and 0.05582 mAP50-95;
- YOLO11s-960 by 0.06045 mAP50 and 0.06914 mAP50-95.

Therefore, the IEEE draft should be framed as a scale-wise mechanism and validity-boundary analysis, not as a universally superior P2 method.

## Files Updated

| File | Update |
| --- | --- |
| `paper/tables/ieee_uavdt_results_status.csv` | 4/4 UAVDT rows marked complete |
| `paper/tables/ieee_uavdt_results_for_paper.csv` | Manuscript-safe UAVDT table exported |
| `paper/ieee_trans/tables/uavdt_results.tex` | Generated LaTeX UAVDT table |
| `paper/ieee_trans/main_draft.tex` | Abstract, experiment section, UAVDT section, discussion, and conclusion updated |
| `paper/tables/reframed_evidence_matrix.csv` | UAVDT rows changed from pending evidence to validity-boundary evidence |
| `paper/ieee_trans/evidence_to_sections.csv` | UAVDT and conclusion statuses updated |
| `paper/ieee_trans/main_tex_preflight.md` | Cross-dataset gate updated to ready as validity-boundary evidence |
| `paper/ieee_trans/post_uavdt_rewrite_checklist.md` | Marked as integrated for current draft |
| `tools/export_ieee_uavdt_results.py` | UAVDT table generation adjusted to avoid LaTeX table overflow |

## Verification

| Check | Result |
| --- | --- |
| `python tools/export_ieee_uavdt_results.py` | Passed; 4/4 complete UAVDT runs |
| `python tools/check_ieee_tables.py` | Passed; 19 ready, 0 pending, 0 missing |
| PDF compile | Passed; `paper/ieee_trans/main_draft.pdf` generated |
| PDF page count | 6 pages |
| LaTeX fatal errors | None found |
| Undefined citations/references | None found |
| Overfull table warnings | None found after UAVDT table layout fix |
| Visual inspection | Pages containing UAVDT table and discussion checked; no obvious overlap |

The remaining LaTeX warnings are font-substitution warnings from the local Tectonic build path and do not affect the current PDF preview.

## Remaining Before Final Submission Source

1. Confirm exact IEEE target journal with the advisor.
2. Confirm author order, affiliations, funding, conflict-of-interest, and code/data release statements.
3. Decide whether the English paper should remain a validity-boundary / mechanism-analysis paper or be further redesigned with a new method.
4. Create final-facing `paper/ieee_trans/main.tex` only after `paper/ieee_trans/main_tex_preflight.md` gates pass.

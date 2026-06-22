# Post-UAVDT Rewrite Checklist

Status: complete UAVDT runs synced and integrated into the current IEEE draft.

This checklist defines the exact manuscript work that should happen after the four planned UAVDT experiments finish. It is intentionally separated from `main_draft.tex` so that partial server metrics do not leak into the paper. The current major-revision framing treats UAVDT as a validity-boundary test, not merely as an extra result table.

## Completion Gate

The main IEEE claims can use UAVDT only through the audited table below:

| Required run | Local run directory | Required status |
| --- | --- | --- |
| YOLO11n-960 on UAVDT | `runs/detect/baseline_yolo11n_960_uavdt` | 100 epochs and synced |
| YOLO11n-P2-960 on UAVDT | `runs/detect/yolo11n_p2_960_uavdt` | 100 epochs and synced |
| YOLOv8n-960 on UAVDT | `runs/detect/baseline_yolov8n_960_uavdt` | 100 epochs and synced |
| YOLO11s-960 on UAVDT | `runs/detect/baseline_yolo11s_960_uavdt` | 100 epochs and synced |

## Commands After Completion

The completed integration used the following commands from the project root:

```powershell
.\tools\sync_ieee_server_results.ps1 -MinEpochs 100
python tools\export_ieee_uavdt_results.py
python tools\build_ieee_experiment_registry.py
python tools\run_ieee_audits.py
powershell -ExecutionPolicy Bypass -File .\tools\build_paper_pdf.ps1 -TexFile paper\ieee_trans\main_draft.tex -OutDir paper\ieee_trans
```

## Manuscript Rewrite Decisions

After the audited UAVDT table exists, update the paper in this order:

1. Decide whether the paper is a method paper, a scale-wise mechanism-analysis paper, or a validity-boundary paper. Current draft: validity-boundary / mechanism-analysis paper.
2. Decide whether the main method is `YOLO11n-P2-960`, a TOFC variant, or a conservative analysis route. Current draft: conservative analysis route; P2 is not claimed as a transferable method.
3. Add `\input{tables/uavdt_results}` only if the table contains complete manuscript-safe rows. Current draft: added.
4. Rewrite the abstract with exact VisDrone and UAVDT values only after both tables are final. Current draft: updated.
5. Update the conclusion after the abstract, not before it. Current draft: updated.
6. Re-check all statements containing `generalize`, `robust`, `outperform`, `best`, `state-of-the-art`, or `cross-dataset`. Current draft: checked for claim discipline; remaining uses are cautious or negative claims.
7. Keep the YOLO11s boundary if YOLO11s remains stronger in absolute accuracy. Current draft: retained.
8. If UAVDT does not support the VisDrone trend, report the inconsistency as a validity boundary rather than hiding it. Current draft: reported as validity boundary.

## Claim Outcomes

| UAVDT outcome | Safe manuscript framing |
| --- | --- |
| P2 improves over YOLO11n-960 and is competitive with YOLOv8n-960 | Strengthen the high-resolution lightweight prediction claim. |
| P2 improves small diagnostics but not aggregate mAP | Frame the paper as scale-wise analysis and accuracy-efficiency trade-off. |
| P2 is weaker than YOLO11n-960 on UAVDT | Report dataset-dependent behavior and downgrade the method claim. |
| YOLO11s remains clearly stronger | Keep the larger-capacity reference as an accuracy upper reference, not a direct lightweight competitor. |

## Final Pre-Submission Locks

Before creating `main.tex`, verify:

- no partial UAVDT metrics remain in text or tables,
- every numeric claim appears in a source CSV,
- generated LaTeX tables match the CSV values,
- the abstract and conclusion do not overclaim beyond completed evidence,
- target journal, author list, affiliations, funding, code/data statements, and conflict-of-interest fields are manually confirmed.

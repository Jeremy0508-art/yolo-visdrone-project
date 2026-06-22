# IEEE CSGate Post-Result Protocol

Status: result-locked protocol for the second-cycle CSGate route. This file
does not contain experimental results and must not be cited as evidence.

## Purpose

CSGate is the current second-cycle adaptive high-resolution candidate after
the completed ScaleGate evidence failed the predeclared main-method decision
routes. This protocol defines the only safe path for moving CSGate from a
running server experiment into paper-facing tables and manuscript claims.

## Completion Gate

Do not sync, export, or cite CSGate metrics until both runs satisfy all local
and remote completion requirements:

| Run | Required directory | Completion rule |
| --- | --- | --- |
| VisDrone CSGate | `runs/detect/yolo11n_p2_csgate_960_visdrone` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` |
| UAVDT CSGate | `runs/detect/yolo11n_p2_csgate_960_uavdt` | 100 epochs, `results.csv`, `args.yaml`, `weights/best.pt` |

Partial epoch values are progress signals only. They must not enter the
manuscript, tables, abstract, conclusion, or README.

## Monitoring Command

Use this command while the server is still running:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\intake_ieee_csgate_results.ps1 -CheckOnly
```

Expected incomplete state:

```text
CSGate intake status: WAITING_FOR_REMOTE_COMPLETION
```

This mode refreshes status reports and audits, but it does not sync runs, run
diagnostics, or compile the manuscript.

## Complete-Result Intake

After both CSGate runs are `READY` at 100 epochs:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\intake_ieee_csgate_results.ps1 -RequireReady
```

This command is allowed to sync only complete runs through
`tools/sync_ieee_server_results.ps1`.

## Diagnostics After Sync

Only after complete local CSGate artifacts exist:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\intake_ieee_csgate_results.ps1 -RequireReady -RunDiagnostics
```

This refreshes:

- VisDrone scale recall/precision,
- local scale-bin AP,
- speed and complexity tables,
- VisDrone and UAVDT paper tables,
- IEEE LaTeX table drafts,
- local audit reports.

The helper `tools/set_ieee_scale_target.py` enables the CSGate scale target
only after the completed VisDrone run exists locally.

## Method Decision

After diagnostics are refreshed, decide the paper route from real evidence:

| Outcome | Manuscript route |
| --- | --- |
| CSGate improves VisDrone and repairs or reduces the UAVDT boundary without unacceptable speed/complexity cost | Consider CSGate as the proposed method, then rewrite title, abstract, method, results, and conclusion. |
| CSGate improves only VisDrone but not UAVDT | Treat it as dataset-dependent adaptive evidence; keep the paper framed around benefits, costs, and boundaries. |
| CSGate does not improve the target trade-off | Keep ScaleGate and CSGate as negative design evidence and select a lower-risk boundary-analysis route or design a third-cycle method. |

Do not choose the route by preference. Choose it from audited numbers.

## Required Follow-Up Checks

Run after any complete-result integration:

```powershell
python tools\run_ieee_audits.py
python tools\check_ieee_main_draft_numbers.py
python tools\check_ieee_draft_shareability.py
python tools\check_ieee_goal_readiness.py
```

Compile the advisor-review draft only after text and tables are updated:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\build_paper_pdf.ps1 -TexFile paper\ieee_trans\main_draft.tex -OutDir paper\ieee_trans
```

## Claim Locks

Until this protocol is completed, do not write:

- CSGate improves VisDrone detection.
- CSGate improves small-object AP or recall.
- CSGate fixes UAVDT.
- CSGate is robust across datasets.
- CSGate is the final proposed method.


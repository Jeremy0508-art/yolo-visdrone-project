# UAVDT Result Integration for IEEE Draft

This document defines how UAVDT results enter the IEEE manuscript workspace. It prevents partial server logs from being used as final manuscript evidence.

## Current Gate

UAVDT is currently in the training stage. The data preparation is complete, but the result table is not ready until all required runs are synced and audited.

Required runs:

| Model | Run directory | Config |
| --- | --- | --- |
| YOLO11n-960 | `runs/detect/baseline_yolo11n_960_uavdt` | `configs/train/baseline_yolo11n_960_uavdt.yaml` |
| YOLO11n-P2-960 | `runs/detect/yolo11n_p2_960_uavdt` | `configs/train/yolo11n_p2_960_uavdt.yaml` |
| YOLOv8n-960 | `runs/detect/baseline_yolov8n_960_uavdt` | `configs/train/baseline_yolov8n_960_uavdt.yaml` |
| YOLO11s-960 | `runs/detect/baseline_yolo11s_960_uavdt` | `configs/train/baseline_yolo11s_960_uavdt.yaml` |

## Server Monitoring

Current default server parameters are embedded in:

```powershell
.\tools\check_ieee_server_status.ps1
.\tools\sync_ieee_server_results.ps1
```

Monitor progress:

```powershell
.\tools\check_ieee_server_status.ps1
```

Partial runs may appear in `paper/ieee_server_status_snapshot.md`, but partial metrics must not be copied into manuscript tables.

## Sync Gate

Sync only complete runs:

```powershell
.\tools\sync_ieee_server_results.ps1 -MinEpochs 100
```

The sync script skips runs with fewer than 100 epochs. This means local result tables remain incomplete until the remote run has finished.

## Export Commands

After sync:

```powershell
python tools\export_ieee_uavdt_results.py
python tools\build_ieee_experiment_registry.py
python tools\run_ieee_audits.py
```

Generated files:

| Output | Purpose |
| --- | --- |
| `paper/tables/ieee_uavdt_results_status.csv` | Status table for complete, partial, and missing UAVDT runs |
| `paper/tables/ieee_uavdt_results_for_paper.csv` | Manuscript-safe UAVDT rows only; complete runs only |
| `paper/ieee_trans/tables/uavdt_results.tex` | LaTeX table generated only from complete local runs |

## Manuscript Rule

Do not `\input{tables/uavdt_results}` in the main manuscript until the UAVDT row set is complete enough to support the intended cross-dataset comparison. If the P2 trend does not transfer to UAVDT, the paper should report the inconsistency as a limitation rather than hide it.

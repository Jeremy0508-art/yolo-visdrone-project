# IEEE Result Integration Protocol

This document defines how server-side IEEE-route experiments can enter the local evidence set. It is conservative by design: partial runs are progress information only and must not be used in manuscript claims or tables.

## Experiments Covered

| Experiment | Role | Expected Local Run Directory |
| --- | --- | --- |
| YOLO11n-P2-TOFC-960 on VisDrone | Candidate new-method validation | `runs/detect/yolo11n_p2_tofc_960_visdrone` |
| YOLO11n-960 on UAVDT | Cross-dataset lightweight baseline | `runs/detect/baseline_yolo11n_960_uavdt` |
| YOLO11n-P2-960 on UAVDT | Cross-dataset P2 validation | `runs/detect/yolo11n_p2_960_uavdt` |
| YOLOv8n-960 on UAVDT | External lightweight reference | `runs/detect/baseline_yolov8n_960_uavdt` |
| YOLO11s-960 on UAVDT | Larger-capacity reference | `runs/detect/baseline_yolo11s_960_uavdt` |
| Full VisDrone scale-wise evaluation | Small-object evidence gate | `paper/tables/ieee_scale_results_visdrone.csv` |

## Minimum Evidence Gate

An IEEE experiment can be integrated only when all required evidence exists:

1. `results.csv` exists and contains at least 100 completed epoch rows for training runs.
2. `args.yaml` exists in the run directory.
3. `weights/best.pt` exists.
4. A matching training or queue log is copied into `runs/logs/`.
5. Any reported speed or complexity value comes from a local table/script, not estimation.
6. Any scale-wise claim comes from a full evaluation table, not a smoke test.
7. `tools/check_ieee_phase1_artifacts.py` and `tools/check_ieee_claims.py` are rerun after sync.

If any condition fails, the item remains a progress item and must not be used as paper evidence.

## Status Check

Use the status script to inspect remote progress without copying partial data:

```powershell
.\tools\check_ieee_server_status.ps1
```

The script writes:

- `paper/ieee_server_status_snapshot.md`
- `paper/tables/ieee_server_status_history.csv`

Then build a summarized progress report:

```powershell
python tools\build_ieee_server_progress_report.py
```

## Guarded Sync

Use the guarded sync script only after a run is expected to be complete:

```powershell
.\tools\sync_ieee_server_results.ps1 -MinEpochs 100
```

The script checks each remote run before copying. Runs marked `PARTIAL` or `MISSING` are skipped. This behavior should not be bypassed for manuscript-facing evidence.

## Post-Sync Local Checks

After synchronization, run:

```powershell
python tools\check_ieee_claims.py
python tools\check_ieee_phase1_artifacts.py
python tools\build_ieee_server_progress_report.py
```

If new final-model weights arrive, regenerate speed and complexity tables before writing final IEEE results. Re-run scale-wise recall/precision evaluation for any new final-method candidate.

## Manuscript Update Order

Use this order after new results are complete:

1. Update evidence tables and audit reports.
2. Update main result interpretation.
3. Update ablation interpretation.
4. Update scale-wise and efficiency analysis.
5. Update abstract, contribution list, and conclusion last.

This prevents the most visible manuscript sections from making unsupported claims.

## Forbidden Practices

- Do not copy partial epoch metrics into IEEE manuscript tables.
- Do not infer AP, latency, FPS, GFLOPs, memory, or per-class values.
- Do not report TOFC as an improvement until full TOFC evidence exists.
- Do not claim cross-dataset generalization until UAVDT results are complete.
- Do not mix reproduced local results with literature-reported numbers in one fairness table.
- Do not report official VisDrone test-dev results unless the platform returns real metrics.

## Current Locked Gates

As of the latest Phase 1 audit:

- TOFC performance is locked.
- UAVDT cross-dataset generalization is locked.
- VisDrone scale-wise recall/precision evidence is ready for completed models.
- AP-specific small/medium/large claims are locked.
- IEEE final manuscript drafting should remain evidence-bounded and planning-oriented until these gates change.

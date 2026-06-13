# CEA Execution Log

This file records execution status for the `Computer Engineering and Applications`
submission-strengthening stage. It is an audit log, not a manuscript source.

## 2026-06-13

- Active server run: `YOLO11n-960`.
- Run directory: `runs/detect/baseline_yolo11n_960_visdrone`.
- Server log: `runs/logs/train_baseline_yolo11n_960_20260613_220108.log`.
- Server PID observed: `43554`.
- A sequential server queue has been started with `tools/run_cea_server_queue.sh`.
- Queue PID observed: `43842`.
- Queue log: `runs/logs/cea_server_queue_.log`.
- Queued experiments:
  - `YOLO11n-P2-960`
  - `YOLOv8n-960`
  - `YOLO11s-960`
  - `YOLOv5n-640`
- Scale-distribution evidence generated from real YOLO-format VisDrone labels:
  - `paper/tables/object_scale_distribution.csv`
  - `paper/tables/class_scale_distribution.csv`
  - `paper/figures/scale_analysis/object_scale_distribution.png`

## Evidence Rules

- Do not copy queued experiment values into the manuscript until `results.csv`,
  `args.yaml`, weights and logs have been copied back and audited.
- Do not use official VisDrone test-dev numbers unless they come from a returned
  official evaluation result.

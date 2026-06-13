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
- Scale-group prediction matching has been generated from existing validation
  weights:
  - `paper/tables/scale_group_results.csv`
  - `paper/figures/scale_analysis/scale_group_recall.png`
  - command: `python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv`
  - default protocol: `conf=0.25`, `IoU=0.5`
- Server-result synchronization script added:
  - `tools/sync_cea_server_results.ps1`
  - command: `.\tools\sync_cea_server_results.ps1 -MinEpochs 100`
  - verified behavior: skips partial runs such as `PARTIAL:3` and regenerates
    paper tables only from local completed artifacts.
- Later status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 6 completed epochs.
  - Last recorded row timestamp on the server: `2026-06-13 22:47:56`.
  - Training PID `43554` was still active and the queue PID `43842` was still
    waiting for subsequent experiments.
  - No 960 fair-comparison result has been copied into paper tables yet because
    the run is still partial.
- Follow-up status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 8 completed epochs.
  - Last recorded row timestamp on the server: `2026-06-13 23:02:19`.
  - Training PID `43554` was still active.
- Follow-up status check:
  - `baseline_yolo11n_960_visdrone/results.csv` recorded 10 completed epochs.
  - Last recorded result row: epoch 10, `mAP50=0.0294104`, `mAP50-95=0.00980345`.
  - Training PID `43554` was still active with elapsed time about 1 hour 22 minutes.
  - Queue PID `43842` was still waiting for subsequent experiments.
  - This is still a partial run and has not been synchronized into paper tables.
- Local paper-material update:
  - Added `paper/CEA_FULL_SUBMISSION_EXECUTION_PLAN.md` as the acceptance-oriented execution plan for the 《计算机工程与应用》 submission track.
  - Updated `paper/README.md` to index the new plan.
  - Replaced stale speed values in Markdown drafts and regenerated HTML previews so they match `paper/tables/speed_results.csv`.
  - Verified that old speed values `13.785`, `72.54`, `17.733`, and `56.39` no longer appear in Markdown, LaTeX, or HTML paper files.
  - Ran `python tools/audit_submission_readiness.py`; the audit report was regenerated successfully.
  - Pushed GitHub commit `e1e4b0f` with message `Add CEA full submission execution plan`.

## Evidence Rules

- Do not copy queued experiment values into the manuscript until `results.csv`,
  `args.yaml`, weights and logs have been copied back and audited.
- Do not use official VisDrone test-dev numbers unless they come from a returned
  official evaluation result.
- Do not describe `scale_group_results.csv` as official AP; it is a thresholded
  prediction-matching analysis by GT object scale.

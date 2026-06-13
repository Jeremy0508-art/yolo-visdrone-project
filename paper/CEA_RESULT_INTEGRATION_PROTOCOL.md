# CEA Result Integration Protocol

This document defines how completed server experiments are allowed to enter the paper-facing evidence set for the 《计算机工程与应用》 submission track. It is intentionally conservative: partial runs are useful for progress monitoring, but they are not paper evidence.

## 1. Experiments Covered

The current server queue contains the fair-comparison experiments required by the journal plan:

| Experiment | Role | Expected local run directory |
| --- | --- | --- |
| YOLO11n-960 | Fair high-resolution baseline for YOLO11n | `runs/detect/baseline_yolo11n_960_visdrone` |
| YOLO11n-P2-960 | Fair P2 comparison at 960 input | `runs/detect/yolo11n_p2_960_visdrone` |
| YOLOv8n-960 | Fair high-resolution YOLOv8n external baseline | `runs/detect/baseline_yolov8n_960_visdrone` |
| YOLO11s-960 | Higher-capacity YOLO11 reference at 960 input | `runs/detect/baseline_yolo11s_960_visdrone` |
| YOLOv5n-640 | Classic lightweight YOLO reference | `runs/detect/baseline_yolov5n_visdrone` |

## 2. Minimum Evidence Gate

An experiment can be integrated into paper tables only when all of the following are true:

1. `results.csv` exists and contains at least 100 completed epoch rows.
2. `args.yaml` exists in the run directory.
3. `weights/best.pt` exists.
4. A corresponding training log has been copied into `runs/logs/`.
5. `tools/export_paper_tables.py` can parse the run without marking it as missing.
6. `tools/audit_submission_readiness.py` regenerates a report with the experiment no longer marked as pending.

If any condition fails, the run remains a progress item and must not be used for manuscript conclusions.

## 3. Sync Command

Use the guarded sync script from the local workstation:

```powershell
.\tools\sync_cea_server_results.ps1 -MinEpochs 100
```

The script checks each remote run before copying. A run marked `PARTIAL:<epochs>` is skipped. This behavior is required and should not be bypassed for paper-facing tables.

To inspect progress without copying partial outputs, use:

```powershell
.\tools\check_cea_server_status.ps1
```

## 4. Post-Sync Regeneration

After at least one completed run is copied back, regenerate the evidence set:

```powershell
python tools/export_paper_tables.py
python tools/benchmark_speed.py --warmup 10 --samples 100 --output paper/tables/speed_results.csv
python tools/collect_per_class_metrics.py
python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv
python tools/plot_accuracy_speed_tradeoff.py
python tools/audit_submission_readiness.py
```

Speed tests should be rerun under one consistent local hardware setting when possible. If a model cannot be speed-tested locally because of missing weights or memory limits, leave its speed cell out of the paper-facing comparison rather than estimating it.

## 5. Manuscript Update Order

Update the manuscript only after the tables have been regenerated and audited:

1. Update the fair-resolution comparison table.
2. Update the external baseline comparison table.
3. Update the ablation interpretation only if a same-family comparison changes the conclusion.
4. Update the accuracy-speed-complexity discussion.
5. Update the abstract and conclusion last.

This order prevents the abstract from making claims that are not supported by final tables.

## 6. Allowed Conclusions

Use conclusions that match the evidence:

- If YOLO11n-960 is close to YOLO11n-P2-CA-960, state that high input resolution is the main source of improvement and P2/CA provide supplementary gains.
- If YOLO11n-P2-960 improves over YOLO11n-960, state that the P2 branch remains useful under fair input resolution.
- If YOLO11n-P2-CA-960 improves over YOLO11n-P2-960, state that CoordAttention contributes under fair resolution.
- If YOLO11s-960 exceeds the proposed method, discuss the result as a capacity upper reference and emphasize parameter efficiency only if supported by the metrics.
- If YOLOv8n-960 is competitive, present the comparison as a fair external baseline result and avoid claiming universal superiority.

## 7. Forbidden Practices

- Do not copy partial epoch metrics into `paper/tables/`.
- Do not infer missing AP, latency, FPS, GFLOPs, or per-class values.
- Do not mix literature-reported metrics with local reproduced metrics in one fairness table.
- Do not report official VisDrone test-dev AP unless it comes from a returned official evaluation result.
- Do not use the server queue log alone as proof of completed training.

## 8. Final Audit Before Submission

Before marking the manuscript as submission-ready, run:

```powershell
python tools/audit_submission_readiness.py
rg -n "<placeholder-marker>|<internal-note-marker>|13\.785|72\.54|17\.733|56\.39" paper README.md tools
git status --short
```

The final manuscript can proceed only when pending fair experiments are either completed and integrated, or explicitly excluded from the manuscript with a clear evidence-based reason.

# Reproducibility Commands

## Project Check

```powershell
python tools/verify_project.py
```

## Export Current Paper Tables

```powershell
python tools/export_paper_tables.py
```

Generated files:

```text
paper/tables/main_results.csv
paper/tables/experiment_registry.csv
paper/tables/model_complexity.csv
paper/tables/main_comparison_for_paper.csv
paper/tables/ablation_results.csv
```

## Speed Benchmark

```powershell
python tools/benchmark_speed.py --warmup 10 --samples 100 --output paper/tables/speed_results.csv
```

Generated file:

```text
paper/tables/speed_results.csv
```

## Per-Class Metrics

Most per-class rows are parsed from final training logs. The 960-input model uses an additional validation run to expose a complete per-class table:

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0 --project runs/val --name yolo11n_p2_coordatt_960_per_class_val
```

The corresponding log is:

```text
runs/logs/val_yolo11n_p2_coordatt_960_20260609_182415.stdout.log
```

Collect per-class metrics with:

```powershell
python tools/collect_per_class_metrics.py
```

Generated file:

```text
paper/tables/per_class_results.csv
```

## VisDrone Test-Dev Export

Export the current best local model to the official VisDrone detection-result text format:

```powershell
python tools/export_visdrone_testdev.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --source data/processed/visdrone_yolo/images/test --imgsz 960 --conf 0.001 --iou 0.7 --max-det 500 --device 0 --output-dir runs/testdev_submit/yolo11n_p2_coordatt_960 --zip-name visdrone_testdev_submit.zip
```

Generated files:

```text
runs/testdev_submit/yolo11n_p2_coordatt_960/visdrone_testdev_submit.zip
runs/testdev_submit/yolo11n_p2_coordatt_960/manifest.csv
runs/testdev_submit/yolo11n_p2_coordatt_960/txt/
```

The zip contains 1580 root-level `.txt` files, one per local test-dev image. Official test-dev AP values must come from the VisDrone evaluation server after upload.

## Completed Training Runs

### YOLO11n Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n.yaml
```

Main output:

```text
runs/detect/baseline_yolo11n_visdrone
```

### YOLO11n-P2

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_pretrained_init.pt
```

Main output:

```text
runs/detect/yolo11n_p2_pretrained_visdrone
```

### YOLO11n-P2-CoordAttention

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_pretrained_init.pt
```

Main output:

```text
runs/detect/yolo11n_p2_coordatt_visdrone
```

### YOLO11n-P2-CoordAttention-960

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_960.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_960_pretrained_init_full.pt
```

Main output:

```text
runs/detect/yolo11n_p2_coordatt_960_visdrone_full
```

### YOLO11n-P2-CoordAttention Small-Object Augmentation

Started on 2026-06-08 and completed as a 100-epoch ablation run.

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_init.pt
```

Main output:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone
```

Initial log files:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stderr.log
```

The run was resumed multiple times from `last.pt` during local workstation pauses. Generic resume command:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --resume runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resume logs:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_183539.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_183539.stderr.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_213035.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_213035.stderr.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260609_072221.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260609_072221.stderr.log
```

Paper-facing result:

```text
Best mAP50: 0.32780 at epoch 80
Best mAP50-95: 0.18699 at epoch 74
Metric source: runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/results.csv
Table source: paper/tables/main_results.csv
```

## External Baseline Runs

These runs are intended to strengthen the paper with broader comparisons. Report only results that have completed training, copied-back logs, audited result files, and exported paper tables.

## CEA Fair-Comparison Experiment Queue

These experiments are required before treating the manuscript as a serious `Computer Engineering and Applications` journal candidate. They should be launched on the rented GPU server and reported only after complete 100-epoch logs and result files are copied back.

Server-side sequential queue:

```bash
chmod +x tools/run_cea_server_queue.sh
WAIT_PID=<current_training_pid> nohup tools/run_cea_server_queue.sh > runs/logs/cea_server_queue_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

Copy completed server runs back to the local project and regenerate paper tables:

```powershell
.\tools\sync_cea_server_results.ps1 -MinEpochs 100
```

Before using synced results in the manuscript, follow:

```text
paper/CEA_RESULT_INTEGRATION_PROTOCOL.md
```

### YOLO11n 960 Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n_960.yaml
```

Expected output:

```text
runs/detect/baseline_yolo11n_960_visdrone
```

### YOLO11n-P2 960

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_960.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_960_pretrained_init.pt
```

Expected output:

```text
runs/detect/yolo11n_p2_960_visdrone
```

### YOLOv8n 960 Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolov8n_960.yaml
```

Expected output:

```text
runs/detect/baseline_yolov8n_960_visdrone
```

### YOLO11s 960 Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11s_960.yaml
```

Expected output:

```text
runs/detect/baseline_yolo11s_960_visdrone
```

### YOLOv5n Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolov5n.yaml
```

Expected output:

```text
runs/detect/baseline_yolov5n_visdrone
```

## Scale Analysis

Analyze object scale distribution from YOLO-format VisDrone labels:

```powershell
python tools/analyze_object_scales.py
```

Evaluate thresholded scale-group matching for completed validation models:

```powershell
python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv
```

Generated files:

```text
paper/tables/object_scale_distribution.csv
paper/tables/class_scale_distribution.csv
paper/tables/scale_group_results.csv
paper/figures/scale_analysis/object_scale_distribution.png
paper/figures/scale_analysis/scale_group_recall.png
```

## Accuracy-Speed Trade-off

Generate the accuracy-speed-parameter trade-off figure from audited result tables:

```powershell
python tools/plot_accuracy_speed_tradeoff.py
```

Generated files:

```text
paper/tables/accuracy_speed_tradeoff.csv
paper/figures/tradeoff/accuracy_speed_tradeoff.png
```

## Method Overview Figure

Generate the method overview schematic used by the journal manuscript plan:

```powershell
python tools/draw_method_overview.py
```

Generated file:

```text
paper/figures/method/hrpca_yolo11n_overview.png
```

## Submission Readiness Audit

Generate a local readiness audit for paper-facing artifacts and pending fair-comparison experiments:

```powershell
python tools/audit_submission_readiness.py
```

Generated file:

```text
paper/submission_readiness_audit.md
```

Object scale distribution from YOLO-format labels:

```powershell
python tools/analyze_object_scales.py --splits train val --output-dir paper/tables --plot-dir paper/figures/scale_analysis
```

Scale-group prediction matching on the VisDrone validation split:

```powershell
python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv
```

The scale-group matching table uses `conf=0.25` and `IoU=0.5` by default. It
reports thresholded precision/recall by GT scale group and should not be
described as official AP.

### YOLOv8n Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolov8n.yaml
```

Main output:

```text
runs/detect/baseline_yolov8n_visdrone
```

Archived evidence:

```text
runs/detect/baseline_yolov8n_visdrone/results.csv
runs/logs/train_baseline_yolov8n_20260612_194313.log
paper/tables/main_results.csv
paper/tables/model_complexity.csv
paper/tables/per_class_results.csv
paper/tables/speed_results.csv
```

Paper-facing result:

```text
Best mAP50: 0.32520 at epoch 78
Best mAP50-95: 0.18386 at epoch 84
Metric source: runs/detect/baseline_yolov8n_visdrone/results.csv
Log source: runs/logs/train_baseline_yolov8n_20260612_194313.log
```

### YOLO11s Baseline

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11s.yaml
```

Main output:

```text
runs/detect/baseline_yolo11s_visdrone
```

Archived evidence:

```text
runs/detect/baseline_yolo11s_visdrone/results.csv
runs/logs/train_baseline_yolo11s_20260613_100711.log
paper/tables/main_results.csv
paper/tables/model_complexity.csv
paper/tables/per_class_results.csv
paper/tables/speed_results.csv
```

Paper-facing result:

```text
Best mAP50: 0.38937 at epoch 79
Best mAP50-95: 0.22719 at epoch 79
Metric source: runs/detect/baseline_yolo11s_visdrone/results.csv
Log source: runs/logs/train_baseline_yolo11s_20260613_100711.log
```

## Validation Examples

```powershell
python tools/val.py --weights runs/detect/baseline_yolo11n_visdrone/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 640 --batch 16 --device 0 --project runs/val --name baseline_val
```

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0 --project runs/val --name yolo11n_p2_coordatt_960_val
```

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

## Running Training Job

### YOLO11n-P2-CoordAttention Small-Object Augmentation

Started on 2026-06-08.

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_init.pt
```

Main output:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone
```

Log files for the current run:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_full_20260608_171712.stderr.log
```

Process observed after launch:

```text
PID 12744
```

Paused on 2026-06-08 before computer sleep. The process was stopped at epoch 6/100 while the latest saved checkpoint was:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resume command:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --resume runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resumed on 2026-06-08. The resume log reports:

```text
Resuming training ... from epoch 6 to 100 total epochs
```

Current resume log files:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_183539.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_183539.stderr.log
```

Resume process observed after launch:

```text
PID 32236
```

Paused again on 2026-06-08. At pause time, `results.csv` contained completed epoch 16, and the process was stopped during epoch 17. Latest checkpoint:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resume again with:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --resume runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resumed again on 2026-06-08. The resume log reports:

```text
Resuming training ... from epoch 17 to 100 total epochs
```

Current resume log files:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_213035.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260608_213035.stderr.log
```

Resume process observed after launch:

```text
PID 39324
```

Paused for the night on 2026-06-08. At pause time, `results.csv` contained completed epoch 31, and the process was stopped during epoch 32. Latest checkpoint:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resume next time with:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --resume runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/last.pt
```

Resumed on 2026-06-09. The resume log reports:

```text
Resuming training ... from epoch 32 to 100 total epochs
```

Current resume log files:

```text
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260609_072221.stdout.log
runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260609_072221.stderr.log
```

Resume process observed after launch:

```text
PID 13736
```

## Validation Examples

```powershell
python tools/val.py --weights runs/detect/baseline_yolo11n_visdrone/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 640 --batch 16 --device 0 --project runs/val --name baseline_val
```

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0 --project runs/val --name yolo11n_p2_coordatt_960_val
```

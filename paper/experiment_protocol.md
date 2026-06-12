# Experiment Protocol

## Project Scope

This project studies YOLO11n-based object detection on VisDrone2019-DET, with emphasis on UAV aerial small-object detection. Paper-facing metrics must be reproduced from local run artifacts or official evaluation feedback.

## Environment Snapshot

- Framework: Ultralytics YOLO.
- Local `ultralytics` version observed during project audit: `8.4.51`.
- Base model family: YOLO11n.
- Dataset config: `configs/dataset/visdrone.yaml`.
- Number of classes: 10.
- Data split:
  - train: 6471 images.
  - val: 548 images.
  - test-dev: 1580 images, without local ground-truth labels.

## Dataset

YOLO-format dataset root:

```text
data/processed/visdrone_yolo
```

Dataset conversion command:

```powershell
python scripts/convert_visdrone_to_yolo.py --raw-root data/raw/VisDrone --output-root data/processed/visdrone_yolo
```

Dataset check command:

```powershell
python scripts/check_dataset.py --dataset-root data/processed/visdrone_yolo
```

## Completed Main Experiments

| Model | Config | Run Directory | Weights | Metric Source |
| --- | --- | --- | --- | --- |
| YOLO11n baseline | `configs/train/baseline_yolo11n.yaml` | `runs/detect/baseline_yolo11n_visdrone` | `weights/best.pt` | `results.csv` |
| YOLO11n-P2 | `configs/train/yolo11n_p2.yaml` | `runs/detect/yolo11n_p2_pretrained_visdrone` | `weights/best.pt` | `results.csv` |
| YOLO11n-P2-CoordAttention | `configs/train/yolo11n_p2_coordatt.yaml` | `runs/detect/yolo11n_p2_coordatt_visdrone` | `weights/best.pt` | `results.csv` |
| YOLO11n-P2-CoordAttention-960 | `configs/train/yolo11n_p2_coordatt_960.yaml` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` | `weights/best.pt` | `results.csv` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` | `weights/best.pt` | `results.csv` |

## Completed Augmentation Ablation

Small-object-friendly augmentation:

```text
configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml
```

Key motivation:

- Close mosaic earlier by increasing `close_mosaic` from 10 to 20, reducing late-stage synthetic mosaic distribution shift.
- Reduce excessive scale variation by lowering `scale`.
- Add light `copy_paste` and disable random erasing to preserve tiny UAV targets.

Training command:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_init.pt
```

Output directory:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone
```

Observed result from `results.csv`:

| Metric | Value |
| --- | ---: |
| Final precision | 0.45208 |
| Final recall | 0.34838 |
| Final mAP50 | 0.32417 |
| Final mAP50-95 | 0.18507 |
| Best mAP50 | 0.32780 at epoch 80 |
| Best mAP50-95 | 0.18699 at epoch 74 |

## Validation

Generic validation command:

```powershell
python tools/val.py --weights path/to/best.pt --data configs/dataset/visdrone.yaml --imgsz 640 --batch 16 --device 0 --project runs/val --name experiment_name
```

For 960-input models, use:

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0 --project runs/val --name yolo11n_p2_coordatt_960_val
```

## Test-Dev Evaluation

The local test-dev split has no ground-truth labels. Local scripts can export predictions, but paper-facing test-dev metrics must come from official VisDrone evaluation feedback if available.

## Paper Artifact Rules

- Tables in `paper/tables/` should be generated from scripts whenever possible.
- Figures in `paper/figures/` should be copied from real run outputs or generated from real metrics.
- Each final paper table should retain source run paths for auditability.

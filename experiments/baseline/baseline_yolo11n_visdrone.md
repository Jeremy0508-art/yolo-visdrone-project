# Baseline: YOLO11n on VisDrone

## Purpose

Train the first full YOLO11n baseline on VisDrone2019-DET. This run is the reference experiment for later improvements such as small-object detection layers, attention modules, and data augmentation ablations.

## Command

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n.yaml --name baseline_yolo11n_visdrone
```

## Configuration

- Model: YOLO11n
- Dataset: VisDrone2019-DET
- Epochs: 100
- Image size: 640
- Batch size: 8
- Device: CUDA 0
- Workers: 0
- Optimizer: auto
- Cosine LR: true
- Close mosaic: 10
- Early stopping patience: 30

## Dataset

- Train: 6471 images, 343204 boxes
- Val: 548 images, 38759 boxes
- Test-dev: 1580 images, no public labels

## Output

- Run directory: `runs/detect/baseline_yolo11n_visdrone`
- Log file: `runs/logs/baseline_yolo11n_visdrone.log`
- Resume log file: `runs/logs/baseline_yolo11n_visdrone_resume_20260516.log`
- Best weights: `runs/detect/baseline_yolo11n_visdrone/weights/best.pt`
- Last weights: `runs/detect/baseline_yolo11n_visdrone/weights/last.pt`

## Notes

This experiment should be used as the baseline for reporting mAP50, mAP50-95, precision, recall, and per-class AP before adding model-level improvements.

## Final Result

- Epochs completed: 100
- Final precision: 0.45440
- Final recall: 0.33922
- Final mAP50: 0.31985
- Final mAP50-95: 0.18066
- Best mAP50: 0.32153 at epoch 80
- Best mAP50-95: 0.18238 at epoch 79

## Artifacts

- Summary: `experiments/baseline/baseline_yolo11n_visdrone_summary.md`
- Sample predictions: `runs/detect_image/baseline_val_samples`

## Next Experiments

1. Add a reproducible validation/report script for baseline weights.
2. Add a small-object detection head or higher-resolution training comparison.
3. Compare baseline and small-object variants using the same VisDrone val split.

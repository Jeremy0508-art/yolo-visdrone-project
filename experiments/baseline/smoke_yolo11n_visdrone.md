# Smoke Test: YOLO11n on VisDrone

## Purpose

Verify that the project can complete the data conversion, training, validation, and image inference workflow.

## Command

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n.yaml --epochs 1 --batch 8 --workers 0 --device 0 --fraction 0.05 --name smoke_yolo11n_visdrone
```

## Environment

- Model: YOLO11n
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- CUDA: available
- Dataset: VisDrone2019-DET
- Train fraction: 0.05
- Epochs: 1
- Batch size: 8

## Dataset Check

- Train: 6471 images, 343204 boxes
- Val: 548 images, 38759 boxes
- Test-dev: 1580 images, no public labels
- Invalid label lines: 0

## Result

The smoke test completed successfully.

- Output directory: `runs/detect/smoke_yolo11n_visdrone-2`
- Best weights: `runs/detect/smoke_yolo11n_visdrone-2/weights/best.pt`
- Overall val mAP50: 0.0063
- Overall val mAP50-95: 0.00259

The metric is intentionally low because this run used only 5% of the training data for 1 epoch. It is only a pipeline verification run, not a meaningful baseline.

## Inference Check

```powershell
python tools/detect_image.py --weights runs/detect/smoke_yolo11n_visdrone-2/weights/best.pt --source <val-image> --device 0 --name smoke_predict
```

- Output directory: `runs/detect_image/smoke_predict`


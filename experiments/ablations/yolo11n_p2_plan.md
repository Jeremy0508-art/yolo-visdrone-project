# YOLO11n-P2 Experiment Plan

## Goal

Evaluate whether adding a P2 high-resolution detection head improves VisDrone small-object detection compared with the YOLO11n baseline and the YOLO11n-ECA variant.

## Motivation

VisDrone contains many small and dense objects. A P2 detection head keeps a higher-resolution feature map in the detection head, which should help small targets such as pedestrians, people, bicycles, tricycles, and motors.

## Variant

- Model config: `configs/models/yolo11n_p2.yaml`
- Train config: `configs/train/yolo11n_p2.yaml`
- Added detection scale: P2/4
- Detect inputs: `[P2, P3, P4, P5]`
- Model size: 2,893,672 parameters
- Compute: 10.7 GFLOPs

## Smoke Test

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml --epochs 1 --fraction 0.01 --batch 8 --workers 0 --device 0 --name smoke_yolo11n_p2_visdrone
```

- Output: `runs/detect/smoke_yolo11n_p2_visdrone`
- Result: completed successfully

## Pretrained Smoke Test

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_pretrained_init.pt --epochs 1 --fraction 0.01 --batch 8 --workers 0 --device 0 --name smoke_yolo11n_p2_pretrained_init_visdrone
```

- Transferred tensors from YOLO11n: 288
- Loaded tensors from remapped initialization checkpoint: 593/593
- Output: `runs/detect/smoke_yolo11n_p2_pretrained_init_visdrone`
- Result: completed successfully

## Full Training Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_pretrained_init.pt --name yolo11n_p2_pretrained_visdrone
```

## Comparison Targets

| Model | Best mAP50 | Best mAP50-95 |
| --- | ---: | ---: |
| YOLO11n baseline | 0.32153 | 0.18238 |
| YOLO11n-ECA | 0.30417 | 0.17239 |
| YOLO11n-P2 | 0.33013 | 0.19012 |

## Full Training Result

- Run directory: `runs/detect/yolo11n_p2_pretrained_visdrone`
- Weights: `runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt`
- Epochs completed: 100
- Final precision: 0.44771
- Final recall: 0.35475
- Final mAP50: 0.32695
- Final mAP50-95: 0.18689
- Best mAP50: 0.33013 at epoch 86
- Best mAP50-95: 0.19012 at epoch 89

## Ablation Conclusion

The P2 detection head improves the YOLO11n baseline on VisDrone.

Compared with the baseline best metrics:

- Best mAP50 improved from 0.32153 to 0.33013.
- Best mAP50-95 improved from 0.18238 to 0.19012.

This confirms that preserving a higher-resolution detection feature map is beneficial for VisDrone small-object detection.

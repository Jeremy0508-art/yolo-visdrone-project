# YOLO11n-P2-CoordAttention Plan

## Purpose

Test whether lightweight spatially aware attention improves the current strongest model, YOLO11n-P2, without disturbing the P2/P3 small-object detection branches.

## Model Change

- Base: `configs/models/yolo11n_p2.yaml`
- New model: `configs/models/yolo11n_p2_coordatt.yaml`
- Attention: `CoordAttention`
- Placement: only after the P4 and P5 neck outputs
- Detect heads: P2, P3, P4, P5

This placement keeps the highest-resolution P2 branch unchanged and applies attention only to higher-level semantic features.

## Training Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_pretrained_init.pt
```

## Metrics To Compare

| Model | Precision | Recall | mAP50 | mAP50-95 | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 | Existing baseline |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 | Strong P2-only model |
| YOLO11n-P2-CoordAttention | 0.45375 | 0.34961 | 0.32709 | 0.18764 | Current best by best mAP50 and best mAP50-95 |

## Outcome

- P2 remains the main effective structure change for VisDrone small-object detection.
- CoordAttention gives a small positive gain over P2-only: Best mAP50 0.33073 vs 0.33013, Best mAP50-95 0.19044 vs 0.19012.
- The 640 CoordAttention checkpoint was the Web demo default before the completed 960 experiment.

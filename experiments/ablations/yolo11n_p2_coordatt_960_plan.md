# YOLO11n-P2-CoordAttention 960 Plan

## Purpose

Test whether increasing input resolution from `640` to `960` improves VisDrone small-object detection on the current strongest model, `YOLO11n-P2-CoordAttention`.

## Controlled Comparison

| Item | Baseline | New Experiment |
| --- | --- | --- |
| Model | `configs/models/yolo11n_p2_coordatt.yaml` | `configs/models/yolo11n_p2_coordatt.yaml` |
| Input size | `640` | `960` |
| Batch size | `8` | `4` |
| Epochs | `100` | `100` |
| Pretrained init | YOLO11 remapped to P2 | YOLO11 remapped to P2 |
| Run name | `yolo11n_p2_coordatt_visdrone` | `yolo11n_p2_coordatt_960_visdrone_full` |

Batch size is reduced to `4` to fit the larger input size on the same GPU.

## Training Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_960.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_960_pretrained_init.pt
```

## Smoke Test

A one-epoch smoke run has already completed at:

```text
runs/detect/yolo11n_p2_coordatt_960_smoke
```

Smoke settings:

| Setting | Value |
| --- | ---: |
| epochs | 1 |
| fraction | 0.02 |
| imgsz | 960 |
| batch | 4 |

The smoke run produced `best.pt`, `last.pt`, plots, and validation visualizations, so the model graph and training entrypoint are valid.

## Completion Status

The full 100 epoch run completed successfully on 2026-06-04 after resuming from epoch 82:

```text
runs/detect/yolo11n_p2_coordatt_960_visdrone_full
```

The run produced `results.csv`, plots, validation visualizations, and stripped `best.pt` / `last.pt` weights.

## Metrics To Compare

| Model | Best mAP50 | Best mAP50-95 | Notes |
| --- | ---: | ---: | --- |
| YOLO11n-P2-CoordAttention 640 | 0.33073 | 0.19044 | Current best completed run |
| YOLO11n-P2-CoordAttention 960 | 0.41996 | 0.25174 | Best checkpoint from the completed full run |

## Decision Rule

The 960 model improves both `Best mAP50` and `Best mAP50-95`, so it should be treated as the strongest completed checkpoint when GPU memory allows.

# YOLO11n-P2-CoordAttention Small-Object Augmentation Plan

## Purpose

Test whether VisDrone-specific augmentation improves the current best `YOLO11n-P2-CoordAttention` model while keeping input size at `640`.

## Changes

| Setting | Current | New |
| --- | ---: | ---: |
| `close_mosaic` | 10 | 20 |
| `scale` | 0.5 | 0.35 |
| `copy_paste` | 0.0 | 0.1 |
| `erasing` | 0.4 | 0.0 |

Rationale:

- Keep mosaic active longer to expose crowded small-object scenes for more epochs.
- Reduce scale jitter so very small objects are less often shrunk into near-invisible targets.
- Add light copy-paste to increase object density.
- Disable random erasing because VisDrone objects are already small and often occluded.

## Training Command

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_pretrained_init.pt
```

## Smoke Test

A one-epoch smoke run has completed at:

```text
runs/detect/yolo11n_p2_coordatt_smallobj_aug_smoke
```

Smoke command:

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --epochs 1 --fraction 0.02 --name yolo11n_p2_coordatt_smallobj_aug_smoke --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_smoke_init.pt
```

The smoke run produced `best.pt`, `last.pt`, plots, and validation visualizations. Peak observed GPU memory was about 5.86 GB on an RTX 4060 Laptop GPU with `batch=8`.

## Metrics To Compare

| Model | Best mAP50 | Best mAP50-95 | Notes |
| --- | ---: | ---: | --- |
| YOLO11n-P2-CoordAttention | 0.33073 | 0.19044 | Current best completed run |
| YOLO11n-P2-CoordAttention small-object augmentation | TBD | TBD | Run full training with the command above |

## Decision Rule

If this run improves recall or `Best mAP50-95`, keep the augmentation strategy for the next combined experiment. If it improves recall but lowers precision noticeably, inspect confusion matrices and dense-scene cases before promoting it.

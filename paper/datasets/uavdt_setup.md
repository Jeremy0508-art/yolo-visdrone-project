# UAVDT Dataset Setup for IEEE Transactions Experiments

## Purpose

UAVDT is the recommended second dataset for the IEEE Transactions route, especially if the target venue is IEEE Transactions on Intelligent Transportation Systems. It provides UAV-captured traffic scenes and vehicle annotations, making it a better cross-dataset validation partner for VisDrone than another generic object-detection dataset.

This document records the intended local dataset layout and conversion flow. No UAVDT result should enter the paper until the converted dataset has passed integrity checks and the corresponding training logs exist.

For the step-by-step acquisition, conversion, preview, troubleshooting, and sync checklist, see `paper/datasets/uavdt_operational_checklist.md`.

## Sources

- Official UAVDT project page: `https://sites.google.com/view/grli-uavdt`
- UAVDT paper: `https://openaccess.thecvf.com/content_ECCV_2018/papers/Dawei_Du_The_Unmanned_Aerial_ECCV_2018_paper.pdf`

The UAVDT paper describes the benchmark as about 80,000 representative UAV frames from 10 hours of raw videos, covering detection, single-object tracking, and multi-object tracking. It also describes traffic-related vehicle categories such as car, truck, and bus, with attributes for occlusion, out-of-view, altitude, view, and weather.

## Expected Local Layout

Place the raw UAVDT files under:

```text
data/raw/UAVDT/
```

The converter is designed to tolerate common UAVDT layouts, including sequence folders with image subdirectories named `img1`, `images`, or `JPEGImages`, and annotation files such as:

```text
gt.txt
gt_whole.txt
<sequence>_gt.txt
<sequence>_gt_whole.txt
```

Converted YOLO-format files will be written to:

```text
data/processed/uavdt_yolo/
```

with the standard YOLO layout:

```text
data/processed/uavdt_yolo/
  images/train/
  images/val/
  images/test/
  labels/train/
  labels/val/
  labels/test/
```

## Class Mapping

The initial IEEE plan uses the official UAVDT vehicle-category setting:

| YOLO ID | Class |
| ---: | --- |
| 0 | car |
| 1 | truck |
| 2 | bus |

If the downloaded UAVDT variant contains additional classes such as `van` or `other_vehicle`, the mapping must be manually audited before training. Do not silently merge classes without documenting the mapping decision.

## Conversion Command

```powershell
python scripts/convert_uavdt_to_yolo.py `
  --raw-root data/raw/UAVDT `
  --output-root data/processed/uavdt_yolo `
  --overwrite
```

After conversion, inspect the generated summary and run a dataset check:

```powershell
python scripts/check_dataset.py `
  --dataset-root data/processed/uavdt_yolo `
  --data-yaml configs/dataset/uavdt.yaml `
  --splits train val test `
  --preview-count 8 `
  --preview-dir runs/dataset_checks/uavdt
```

The dataset checker can load class names from the UAVDT YAML through `--data-yaml`, so preview images should display the UAVDT class labels rather than VisDrone labels.

## Training Config

The YOLO data config is:

```text
configs/dataset/uavdt.yaml
```

Minimum first experiments:

```powershell
python tools/train_baseline.py --model yolo11n.pt --data configs/dataset/uavdt.yaml --imgsz 960 --epochs 100 --name baseline_yolo11n_960_uavdt
```

For P2 or custom-model experiments, use the same naming rule and record the exact command in `paper/commands.md` or the future IEEE experiment registry before using any metric in the manuscript.

## Integrity Gates

Before training:

- Raw image count and annotation count are recorded.
- At least one preview image per split has visually correct boxes.
- Class IDs are within `[0, 2]`.
- Empty-label images are counted and accepted only if expected.
- Train/val/test split origin is documented.

Before manuscript use:

- `results.csv`, `args.yaml`, `weights/best.pt`, `weights/last.pt`, and training log exist.
- Metrics are exported to an IEEE-specific table.
- Scale-wise metrics are computed for UAVDT or the limitation is explicitly stated.

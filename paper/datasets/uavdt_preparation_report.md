# UAVDT Preparation Report

This report records the real UAVDT preparation work performed for the IEEE Transactions route. It is a data-preparation and queue-status record, not an experimental-result table.

## Source Record

| Item | Evidence |
| --- | --- |
| Official project page | https://sites.google.com/view/grli-uavdt |
| Download mirror used on the server | https://zenodo.org/records/14575517 |
| Archive path on server | `/root/autodl-tmp/yolo-visdrone-project/data/raw/UAVDT_archives/UAVDT_zenodo.zip` |
| Archive size | 4,026,830,525 bytes |
| MD5 | `19f318b1d5e97a47e3dd30ec5bff182b` |
| Extraction root | `/root/autodl-tmp/yolo-visdrone-project/data/raw/UAVDT` |
| Prepared YOLO root | `/root/autodl-tmp/yolo-visdrone-project/data/processed/uavdt_yolo` |

The official Google Drive download was not reachable from the rented server network during this preparation step, so the Zenodo mirror was used and checked by MD5 before extraction.

## Layout Decision

The downloaded archive already uses a YOLO-style split layout:

```text
UAVDT/
  train/images/
  train/labels/
  val/images/
  val/labels/
  test/images/
  test/labels/
```

Because the archive already contains YOLO label files, the MOT-style converter `scripts/convert_uavdt_to_yolo.py` was not used for this archive. Instead, `tools/prepare_uavdt_yolo_layout.py` reorganized the existing YOLO layout into the project layout required by `configs/dataset/uavdt.yaml`:

```text
data/processed/uavdt_yolo/
  images/train/
  images/val/
  images/test/
  labels/train/
  labels/val/
  labels/test/
```

## Preparation Commands

```bash
cd /root/autodl-tmp/yolo-visdrone-project

/root/miniconda3/bin/python tools/prepare_uavdt_yolo_layout.py \
  --source-root data/raw/UAVDT \
  --output-root data/processed/uavdt_yolo \
  --overwrite

/root/miniconda3/bin/python scripts/check_dataset.py \
  --dataset-root data/processed/uavdt_yolo \
  --data-yaml configs/dataset/uavdt.yaml \
  --splits train val test \
  --preview-count 8 \
  --preview-dir runs/dataset_checks/uavdt
```

## Dataset Statistics

These numbers come from `paper/datasets/uavdt_prepare_summary.json` and the server-side dataset checker.

| Split | Images | Label files | Boxes | Missing labels | Empty labels | Invalid lines |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 1266 | 1266 | 35007 | 0 | 0 | 0 |
| val | 271 | 271 | 7046 | 0 | 0 | 0 |
| test | 272 | 272 | 7957 | 0 | 0 | 0 |

Ultralytics cache creation reported three duplicate label rows in the training split and removed them in the cache:

- `DJI_0955 (6_23)_n0.jpg`
- `lim_1050.jpg`
- `lim_3630.jpg`

No corrupt images were reported by the training cache scan.

## Training Queue Status

The UAVDT queue was started on the rented RTX 4090 server:

```bash
bash tools/start_ieee_uavdt_queue.sh
```

Queue log:

```text
/root/autodl-tmp/yolo-visdrone-project/runs/logs/ieee_uavdt_queue_latest.log
```

First active run at launch:

```text
baseline_yolo11n_960_uavdt
```

The queue is configured to run the following 960-input experiments in order:

| Order | Experiment | Config |
| ---: | --- | --- |
| 1 | YOLO11n-960 on UAVDT | `configs/train/baseline_yolo11n_960_uavdt.yaml` |
| 2 | YOLO11n-P2-960 on UAVDT | `configs/train/yolo11n_p2_960_uavdt.yaml` |
| 3 | YOLOv8n-960 on UAVDT | `configs/train/baseline_yolov8n_960_uavdt.yaml` |
| 4 | YOLO11s-960 on UAVDT | `configs/train/baseline_yolo11s_960_uavdt.yaml` |

## Manuscript Boundary

UAVDT should not be used as completed cross-dataset evidence until the four training runs finish, the result files are synced, and the IEEE audits are refreshed. This report only proves that the dataset source, layout, integrity checks, and training queue are in place.

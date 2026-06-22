# UAVDT Operational Checklist

This checklist is for the IEEE Transactions route. It records the practical steps for acquiring, converting, validating, and integrating UAVDT. Do not use UAVDT in manuscript claims until every required gate is complete.

## Stage 1: Raw Data Placement

Expected raw root:

```text
data/raw/UAVDT/
```

Before conversion, record:

| Item | Expected Evidence |
| --- | --- |
| Raw dataset source | Official UAVDT project page or documented mirror |
| Download archive names | File names and sizes |
| Extraction path | `data/raw/UAVDT/` |
| Sequence count | Output of `Get-ChildItem data/raw/UAVDT -Recurse -Directory` or Linux `find` |
| Annotation files found | `gt.txt`, `gt_whole.txt`, `*_gt.txt`, or `*_gt_whole.txt` |
| Image folders found | `img1`, `images`, `JPEGImages`, `Imgs`, or direct image files |

Recommended inspection commands:

```powershell
Get-ChildItem data\raw\UAVDT -Recurse -Directory | Select-Object -First 50 FullName
Get-ChildItem data\raw\UAVDT -Recurse -Include gt.txt,gt_whole.txt,*_gt.txt,*_gt_whole.txt | Select-Object -First 50 FullName
Get-ChildItem data\raw\UAVDT -Recurse -Include *.jpg,*.png,*.jpeg | Select-Object -First 10 FullName
```

## Stage 2: Conversion

Primary conversion command:

```powershell
python scripts\convert_uavdt_to_yolo.py `
  --raw-root data/raw/UAVDT `
  --output-root data/processed/uavdt_yolo `
  --overwrite
```

If the raw layout has extra classes and the annotation meaning is confirmed:

```powershell
python scripts\convert_uavdt_to_yolo.py `
  --raw-root data/raw/UAVDT `
  --output-root data/processed/uavdt_yolo `
  --overwrite `
  --include-unknown-classes
```

Do not use `--include-unknown-classes` by default. The current IEEE plan maps official UAVDT categories to:

| Raw ID | YOLO ID | Class |
| ---: | ---: | --- |
| 1 | 0 | car |
| 2 | 1 | truck |
| 3 | 2 | bus |

If a downloaded variant includes `van`, `other_vehicle`, or non-vehicle classes, document the mapping before training.

If the downloaded archive already contains a YOLO-style layout such as `train/images`, `train/labels`, `val/images`, and `val/labels`, do not run the MOT-style converter. Use the layout preparation script instead:

```powershell
python tools\prepare_uavdt_yolo_layout.py `
  --source-root data/raw/UAVDT `
  --output-root data/processed/uavdt_yolo `
  --overwrite
```

The 2026-06-20 server preparation followed this YOLO-layout branch. See `paper/datasets/uavdt_preparation_report.md` for the source archive, MD5, split statistics, dataset-check output, and queue log path.

## Stage 3: Dataset Integrity Check

Run:

```powershell
python scripts\check_dataset.py `
  --dataset-root data/processed/uavdt_yolo `
  --data-yaml configs/dataset/uavdt.yaml `
  --splits train val test `
  --preview-count 8 `
  --preview-dir runs/dataset_checks/uavdt
```

Required checks:

| Gate | Pass Condition |
| --- | --- |
| Images found | `images/train` and `images/val` are non-empty |
| Labels found | Label files exist for converted images |
| Class IDs valid | No class ID outside `[0, 2]` |
| Box values valid | YOLO coordinates are all within `[0, 1]` |
| Preview correct | Random preview images show boxes aligned with vehicles |
| Empty labels understood | Empty-label images, if any, are expected and counted |
| Split source documented | Train/val/test origin or fallback split rule is recorded |

## Stage 4: Visual Preview Review

Open:

```text
runs/dataset_checks/uavdt/train/
runs/dataset_checks/uavdt/val/
runs/dataset_checks/uavdt/test/
```

Manual review questions:

1. Are boxes aligned with vehicles?
2. Are class names `car`, `truck`, and `bus` displayed correctly?
3. Are there many missing labels for visibly annotated frames?
4. Are frame numbers and sequence names preserved enough to trace back to raw files?
5. Are boxes clipped incorrectly near image borders?

If previews are wrong, stop before training and inspect:

- Annotation column order.
- Frame filename convention.
- Image size reading.
- Class ID mapping.
- Raw sequence folder layout.

## Stage 5: First Training Queue

Only after conversion and preview pass:

```bash
RUN_TRAINING=1 RUN_UAVDT=1 RUN_SCALE=0 ./tools/run_ieee_server_queue.sh
```

Minimum first UAVDT experiments:

| Experiment | Config |
| --- | --- |
| YOLO11n-960 | `configs/train/baseline_yolo11n_960_uavdt.yaml` |
| YOLO11n-P2-960 | `configs/train/yolo11n_p2_960_uavdt.yaml` |
| YOLOv8n-960 | `configs/train/baseline_yolov8n_960_uavdt.yaml` |
| YOLO11s-960 | `configs/train/baseline_yolo11s_960_uavdt.yaml` |

TOFC on UAVDT should be launched only if VisDrone TOFC results justify it.

## Stage 6: Result Sync and Manuscript Gate

Check remote progress:

```powershell
.\tools\check_ieee_server_status.ps1
python tools\build_ieee_server_progress_report.py
```

Sync only complete runs:

```powershell
.\tools\sync_ieee_server_results.ps1 -MinEpochs 100
```

Post-sync:

```powershell
python tools\check_ieee_claims.py
python tools\check_ieee_phase1_artifacts.py
python tools\build_ieee_submission_dashboard.py
```

UAVDT can support manuscript claims only after complete run evidence and refreshed audits exist.

## Common Failure Cases

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| No sequences discovered | Raw layout differs from expected image/annotation names | Inspect folders and update `IMAGE_DIR_NAMES` or `ANNOTATION_NAMES`. |
| Many missing images | Frame IDs do not match image filenames | Extend `find_frame_image()` naming patterns. |
| Boxes shifted or too large | Annotation columns differ from assumed MOT-like format | Inspect raw annotation specification before modifying parser. |
| All labels become `car` | `--include-unknown-classes` was used too early | Recheck raw class IDs and mapping. |
| Validation split empty | Folder names do not expose split and fallback ratio failed | Set explicit split logic or reorganize raw folders. |
| Preview labels show VisDrone classes | `--data-yaml configs/dataset/uavdt.yaml` was omitted | Rerun dataset checker with UAVDT YAML. |

## Evidence Boundary

UAVDT is currently a planned second dataset, not completed evidence. Do not write "cross-dataset generalization" or "generalizes to UAVDT" until this checklist is complete and the corresponding experiments have been synced and audited.

# IEEE Local Scale-Bin AP Protocol

Status: tool protocol. Full VisDrone validation output is available for completed models.

This document defines the optional AP-style scale-bin evaluation added for the IEEE Transactions route. It complements the completed scale-wise recall/precision output from `tools/evaluate_scale_groups.py`.

## Purpose

The completed scale-wise table reports recall and precision by object scale. Reviewers may also expect AP-style evidence when a manuscript discusses small-object detection. The new script:

```text
tools/evaluate_scale_ap.py
```

computes local scale-bin AP50 and mAP50-95 from YOLO-format labels and model predictions.

## Important Boundary

This is not an official COCO or VisDrone `AP_small` evaluator.

By default, the script uses:

- COCO-style scale bins based on box area:
  - small: `< 32 x 32`
  - medium: `[32 x 32, 96 x 96)`
  - large: `>= 96 x 96`
- prediction confidence threshold `0.001` for AP curves
- NMS IoU threshold `0.7`
- AP IoU thresholds from `0.50` to `0.95` in 10 steps
- `same-bin` prediction filtering, meaning GT boxes and predicted boxes are evaluated within the same scale bin

Therefore manuscript wording should say "local scale-bin AP" unless an official evaluator is used.

## Smoke Test

A one-image CPU smoke test has passed. The temporary smoke CSV and figure were deleted and must not be used as paper evidence.

Smoke command:

```powershell
python tools\evaluate_scale_ap.py `
  --limit-images 1 `
  --device cpu `
  --output paper\tables\ieee_scale_ap_smoke.csv `
  --plot-output paper\figures\scale_analysis\ieee_scale_ap_smoke.png
```

## Full Evaluation Command

Run only when compute is available:

```powershell
python tools\evaluate_scale_ap.py `
  --dataset-root data/processed/visdrone_yolo `
  --dataset-name VisDrone2019-DET `
  --split val `
  --targets-csv paper/tables/ieee_scale_eval_targets.csv `
  --output paper/tables/ieee_scale_ap_results_visdrone.csv `
  --plot-output paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png `
  --device 0
```

CPU or `--limit-images` runs are for smoke testing only.

## Output Columns

| Column | Meaning |
| --- | --- |
| `model` | Model label from target CSV |
| `weights` | Weight file used for prediction |
| `imgsz` | Inference image size |
| `nms_conf` | Prediction confidence threshold |
| `nms_iou` | NMS IoU threshold |
| `prediction_scale_policy` | Whether predictions are filtered to the same scale bin |
| `scale` | small, medium, or large |
| `gt_instances` | Number of GT instances in the scale bin |
| `predictions` | Number of predictions considered in the scale bin |
| `precision_at_max_f1` | Mean per-class precision at max-F1 threshold from `ap_per_class` |
| `recall_at_max_f1` | Mean per-class recall at max-F1 threshold from `ap_per_class` |
| `ap50` | Local scale-bin AP at IoU 0.50 |
| `map50_95` | Local scale-bin mAP over IoU 0.50:0.95 |

## Manuscript Use

Allowed after full output is generated and audited:

> The local scale-bin AP analysis reports AP50 and mAP50-95 within small, medium, and large object groups. These values are used as an auxiliary diagnostic and are not treated as official COCO AP_small metrics.

Not allowed:

- "The method improves official AP_small."
- "The method improves COCO AP_small."
- "The method improves VisDrone small-object AP" unless the metric definition is explicitly stated as local scale-bin AP.

## Current Status

| Item | Status | Evidence |
| --- | --- | --- |
| AP-size script | Ready | `tools/evaluate_scale_ap.py` |
| One-image smoke test | Passed | temporary smoke files deleted |
| Full VisDrone AP-size output | Ready | `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| Full AP50 scale figure | Ready | `paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png` |

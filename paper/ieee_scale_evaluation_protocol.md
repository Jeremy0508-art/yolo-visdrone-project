# IEEE Scale-Wise Evaluation Protocol

This document defines how scale-wise small-object evidence should be generated and interpreted for the IEEE Transactions route.

## Purpose

Overall mAP is not enough for a small-object detection paper. A claim such as "improves small-object detection" must be supported by metrics grouped by object scale.

The current scale bins follow COCO-style object areas:

| Scale | GT Box Area |
| --- | --- |
| small | `< 32 x 32` pixels |
| medium | `[32 x 32, 96 x 96)` pixels |
| large | `>= 96 x 96` pixels |

The evaluation is implemented in:

```text
tools/evaluate_scale_groups.py
```

## Existing Preliminary Evidence

The existing file:

```text
paper/tables/scale_group_results.csv
```

contains an earlier two-model scale-wise evaluation:

- YOLO11n baseline at 640.
- YOLO11n-P2-CoordAttention-960.

This is useful as preliminary evidence, but it is not the full IEEE target evaluation because it does not include all 960 fair-comparison targets and does not include the pending TOFC model.

## Full IEEE Target List

The full VisDrone target list is:

```text
paper/tables/ieee_scale_eval_targets.csv
```

Current enabled targets:

- YOLO11n-960.
- YOLO11n-P2-960.
- YOLO11n-P2-CA-960.
- YOLOv8n-960.
- YOLO11s-960.

TOFC is present in the target list but disabled until its weights exist.

## Full Evaluation Command

Run only when the required weights are available:

```powershell
python tools\evaluate_scale_groups.py `
  --dataset-root data/processed/visdrone_yolo `
  --dataset-name VisDrone2019-DET `
  --split val `
  --targets-csv paper/tables/ieee_scale_eval_targets.csv `
  --output paper/tables/ieee_scale_results_visdrone.csv `
  --plot-output paper/figures/scale_analysis/ieee_scale_recall_visdrone.png `
  --device 0
```

CPU or `--limit-images` runs are allowed only for smoke tests and must not be used in paper claims.

## Output Interpretation

The output table records:

| Column | Meaning |
| --- | --- |
| `model` | Model label from the target CSV |
| `dataset` | Dataset name written by the command |
| `weights` | Weight file used for prediction |
| `split` | Evaluated split |
| `imgsz` | Inference image size |
| `conf` | Prediction confidence threshold |
| `iou` | Matching IoU threshold |
| `scale` | GT/prediction scale group |
| `gt_instances` | Number of GT instances in the scale group |
| `matched_gt` | GT instances matched by predictions |
| `recall` | `matched_gt / gt_instances` |
| `predictions` | Number of predictions in that scale group |
| `true_positive_predictions` | Predictions matched to GT |
| `precision` | `true_positive_predictions / predictions` |

This script reports recall/precision by scale group. It does not compute COCO AP-small/AP-medium/AP-large. Therefore, manuscript wording should say "scale-wise recall/precision" unless a separate AP computation is added.

## Claim Rules

| Claim | Required Evidence |
| --- | --- |
| "The model improves small-object recall" | `small` recall improves over a matched baseline in `paper/tables/ieee_scale_results_visdrone.csv`. |
| "The model improves small-object precision" | `small` precision improves over a matched baseline in the same full evaluation table. |
| "The model improves small-object detection overall" | Both scale-wise metrics and overall mAP should support the claim, or the wording must specify the exact metric. |
| "The method is robust across scales" | Small, medium, and large groups should be reported, including any trade-offs. |
| "The method improves tiny-object AP" | Not allowed from this script alone; AP-specific evaluation is needed. |

## Integration Gate

Before scale-wise evidence enters the IEEE manuscript:

1. `paper/tables/ieee_scale_results_visdrone.csv` exists.
2. `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` exists.
3. All enabled targets from `paper/tables/ieee_scale_eval_targets.csv` appear in the output.
4. Each enabled target has rows for small, medium, and large.
5. `conf`, `iou`, split, dataset name, and weights are documented.
6. `tools/check_ieee_scale_outputs.py` reports the full output as ready.

## Current Boundary

The existing two-model `scale_group_results.csv` can inform planning and discussion, but the IEEE manuscript should wait for the full target-list output before making central small-object claims.

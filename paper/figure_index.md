# Figure Index for Paper Draft

This file records paper-facing figures copied from real experiment outputs. Do not use a figure in the paper unless its source run is listed here or in the corresponding table/log files.

## Recommended Main Figures

| Paper Use | Figure File | Source | Suggested Caption |
| --- | --- | --- | --- |
| Training convergence comparison | `paper/figures/training_curves/p2_coordatt_960_results.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png` | Training and validation curves of the best completed YOLO11n-P2-CoordAttention-960 model on VisDrone. |
| PR curve of best model | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png` | Precision-recall curve of the best completed model on the validation set. |
| Normalized confusion matrix | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png` | Normalized confusion matrix of the best completed model. |
| Object scale distribution | `paper/figures/scale_analysis/object_scale_distribution.png` | `paper/tables/object_scale_distribution.csv` | Distribution of small, medium, and large objects in the VisDrone train and validation sets. |
| Scale-group recall comparison | `paper/figures/scale_analysis/scale_group_recall.png` | `paper/tables/scale_group_results.csv` | Thresholded scale-group recall comparison between YOLO11n baseline and YOLO11n-P2-CoordAttention-960. |
| Qualitative detection results | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg` | Representative detection results on VisDrone validation images. |
| Failure/error analysis | `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | Existing visual asset under `experiments/figures/` | Example failure cases for qualitative analysis. |

## Training Curves and PR Curves

| Model | Results Curve | PR Curve | Source Run |
| --- | --- | --- | --- |
| YOLO11n baseline | `paper/figures/training_curves/baseline_results.png` | `paper/figures/training_curves/baseline_pr_curve.png` | `runs/detect/baseline_yolo11n_visdrone` |
| YOLO11n-P2 | `paper/figures/training_curves/p2_results.png` | `paper/figures/training_curves/p2_pr_curve.png` | `runs/detect/yolo11n_p2_pretrained_visdrone` |
| YOLO11n-P2-CoordAttention | `paper/figures/training_curves/p2_coordatt_results.png` | `paper/figures/training_curves/p2_coordatt_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_visdrone` |
| YOLO11n-P2-CoordAttention-960 | `paper/figures/training_curves/p2_coordatt_960_results.png` | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `paper/figures/training_curves/p2_coordatt_smallobj_aug_results.png` | `paper/figures/training_curves/p2_coordatt_smallobj_aug_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |

## Confusion Matrices

| Model | Figure File | Source Run |
| --- | --- | --- |
| YOLO11n baseline | `paper/figures/confusion_matrices/baseline_confusion_matrix_normalized.png` | `runs/detect/baseline_yolo11n_visdrone` |
| YOLO11n-P2 | `paper/figures/confusion_matrices/p2_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_pretrained_visdrone` |
| YOLO11n-P2-CoordAttention | `paper/figures/confusion_matrices/p2_coordatt_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_visdrone` |
| YOLO11n-P2-CoordAttention-960 | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `paper/figures/confusion_matrices/p2_coordatt_smallobj_aug_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |

## Scale Analysis Figures

| Figure File | Source Data | Source Script |
| --- | --- | --- |
| `paper/figures/scale_analysis/object_scale_distribution.png` | `paper/tables/object_scale_distribution.csv` | `tools/analyze_object_scales.py` |
| `paper/figures/scale_analysis/scale_group_recall.png` | `paper/tables/scale_group_results.csv` | `tools/evaluate_scale_groups.py` |

## Qualitative Figures

| Model | Figure File | Source Run |
| --- | --- | --- |
| YOLO11n-P2-CoordAttention-960 | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| YOLO11n-P2-CoordAttention-960 | `paper/figures/qualitative/p2_coordatt_960_val_batch1_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| YOLO11n-P2-CoordAttention-960 | `paper/figures/qualitative/p2_coordatt_960_val_batch2_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `paper/figures/qualitative/p2_coordatt_smallobj_aug_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `paper/figures/qualitative/p2_coordatt_smallobj_aug_val_batch1_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |
| YOLO11n-P2-CoordAttention-SmallObjAug | `paper/figures/qualitative/p2_coordatt_smallobj_aug_val_batch2_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |

## Notes for Writing

- The current best completed model is YOLO11n-P2-CoordAttention-960 according to validation mAP.
- The small-object augmentation experiment is useful as an ablation result: it improves over the original YOLO11n baseline but does not surpass the P2/CoordAttention/960 setting.
- Official VisDrone test-dev/test-challenge AP should not be reported unless the official server returns a result. The local zip package is only evidence that the submission file was prepared.
- The older `experiments/visual_assets.md` should be treated as historical material because it was written before the 960 and small-object augmentation experiments were fully organized.

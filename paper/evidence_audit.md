# Evidence Audit for Paper Manuscripts

This audit checks the main paper-facing numbers in `paper/manuscript_polished.md` and `paper/manuscript_submission_candidate.tex` against existing result tables and generated artifacts. No official VisDrone test-dev/test-challenge AP is available yet.

The current target track is the 《计算机工程与应用》 journal submission plan recorded in `paper/CEA_JOURNAL_MASTER_PLAN.md`. New fair-comparison experiments must be added here only after complete 100-epoch runs are synchronized and audited.

## Main Result Claims

| Claim in Manuscript | Value | Evidence Source | Status |
| --- | ---: | --- | --- |
| YOLO11n baseline best mAP50 | 0.32153 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n baseline best mAP50-95 | 0.18238 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2 best mAP50 | 0.33013 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2 best mAP50-95 | 0.19012 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention best mAP50 | 0.33073 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention best mAP50-95 | 0.19044 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 best mAP50 | 0.41996 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 best mAP50-95 | 0.25174 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention-SmallObjAug best mAP50 | 0.32780 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLO11n-P2-CoordAttention-SmallObjAug best mAP50-95 | 0.18699 | `paper/tables/main_comparison_for_paper.csv` | Verified |
| YOLOv8n baseline best mAP50 | 0.32520 | `paper/tables/main_comparison_for_paper.csv` | Verified external baseline |
| YOLOv8n baseline best mAP50-95 | 0.18386 | `paper/tables/main_comparison_for_paper.csv` | Verified external baseline |
| YOLO11s baseline best mAP50 | 0.38937 | `paper/tables/main_comparison_for_paper.csv` | Verified external baseline |
| YOLO11s baseline best mAP50-95 | 0.22719 | `paper/tables/main_comparison_for_paper.csv` | Verified external baseline |

## Ablation Delta Claims

| Claim in Manuscript | Value | Evidence Source | Status |
| --- | ---: | --- | --- |
| P2 mAP50 gain over baseline | +0.00860 | `paper/tables/ablation_results.csv` | Verified |
| P2 mAP50-95 gain over baseline | +0.00774 | `paper/tables/ablation_results.csv` | Verified |
| CoordAttention mAP50 gain over baseline | +0.00920 | `paper/tables/ablation_results.csv` | Verified |
| CoordAttention mAP50-95 gain over baseline | +0.00806 | `paper/tables/ablation_results.csv` | Verified |
| 960-input mAP50 gain over baseline | +0.09843 | `paper/tables/ablation_results.csv` | Verified |
| 960-input mAP50-95 gain over baseline | +0.06936 | `paper/tables/ablation_results.csv` | Verified |
| SmallObjAug mAP50 gain over baseline | +0.00627 | `paper/tables/ablation_results.csv` | Verified |
| SmallObjAug mAP50-95 gain over baseline | +0.00461 | `paper/tables/ablation_results.csv` | Verified |

## Speed and Complexity Claims

| Claim in Manuscript | Value | Evidence Source | Status |
| --- | ---: | --- | --- |
| YOLO11n params | 2.592 M | `paper/tables/main_comparison_for_paper.csv`, `paper/tables/model_complexity.csv` | Verified |
| YOLO11n GFLOPs | 6.5 | `paper/tables/main_comparison_for_paper.csv`, `paper/tables/model_complexity.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 params | 2.904 M | `paper/tables/main_comparison_for_paper.csv`, `paper/tables/model_complexity.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 GFLOPs | 10.7 | `paper/tables/main_comparison_for_paper.csv`, `paper/tables/model_complexity.csv` | Verified |
| YOLO11n average wall-clock latency | 40.092 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n FPS | 24.94 | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention latency | 45.768 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention FPS | 21.85 | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 latency | 50.811 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 FPS | 19.68 | `paper/tables/speed_results.csv` | Verified |
| YOLOv8n FPS | 23.65 | `paper/tables/speed_results.csv` | Verified external baseline |
| YOLO11s FPS | 25.66 | `paper/tables/speed_results.csv` | Verified external baseline |

## Scale Analysis Claims

| Claim in Manuscript | Value | Evidence Source | Status |
| --- | ---: | --- | --- |
| VisDrone train small objects | 207604 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone train medium objects | 116620 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone train large objects | 18980 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone train small-object ratio | 0.604900 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone val small objects | 26586 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone val medium objects | 11105 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone val large objects | 1068 | `paper/tables/object_scale_distribution.csv` | Verified |
| VisDrone val small-object ratio | 0.685931 | `paper/tables/object_scale_distribution.csv` | Verified |
| YOLO11n baseline small-scale recall at conf=0.25, IoU=0.5 | 0.307681 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |
| YOLO11n-P2-CoordAttention-960 small-scale recall at conf=0.25, IoU=0.5 | 0.455089 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |
| YOLO11n baseline medium-scale recall at conf=0.25, IoU=0.5 | 0.711932 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |
| YOLO11n-P2-CoordAttention-960 medium-scale recall at conf=0.25, IoU=0.5 | 0.781450 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |
| YOLO11n baseline large-scale recall at conf=0.25, IoU=0.5 | 0.869850 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |
| YOLO11n-P2-CoordAttention-960 large-scale recall at conf=0.25, IoU=0.5 | 0.882022 | `paper/tables/scale_group_results.csv` | Verified thresholded matching result |

Scale-group values are not official AP. They are generated by `tools/evaluate_scale_groups.py` from validation-set predictions and YOLO-format labels, using the configured `conf` and `IoU` thresholds.

## Figure Claims

| Figure Use | File | Evidence Source | Status |
| --- | --- | --- | --- |
| Best model training curves | `paper/figures/training_curves/p2_coordatt_960_results.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png` | Verified |
| Best model PR curve | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png` | Verified |
| Best model normalized confusion matrix | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png` | Verified |
| Best model qualitative validation image | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg` | Verified |
| Failure-case contact sheet | `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | Existing `experiments/figures/` visual asset | Verified as qualitative material |
| Object scale distribution | `paper/figures/scale_analysis/object_scale_distribution.png` | `paper/tables/object_scale_distribution.csv` generated by `tools/analyze_object_scales.py` | Verified |
| Scale-group recall comparison | `paper/figures/scale_analysis/scale_group_recall.png` | `paper/tables/scale_group_results.csv` generated by `tools/evaluate_scale_groups.py` | Verified |
| Accuracy-speed-parameter trade-off | `paper/figures/tradeoff/accuracy_speed_tradeoff.png` | `paper/tables/accuracy_speed_tradeoff.csv` generated by `tools/plot_accuracy_speed_tradeoff.py` | Verified |

## Known Limitations

- The manuscript reports validation-set metrics only.
- The local VisDrone submission zip is prepared, but no official AP has been returned.
- Speed numbers are single-image `model.predict` wall-clock results from `tools/benchmark_speed.py`, not universal deployment FPS.
- Small-object augmentation is an ablation result. It improves over baseline but is not the best completed model.

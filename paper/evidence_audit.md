# Evidence Audit for `manuscript_polished.md`

This audit checks the main paper-facing numbers in `paper/manuscript_polished.md` against existing result tables and generated artifacts. No official VisDrone test-dev/test-challenge AP is available yet.

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
| YOLO11n average wall-clock latency | 13.785 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n FPS | 72.54 | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention latency | 15.347 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention FPS | 65.16 | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 latency | 17.733 ms | `paper/tables/speed_results.csv` | Verified |
| YOLO11n-P2-CoordAttention-960 FPS | 56.39 | `paper/tables/speed_results.csv` | Verified |

## Figure Claims

| Figure Use | File | Evidence Source | Status |
| --- | --- | --- | --- |
| Best model training curves | `paper/figures/training_curves/p2_coordatt_960_results.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png` | Verified |
| Best model PR curve | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png` | Verified |
| Best model normalized confusion matrix | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png` | Verified |
| Best model qualitative validation image | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg` | Verified |
| Failure-case contact sheet | `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | Existing `experiments/figures/` visual asset | Verified as qualitative material |

## Known Limitations

- The manuscript reports validation-set metrics only.
- The local VisDrone submission zip is prepared, but no official AP has been returned.
- Speed numbers are single-image `model.predict` wall-clock results from `tools/benchmark_speed.py`, not universal deployment FPS.
- Small-object augmentation is an ablation result. It improves over baseline but is not the best completed model.

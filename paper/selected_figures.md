# 正文推荐图清单

本文件从 `paper/figure_index.md` 中筛选正式论文正文建议使用的核心图。筛选原则是：优先使用当前最佳模型 YOLO11n-P2-CoordAttention-960 的真实输出图，并覆盖训练过程、精度曲线、类别混淆、定性检测和误差分析。

## 推荐正文图

| 图号建议 | 文件 | 来源 | 用途 | 建议图题 |
| --- | --- | --- | --- | --- |
| 图 1 | `paper/figures/training_curves/p2_coordatt_960_results.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png` | 展示最佳模型训练收敛过程 | YOLO11n-P2-CoordAttention-960 训练过程曲线 |
| 图 2 | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png` | 展示最佳模型 PR 曲线 | YOLO11n-P2-CoordAttention-960 在验证集上的 PR 曲线 |
| 图 3 | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png` | 展示类别混淆情况 | YOLO11n-P2-CoordAttention-960 归一化混淆矩阵 |
| 图 4 | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg` | 展示检测可视化结果 | VisDrone 验证集检测结果示例 |
| 图 5 | `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | `experiments/figures/` existing visual asset | 展示误检、漏检或困难样例 | 复杂场景下的典型检测困难样例 |

## 篇幅较短时的精简方案

如果目标会议篇幅较紧，建议正文只保留 3 张图：

1. 图 1：训练过程曲线。
2. 图 4：检测结果示例。
3. 图 5：困难样例或误差分析。

PR 曲线和混淆矩阵可以作为附录材料或答辩补充材料保留。

## 使用边界

- 以上图像均来自已有 run 输出或已整理的历史可视化材料。
- 图题中不要写官方 test-dev/test-challenge 结果，因为当前没有官方服务器返回指标。
- 若正文使用失败案例图，需要在文字中说明它用于定性分析，不代表额外量化指标。

# 可视化材料索引

本文件整理当前项目已经生成、适合放入实验报告或答辩 PPT 的图表材料。所有关键图片已从 `runs/` 目录复制到 `experiments/figures/`，便于统一引用。

## 训练曲线

| 用途 | 图片 | 建议章节 |
| --- | --- | --- |
| Baseline 训练过程 | `experiments/figures/curves/baseline_results.png` | Baseline 实验 |
| ECA 训练过程 | `experiments/figures/curves/eca_results.png` | ECA 消融实验 |
| P2 训练过程 | `experiments/figures/curves/p2_results.png` | P2 消融实验 |

写作建议：

- 说明训练整体收敛趋势是否稳定。
- 对比 baseline、ECA、P2 的 mAP50 和 mAP50-95 曲线。
- 强调 P2 最终在小目标检测场景中取得当前最佳结果。

## PR 曲线

| 用途 | 图片 | 建议章节 |
| --- | --- | --- |
| Baseline PR 曲线 | `experiments/figures/curves/baseline_pr_curve.png` | 评价指标分析 |
| ECA PR 曲线 | `experiments/figures/curves/eca_pr_curve.png` | 消融对比 |
| P2 PR 曲线 | `experiments/figures/curves/p2_pr_curve.png` | 消融对比 |

写作建议：

- PR 曲线适合说明不同类别的检测难度。
- VisDrone 中 pedestrian、people、motor 等小目标类别通常更难检测。
- 可结合每类 AP 指标分析模型短板。

## 混淆矩阵

| 用途 | 图片 | 建议章节 |
| --- | --- | --- |
| Baseline 归一化混淆矩阵 | `experiments/figures/confusion/baseline_confusion_matrix_normalized.png` | 错误分析 |
| ECA 归一化混淆矩阵 | `experiments/figures/confusion/eca_confusion_matrix_normalized.png` | 错误分析 |
| P2 归一化混淆矩阵 | `experiments/figures/confusion/p2_confusion_matrix_normalized.png` | 错误分析 |

写作建议：

- 重点观察相近类别的混淆，例如 pedestrian 与 people、car 与 van。
- 结合航拍视角说明类别外观相似、尺度过小、遮挡密集等原因。
- P2 的优势可以从召回率提升、小目标漏检减少的角度解释。

## 定性检测样例

| 用途 | 图片 | 建议章节 |
| --- | --- | --- |
| P2 验证集预测样例 1 | `experiments/figures/qualitative/p2_val_batch0_pred.jpg` | 可视化结果 |
| P2 验证集预测样例 2 | `experiments/figures/qualitative/p2_val_batch1_pred.jpg` | 可视化结果 |
| P2 验证集预测样例 3 | `experiments/figures/qualitative/p2_val_batch2_pred.jpg` | 可视化结果 |

完整 P2 图片检测结果位于：

```text
runs/detect_image/p2_val_samples
```

当前该目录包含 548 张验证集检测结果，可用于挑选成功案例和失败案例。

精选案例分析位于：

```text
experiments/case_study.md
experiments/cases/p2_case_contact_sheet.jpg
```

## 报告中推荐放置的核心图

如果篇幅有限，建议至少放置以下 6 类材料：

1. `baseline_results.png`：说明 baseline 训练过程。
2. `p2_results.png`：说明最佳改进模型训练过程。
3. `baseline_pr_curve.png`：说明 baseline 各类别检测能力。
4. `p2_pr_curve.png`：展示 P2 改进后的类别表现。
5. `p2_confusion_matrix_normalized.png`：分析类别混淆问题。
6. `p2_val_batch0_pred.jpg` 或检测样例：展示系统实际检测效果。
7. `p2_case_contact_sheet.jpg`：展示 P2 的成功、密集和失败案例。

## 当前结论可写入报告

在三组实验中，YOLO11n-P2 是当前最佳模型。相比 YOLO11n baseline，P2 的 Best mAP50 从 0.32153 提升到 0.33013，Best mAP50-95 从 0.18238 提升到 0.19012。说明增加高分辨率小目标检测层能够改善 VisDrone 航拍小目标检测效果。

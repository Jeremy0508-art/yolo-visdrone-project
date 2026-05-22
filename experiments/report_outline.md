# 实验报告大纲：基于改进 YOLO 的无人机航拍小目标检测系统

## 1. 绪论

- 研究背景：无人机航拍场景中的小目标检测需求。
- 问题特点：目标尺度小、密集遮挡、视角变化大、背景复杂。
- 项目目标：基于 Ultralytics YOLO11n 构建可训练、可验证、可部署的检测系统。

## 2. 数据集与预处理

- 数据集：VisDrone2019-DET 图像目标检测任务。
- 数据规模：train 6471 张，val 548 张，test-dev 1580 张。
- 标注转换：将 VisDrone 原始格式转换为 YOLO 格式。
- 类别设置：使用 VisDrone DET 的 10 个目标类别。

## 3. Baseline 方法

- 基础模型：YOLO11n。
- 训练配置：输入尺寸、batch、epoch、优化器、数据增强参数。
- 评价指标：Precision、Recall、mAP50、mAP50-95。
- Baseline 结果：引用 `experiments/baseline/baseline_yolo11n_visdrone_summary.md`。

## 4. 改进方法

### 4.1 P2 小目标检测层

- 改进动机：提高浅层高分辨率特征对小目标的表达能力。
- 模型变化：增加 P2 检测头，与原 P3/P4/P5 检测头共同预测。
- 实验结论：P2 相比 baseline 提升 mAP50 和 mAP50-95，是主要有效改进。

### 4.2 P2 + CoordAttention

- 改进动机：在 P2 高分辨率检测头基础上进一步引入坐标注意力，增强模型对空间方向信息和关键区域的建模。
- 实现位置：在 P2 模型的 P4/P5 特征路径中加入 CoordAttention。
- 实验结论：相比 P2-only，Best mAP50 和 Best mAP50-95 有轻微正提升，是当前最佳权重。

## 5. 实验结果与消融分析

建议放置以下表格：

| Model | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |
| YOLO11n-P2-CoordAttention | 0.45375 | 0.34961 | 0.32709 | 0.18764 |

建议分析角度：

- P2 对小目标召回率的帮助。
- CoordAttention 带来的提升较小，说明注意力模块需要结合插入位置和训练策略继续验证。
- mAP50 与 mAP50-95 的差异，说明定位精度仍有提升空间。

## 6. 系统实现

- 工程结构：configs、scripts、tools、src、web 分层。
- 训练模块：统一配置驱动训练。
- 推理模块：图片检测、视频检测。
- Web 模块：Flask 上传图片/视频并展示结果。
- 默认部署权重：`runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt`。

## 7. 可视化与案例分析

建议放置：

- 训练曲线图：`runs/detect/*/results.png`。
- 混淆矩阵：`runs/detect/*/confusion_matrix.png`。
- 检测样例：`runs/detect_image/p2_val_samples`。
- 失败案例：密集目标、远距离行人、遮挡车辆等。

已整理的报告配图索引见：

```text
experiments/visual_assets.md
```

关键配图已集中复制到：

```text
experiments/figures/
```

精选成功/失败案例分析见：

```text
experiments/case_study.md
```

## 8. 总结与展望

- 已完成：数据处理、baseline、P2 消融、P2+CoordAttention 实验、推理脚本、Web 展示。
- 当前最佳模型：YOLO11n-P2-CoordAttention。
- 后续方向：更大输入尺寸、增强策略优化、易混淆类别分析、模型轻量化部署。

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

### 4.1 ECA 注意力机制

- 改进动机：增强通道特征选择能力。
- 实现位置：在 P3/P4/P5 特征路径中加入 ECA。
- 实验结论：当前设置下 ECA 单独加入未提升检测性能。

### 4.2 P2 小目标检测层

- 改进动机：提高浅层高分辨率特征对小目标的表达能力。
- 模型变化：增加 P2 检测头，与原 P3/P4/P5 检测头共同预测。
- 实验结论：P2 相比 baseline 提升 mAP50 和 mAP50-95，是当前最佳改进。

## 5. 实验结果与消融分析

建议放置以下表格：

| Model | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-ECA | 0.43047 | 0.32856 | 0.30236 | 0.17121 |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |

建议分析角度：

- P2 对小目标召回率的帮助。
- ECA 未提升的可能原因：训练策略、插入位置、轻量模型容量限制。
- mAP50 与 mAP50-95 的差异，说明定位精度仍有提升空间。

## 6. 系统实现

- 工程结构：configs、scripts、tools、src、web 分层。
- 训练模块：统一配置驱动训练。
- 推理模块：图片检测、视频检测。
- Web 模块：Flask 上传图片/视频并展示结果。
- 默认部署权重：`runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt`。

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

- 已完成：数据处理、baseline、ECA 消融、P2 消融、推理脚本、Web 展示。
- 当前最佳模型：YOLO11n-P2。
- 后续方向：P2+ECA 组合、更大输入尺寸、增强策略优化、模型轻量化部署。

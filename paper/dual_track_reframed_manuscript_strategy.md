# 双路线论文重构策略

状态：中文中刊与英文扩展稿共享的论文设计层文件。

## 共同核心

中文稿和英文稿不应是两个互相矛盾的项目。二者共享同一套实验和证据，但叙事重心不同：

| 路线 | 推荐定位 | 写法重点 |
| --- | --- | --- |
| 中文中刊 | 面向无人机航拍小目标检测的轻量 YOLO 高分辨率预测机制研究 | 问题清楚、实验扎实、工程可复现、结论克制 |
| 英文扩展 | Benefits, costs, and validity boundaries of high-resolution prediction for lightweight UAV object detection | 研究问题、边界分析、尺度诊断、跨数据集验证 |

## 中文中刊主线

中文稿更适合采用“方法分析 + 实验验证”的写法：

1. 提出无人机航拍小目标检测中轻量模型浅层细节不足的问题；
2. 设计高分辨率输入与 P2 浅层预测分支的轻量化检测框架；
3. 通过 CoordAttention、TOFC、SmallObjAug 作为消融，分析不同增强策略的贡献；
4. 用 VisDrone 和 UAVDT 结果验证方法收益和适用边界；
5. 明确大模型 YOLO11s 仍有绝对精度优势，本文方法定位为轻量化折中。

中文稿可以比英文稿更强调工程实现和可复现流程，但不能写成工作进展报告。

## 英文扩展主线

英文稿应避免“又一个改 YOLO 模块”的写法，更适合强调研究问题：

1. How much does input resolution contribute?
2. Does P2 still help after resolution is matched?
3. Are attention and calibration modules consistently beneficial?
4. What are the computational costs?
5. Does the trend transfer to UAVDT?

如果 UAVDT 结果支持 P2，英文稿可以加强方法贡献。  
如果 UAVDT 结果不支持 P2，英文稿应转为 validity-boundary analysis。

## 旧稿内容如何继承

| 旧材料 | 新用途 |
| --- | --- |
| 中文 manuscript_submission_candidate | 保留实验数据和图表，重写叙事 |
| IEEE main_draft | 作为英文重构初稿，继续接入 UAVDT |
| PROJECT_ROADMAP | 保留路线管理，但不作为论文正文 |
| 表格 CSV | 作为所有数值唯一来源 |
| speed_results/model_complexity | 支撑轻量化折中 |
| scale diagnostics | 支撑小目标机制分析 |
| UAVDT 队列 | 支撑跨数据集边界 |

## 不再采用的写法

- “本文提出 P2+CA+960 的改进模型并全面提升检测性能。”
- “TOFC 是最终小目标增强模块。”
- “本方法优于 YOLO11s。”
- “UAVDT 结果显示……”但结果还未完整同步审计。
- “论文正在等待实验完成”这类进度汇报式句子进入正式稿。

## 等 UAVDT 完成后的决策树

| UAVDT 结果 | 中文稿策略 | 英文稿策略 |
| --- | --- | --- |
| P2 优于 YOLO11n 且接近/优于 YOLOv8n | 主推高分辨率 P2 轻量化方法 | 写成方法型论文 |
| P2 小目标指标好但 aggregate 不好 | 强调小目标检测和折中 | 写成机制分析论文 |
| P2 弱于 YOLO11n | 降低方法主张，转为边界分析 | 明确 dataset-dependent behavior |
| YOLO11s 明显最强 | 保留为大模型上界 | 不与 nano 模型混作同类竞品 |

## 当前完成标准

在 UAVDT 完成前，论文设计层大改应达到：

- 主线已从“模块组合”改为“高分辨率预测机制研究”；
- 证据矩阵已建立；
- 英文草稿已按新主线重写；
- 中文/英文双路线统一策略已建立；
- 后续 UAVDT 结果有明确接入规则。

# 导师汇报简版

本文档用于向导师简要说明项目从 YOLO 工程实现推进到《计算机工程与应用》投稿准备的阶段性工作。所有论文数值均来自真实训练日志、验证结果或 `paper/tables/` 汇总文件。

## 1. 研究目标

项目围绕 VisDrone2019-DET 无人机航拍目标检测任务，重点解决航拍图像中目标尺度小、目标分布密集、遮挡频繁、类别外观相似等问题。当前论文目标期刊为《计算机工程与应用》，计划从工程项目整理升级为中文期刊论文稿件。

## 2. 已完成工作

### 2.1 工程与数据闭环

- 完成 VisDrone2019-DET 到 YOLO 格式的数据转换与检查。
- 保留训练、验证、图片推理、视频推理、Web 演示和测速脚本。
- 建立 `paper/` 目录，集中管理论文稿件、表格、图件、复现实验命令和证据审计。

### 2.2 主线模型实验

已完成 100 epoch 的主线实验包括：

- YOLO11n baseline。
- YOLO11n-P2。
- YOLO11n-P2-CoordAttention。
- YOLO11n-P2-CoordAttention-960。
- YOLO11n-P2-CoordAttention-SmallObjAug。

当前已完成实验中，YOLO11n-P2-CoordAttention-960 在 VisDrone 验证集上取得 best mAP50 `0.41996`、best mAP50-95 `0.25174`。与 YOLO11n baseline 相比，mAP50 和 mAP50-95 分别提升 `0.09843` 和 `0.06936`。

### 2.3 外部参考基线

已完成 YOLOv8n-640 与 YOLO11s-640 的同数据集训练，用于辅助分析不同 YOLO 版本和模型容量的影响。当前不会把 YOLOv8n baseline 与 YOLO11n-P2-CA-960 直接作为单因素公平消融，因为二者基础架构和输入设置不同。

### 2.4 小目标专项分析

已基于 YOLO 格式标注完成目标尺度统计：

- 训练集 small 目标占比为 `60.49%`。
- 验证集 small 目标占比为 `68.59%`。

已基于预测结果完成尺度分组匹配分析。在 `conf=0.25`、`IoU=0.5` 的验证集匹配口径下，YOLO11n-P2-CoordAttention-960 的 small 目标召回率为 `0.455089`，YOLO11n baseline 为 `0.307681`。该结果用于说明不同尺度目标的匹配情况，不等同于官方 AP。

### 2.5 论文材料整理

已经生成或整理：

- LaTeX 投稿候选稿：`paper/manuscript_submission_candidate.tex`
- PDF 预览：`paper/manuscript_submission_candidate.pdf`
- 投稿主控计划：`paper/CEA_JOURNAL_MASTER_PLAN.md`
- 期刊差距分析：`paper/CEA_REVIEW_GAP_ANALYSIS.md`
- 期刊长文提纲：`paper/CEA_JOURNAL_MANUSCRIPT_OUTLINE.md`
- 证据审计：`paper/evidence_audit.md`
- 投稿前检查清单：`paper/submission_checklist.md`
- 精度-速度-参数量折中图：`paper/figures/tradeoff/accuracy_speed_tradeoff.png`

## 3. 当前补跑实验

为增强期刊投稿说服力，已经在租用服务器上排队补跑公平对照实验：

1. YOLO11n-960。
2. YOLO11n-P2-960。
3. YOLOv8n-960。
4. YOLO11s-960。
5. YOLOv5n-640。

当前服务器正在运行 YOLO11n-960，后续实验由队列脚本顺序执行。未完成 100 epoch 的实验结果不会进入论文主表。

## 4. 当前论文主张

目前不建议使用绝对化性能表述。更稳妥的主张是：

> 面向 VisDrone 无人机航拍小目标检测，本文构建一种融合 P2 高分辨率检测分支、CoordAttention 与 960 输入策略的轻量化 YOLO11n 改进方法，并通过公平分辨率对照、主流 YOLO 基线、消融实验、尺度分组分析和速度复杂度统计，系统分析不同设计对检测精度与推理效率的影响。

这个主张可以根据服务器补跑结果继续调整。

## 5. 主要风险与应对

| 风险 | 应对 |
| --- | --- |
| YOLO11n-960 接近最终模型 | 将论文主张调整为高分辨率输入贡献为主，P2/CA 为结构补充 |
| YOLO11s-960 超过最终模型 | 强调轻量化参数效率，并把 YOLO11s-960 作为容量上限讨论 |
| SmallObjAug 表现不如结构改进 | 作为负向消融，说明简单增强策略不一定有效 |
| 官方 VisDrone test-dev 平台不可用 | 只报告验证集结果，不写入未经官方返回的 AP |
| 论文创新性不足 | 强化公平实验、小目标尺度分析、速度复杂度折中和失败案例归因 |

## 6. 下一步计划

1. 等服务器完成公平对照实验后，同步完整日志、结果和权重元信息。
2. 重新生成 `paper/tables/` 中的结果表。
3. 补测新增模型速度与复杂度。
4. 根据真实结果重写期刊长文实验分析。
5. 扩充相关工作与参考文献，并按《计算机工程与应用》风格完成投稿前排版检查。

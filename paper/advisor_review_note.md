# 给导师审阅的论文材料说明

本文档用于随 `paper/advisor_review_package.zip` 一起发送给导师，帮助导师快速判断当前 YOLO VisDrone 项目是否具备继续向《计算机工程与应用》投稿推进的基础。本文档只整理已有真实实验和审计结果，不新增实验数值，也不替代论文正文。

## 一句话概括

本项目围绕 VisDrone2019-DET 无人机航拍小目标检测任务，基于 Ultralytics YOLO11n 构建了 P2 高分辨率检测分支、CoordAttention 注意力模块、960 输入分辨率和小目标友好数据增强的系统性实验，并补充了 YOLOv5n、YOLOv8n、YOLO11n、YOLO11s 等公平对比结果。当前结论应表述为“高分辨率输入与 P2 分支对小目标场景具有稳定价值，CoordAttention 和小目标增强的收益存在条件性”，不能表述为“本文方法全面优于所有模型”。

## 建议导师优先看的材料

1. `paper/manuscript_submission_candidate.pdf`
   当前论文 PDF 预览，包含方法、实验、消融、可视化、失败案例和结论。

2. `paper/advisor_progress_brief.md`
   面向导师的简版进度说明，适合先快速了解研究定位、实验完成情况和主要结论。

3. `paper/tables/main_comparison_for_paper.csv`
   主结果表。所有关键数值均应以该表和对应 `runs/` 结果为准。

4. `paper/evidence_audit.md` 与 `paper/manuscript_number_trace_audit.md`
   用于核对论文中的数值来源，避免论文中出现没有日志或表格支撑的指标。

5. `paper/submission_audit_dashboard.md`
   当前投稿材料审计总览，可快速看到哪些本地材料已经 ready，哪些仍需人工确认。

## 当前最重要的实验结论边界

### 1. 大模型上界

`YOLO11s baseline 960` 在验证集上取得当前最高精度：

- best mAP50：0.48901
- best mAP50-95：0.29812
- FPS：62.13
- 参数量：9.432M

这说明在 VisDrone 场景中，模型容量仍然是提升检测性能的重要因素。论文中应把它作为容量更大的参考上界，而不是与 nano 级方法做单一变量消融。

### 2. nano 级轻量模型折中点

`YOLO11n-P2-960` 是当前 nano 级模型中更适合作为轻量改进主线的结果：

- best mAP50：0.42361
- best mAP50-95：0.25552
- FPS：55.68
- 参数量：2.894M

与 `YOLO11n baseline 960` 相比，`YOLO11n-P2-960` 的 best mAP50 从 0.42136 提升到 0.42361，best mAP50-95 从 0.25067 提升到 0.25552，但速度从 61.09 FPS 降至 55.68 FPS。论文中应强调“精度-速度折中”，不要只写精度提升。

### 3. CoordAttention 的真实表现

`YOLO11n-P2-CoordAttention` 在 640 输入下相对 P2 有小幅提升：

- P2：mAP50 0.33013，mAP50-95 0.19012
- P2-CA：mAP50 0.33073，mAP50-95 0.19044

但在 960 输入下，`YOLO11n-P2-CoordAttention-960` 未超过 `YOLO11n-P2-960`：

- P2-960：mAP50 0.42361，mAP50-95 0.25552
- P2-CA-960：mAP50 0.41996，mAP50-95 0.25174

因此论文中应把 CoordAttention 写成“辅助设计与边界结果”，不宜作为主要性能提升来源。

### 4. 小目标增强的真实表现

`YOLO11n-P2-CoordAttention-SmallObjAug` 相对 YOLO11n baseline 有提升，但低于 P2 与 P2-CA：

- SmallObjAug：mAP50 0.32780，mAP50-95 0.18699
- YOLO11n baseline：mAP50 0.32153，mAP50-95 0.18238
- P2-CA：mAP50 0.33073，mAP50-95 0.19044

因此小目标增强可以作为“策略探索和负向/边界消融”讨论，不能写成最终最优方案。

## 当前论文可主张的创新点

1. 面向无人机航拍小目标检测，系统评估 YOLO11n 的 P2 高分辨率检测分支、注意力增强、输入分辨率和小目标增强策略。

2. 在统一 VisDrone 数据处理、训练配置和验证流程下，补充 YOLOv5n、YOLOv8n、YOLO11n、YOLO11s 以及 P2 系列变体的公平对比。

3. 不是只报告 mAP，而是同时整理参数量、GFLOPs、模型大小、单图推理速度、尺度分组匹配、类别级结果、可视化结果和失败案例。

4. 对负向或条件性结果进行如实讨论，尤其是 CoordAttention 与小目标增强没有在所有设置下带来稳定提升这一点。

## 需要导师重点把关的问题

1. 论文题目是否应突出“高分辨率 P2 分支与轻量化折中”，而不是突出 CoordAttention 或小目标增强。

2. 结论中是否接受“YOLO11s-960 精度最高，YOLO11n-P2-960 是 nano 级折中点”的写法。

3. 是否需要进一步补充更强模型或其他公开方法作为参考对比；如果补充，必须重新跑实验或引用有明确来源的可比结果。

4. 是否继续尝试 VisDrone test-dev 官方评测。当前论文只能报告验证集结果，不能写官方 test-dev AP。

5. 是否需要迁移到《计算机工程与应用》官方 Word/LaTeX 模板。当前本地 PDF 是投稿候选稿，不等同于已满足官方上传格式。

## 不建议在论文中使用的表述

- 不建议写“本文方法全面优于 YOLOv8n/YOLO11s”。
- 不建议拿 `YOLOv8n baseline 640` 与 `YOLO11n-P2-CA-960` 直接作为公平结论。
- 不建议把 `YOLO11s-960` 的结果解释为本文轻量方法的改进效果。
- 不建议把官方 test-dev 作为已完成结果描述。
- 不建议把未确认的期刊模板、费用、字数或投稿系统要求写成确定事实。

## 当前可交付状态

本地论文材料、实验表格、图表、审计报告和导师审阅包已经整理完成；剩余关键步骤主要是人工项：导师确认论文主线、确认作者与基金信息、下载并核对期刊官方模板、逐页检查最终 PDF、确认 GitHub 页面渲染，以及在官方 VisDrone 平台可用时再提交 test-dev。

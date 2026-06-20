# IEEE Transactions 路线导师汇报简版

## 当前定位

项目已从《计算机工程与应用》中文期刊路线暂时切换到 IEEE Transactions 英文期刊准备路线。当前更合理的论文定位不是直接宣称某个模块全面超过所有模型，而是围绕无人机交通场景中的轻量小目标检测，系统分析高分辨率输入、P2 浅层检测分支、注意力/特征校准模块对精度、速度、复杂度和尺度分组指标的影响。

建议当前题目方向：

> High-Resolution Lightweight YOLO for Small Object Detection in UAV Traffic Scenes

TOFC 不建议现在放进题目作为“小目标增强主方法”，因为它虽然提升了整体 mAP，但当前小目标诊断指标不如 YOLO11n-P2-960。

## 已完成的主要工作

1. 完成 VisDrone2019-DET 上的 YOLO11n 系列、公平 960 输入对比、YOLOv5n/YOLOv8n/YOLO11s 参考模型对比。
2. 新增并完成 YOLO11n-P2-TOFC-960 训练，训练轮数为 100 epochs，结果已同步到本地证据链。
3. 补充了主结果表、复杂度表、速度测试表、尺度分组 recall/precision、local scale-bin AP 诊断表。
4. 建立 IEEE 投稿准备材料目录 `paper/ieee_trans/`，包含英文段落草稿、表格草稿、证据映射、审计报告和投稿准备清单。
5. 建立自动审计脚本，确保论文中的数字来自真实 CSV、日志或运行结果，不手动编造数值。

## 当前关键实验结果

VisDrone 验证集主要结果如下，数值来自 `paper/tables/main_comparison_for_paper.csv`。

| 模型 | 输入 | Params/M | mAP50 | mAP50-95 | 说明 |
| --- | ---: | ---: | ---: | ---: | --- |
| YOLO11n-960 | 960 | 2.592 | 0.42136 | 0.25067 | 分辨率公平 baseline |
| YOLO11n-P2-960 | 960 | 2.894 | 0.42361 | 0.25552 | 小目标诊断更强的轻量方案 |
| YOLO11n-P2-CA-960 | 960 | 2.904 | 0.41996 | 0.25174 | 注意力消融，整体指标未超过 P2 |
| YOLO11n-P2-TOFC-960 | 960 | 2.896 | 0.42837 | 0.26054 | 当前 nano 级整体 mAP 最好 |
| YOLO11s-960 | 960 | 9.432 | 0.48901 | 0.29812 | 大容量参考上界 |

当前结论需要谨慎：

- TOFC 的整体 mAP50 和 mAP50-95 优于 YOLO11n-P2-960。
- 但 TOFC 的小目标 recall 为 0.430828，低于 YOLO11n-P2-960 的 0.450124。
- TOFC 的 local small-bin AP50 为 0.229853，低于 YOLO11n-P2-960 的 0.247659。
- 因此 TOFC 不能写成“小目标检测全面增强模块”，更适合写成整体精度校准候选或消融结果。
- YOLO11s-960 仍然显著强于 nano 模型，论文必须强调轻量化折中，而不是绝对 SOTA。

## 当前有没有论文初版

有材料级初版，但还不是正式 IEEE 投稿稿。

可以给导师看的文件：

1. `paper/ieee_advisor_progress_brief.md`：当前这份导师汇报简版。
2. `paper/ieee_trans/section_draft_pack.md`：英文论文各章节的 evidence-bounded 草稿，可视为 IEEE 英文稿雏形。
3. `paper/ieee_trans/tables/visdrone_main_results.tex`：IEEE 主结果表草稿。
4. `paper/ieee_trans/tables/speed_complexity.tex`：速度与复杂度表草稿。
5. `paper/ieee_submission_dashboard.md`：当前投稿准备状态总览。
6. `paper/IEEE_TRANS_SUBMISSION_PLAN.md`：完整 IEEE 路线计划。

不建议现在把它称为“可投稿初稿”，因为 `paper/ieee_trans/main.tex` 还没有生成，UAVDT 第二数据集实验也未完成。

## 当前最大短板

IEEE Transactions 级别目前最大的短板是泛化证据不足。当前结果主要来自 VisDrone 验证集，UAVDT 或其他第二数据集尚未完成转换与训练，因此还不能宣称方法具有跨数据集泛化能力。

下一步优先级：

1. 准备 UAVDT 原始数据并完成 YOLO 格式转换。
2. 在 UAVDT 上跑 YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960。
3. 如果资源允许，再决定是否补 TOFC-UAVDT 或多 seed 稳定性实验。
4. 根据第二数据集结果决定最终主方法和英文论文标题。

## 建议给导师的汇报口径

可以这样说：

> 目前已经完成 VisDrone 上的系统实验和 IEEE 投稿准备框架。结果显示，960 输入和 P2 高分辨率分支对轻量 YOLO 的小目标诊断有较明确作用；新尝试的 TOFC 在整体 mAP 上超过 P2-960，但小目标尺度诊断不如 P2-960，因此暂不把 TOFC 作为小目标增强主结论，而作为整体精度校准消融来处理。当前距离 IEEE Transactions 投稿还缺第二数据集 UAVDT 验证和最终英文稿整合。


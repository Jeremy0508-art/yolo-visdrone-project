# IEEE Transactions 路线导师汇报简版

更新时间：2026-06-21

## 当前定位

项目目前保留中文期刊和英文 IEEE Transactions 两条路线。中文路线没有放弃；英文路线单独面向更高质量的投稿目标推进。

英文稿已经不再按“静态 P2 一定有效”来包装，而是根据 VisDrone 与 UAVDT 的真实结果重新组织主线：

> 轻量 YOLO 在无人机航拍小目标检测中需要浅层高分辨率特征，但静态 P2 分支是否稳定有效、计算代价如何、能否跨数据集成立，需要用完整实验验证。

因此，当前英文路线已经从“整理现有 P2 结果”转向“基于 VisDrone 和 UAVDT 证据重新设计自适应 P2 方法并验证”。

## 已完成工作

1. 完成 VisDrone2019-DET 上 YOLO11n、YOLO11n-P2、YOLO11n-P2-CA、YOLO11n-P2-TOFC、YOLOv5n、YOLOv8n、YOLO11s 等模型的主结果、速度、复杂度和尺度诊断整理。
2. 完成 UAVDT 数据集准备、转换和四组公平对照实验同步：YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960。
3. 生成 IEEE 英文工作区 `paper/ieee_trans/`，包括 draft PDF、表格、图表计划、证据映射、审计脚本和投稿前检查清单。
4. 根据 UAVDT 结果确认：静态 P2 在 VisDrone 上有小目标诊断收益，但在 UAVDT 上不具备稳定迁移优势。
5. 新设计并实现了 `ScaleAwareP2Gate` 自适应 P2 候选模块，并已在服务器启动 VisDrone 与 UAVDT 队列实验。

## 关键实验结论

VisDrone 上，YOLO11n-P2-960 相比 YOLO11n-960 有小幅提升：

| 模型 | 输入 | Params/M | VisDrone mAP50 | VisDrone mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n-960 | 960 | 2.592 | 0.42136 | 0.25067 |
| YOLO11n-P2-960 | 960 | 2.894 | 0.42361 | 0.25552 |
| YOLO11n-P2-CA-960 | 960 | 2.904 | 0.41996 | 0.25174 |
| YOLO11n-P2-TOFC-960 | 960 | 2.896 | 0.42837 | 0.26054 |
| YOLO11s-960 | 960 | 9.432 | 0.48901 | 0.29812 |

UAVDT 上，静态 P2 没有保持优势：

| 模型 | UAVDT mAP50 | UAVDT mAP50-95 |
| --- | ---: | ---: |
| YOLO11n-960 | 0.88444 | 0.59081 |
| YOLO11n-P2-960 | 0.83711 | 0.53905 |
| YOLOv8n-960 | 0.88983 | 0.59487 |
| YOLO11s-960 | 0.89756 | 0.60819 |

这说明当前论文不能写成“P2 普遍提升”或“轻量模型超过更大模型”。更合理的主线是：高分辨率预测对 VisDrone 小目标诊断有帮助，但存在计算代价和数据集适用边界，因此需要设计自适应高分辨率机制。

## 新方法进展

当前新方法候选为 `ScaleAwareP2Gate`：

- 插入位置：P2 高分辨率特征融合之后；
- 设计思想：不固定增强 P2，而是通过局部上下文、通道门控、空间门控和有界残差增益，让 P2 特征自适应调制；
- 初始化方式：增益参数初始化为 0，因此初始输出等同于普通 P2，降低训练不稳定风险；
- 当前状态：代码、模型 YAML、训练配置和结构图已完成；服务器实验正在运行。

截至最近一次状态检查：

- `yolo11n_p2_scalegate_960_visdrone`：4/100 epoch，训练中；
- `yolo11n_p2_scalegate_960_uavdt`：排队中；
- 早期 epoch 结果只作为训练进度，不进入论文结论。

## 当前可给导师查看的材料

建议优先查看：

1. `paper/ieee_trans/main_draft.pdf`：当前英文 evidence-bounded draft；
2. `paper/ieee_trans/scalegate_method_section_draft.md`：ScaleAwareP2Gate 方法小节草稿；
3. `paper/figures/method/scalegate_schematic.png`：ScaleGate 模块结构图；
4. `paper/ieee_submission_dashboard.md`：IEEE 路线总体状态；
5. `paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md`：从静态 P2 转向自适应 P2 的方法重设计计划；
6. `paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md`：ScaleGate 完成后如何同步、测速、做尺度诊断和写入论文的协议。

## 下一步计划

1. 等待 ScaleGate 的 VisDrone 和 UAVDT 两个完整 100 epoch 实验完成。
2. 同步完整运行目录，并只把 100 epoch 完成结果纳入论文表格。
3. 补测 ScaleGate 的速度、复杂度、尺度召回/精度和本地 scale-bin AP。
4. 根据真实结果决定最终路线：
   - 如果 ScaleGate 同时改善 VisDrone 与 UAVDT，转为自适应 P2 方法论文；
   - 如果只改善 VisDrone，不改善 UAVDT，写成方法加适用边界；
   - 如果 ScaleGate 不改善，则继续第二轮方法设计，不强行包装结果。
5. 在最终路线确定后，再重写摘要、贡献点、结论和投稿版 `main.tex`。

# 《计算机工程与应用》论文章节证据映射表

本文档用于指导期刊长文重写。它把每个论文章节允许提出的核心论点、必须引用的证据来源、当前状态和写作边界提前固定下来，避免在服务器公平实验完成前写出超出证据范围的结论。

## 1. 使用规则

- 正文每个数值必须能追溯到 `paper/tables/`、`runs/`、`runs/logs/`、脚本输出或官方评测返回结果。
- 当前未完成的服务器公平实验只可作为“待同步的实验门槛”记录，不进入论文结论。
- 若某一节缺少证据，优先保留写作框架，等完整结果同步后再填入具体结论。
- 如果证据与预期相反，按真实结果改写论点。

## 2. 章节级证据映射

| 目标章节 | 可写核心论点 | 必须引用的证据 | 当前状态 | 写作边界 |
| --- | --- | --- | --- | --- |
| 摘要 | 说明无人机小目标检测问题、本文方法组成、最终真实结果和速度/复杂度折中 | `main_comparison_for_paper.csv`, `speed_results.csv`, `model_complexity.csv` | 部分可写 | 最终摘要等公平实验同步后再定稿 |
| 引言 | VisDrone 场景存在目标小、密集、遮挡、类别相似等挑战；轻量 YOLO 需要兼顾精度与速度 | `object_scale_distribution.csv`, VisDrone 数据集说明, 相关文献 | 可写 | 不提前宣称主方法全面最优 |
| 相关工作 | 梳理 YOLO、无人机检测、小目标检测、多尺度融合、注意力机制和轻量化检测 | `reference_verification_matrix.md`, `references.md` | 可写 | 未核验文献不进入正式引用 |
| 方法总体结构 | 本方法以 YOLO11n 为基础，引入 P2、CoordAttention 和 960 输入策略 | `configs/`, `paper/figures/method/hrpca_yolo11n_overview.png`, 模型 YAML | 可写 | 960 输入是训练/推理策略，不写成网络结构模块 |
| P2 分支 | P2 分支用于增强浅层空间细节，对小目标更友好 | `ablation_results.csv`, `main_comparison_for_paper.csv` | 可写 | P2 在 960 下的独立贡献需等待 YOLO11n-960 与 YOLO11n-P2-960 |
| CoordAttention | 坐标注意力用于补充位置信息表达 | `ablation_results.csv`, `main_comparison_for_paper.csv` | 可写 | 若 CA 增益有限，应写为辅助模块 |
| 960 输入策略 | 高输入分辨率提升小目标有效像素，但增加推理成本 | `main_comparison_for_paper.csv`, `speed_results.csv`, `model_complexity.csv` | 部分可写 | 分辨率贡献需等待 YOLO11n-960 公平结果 |
| 小目标增强策略 | SmallObjAug 是数据层面消融，结果应按真实表现解释 | `ablation_results.csv`, 训练配置 YAML | 可写 | 不把负向或有限增益写成成功创新 |
| 实验设置 | 数据集、训练环境、超参数、评价指标、速度协议和复现命令 | `commands.md`, `config_inventory_audit.md`, `repro_commands_audit.md`, `args.yaml` | 可写 | 无法确认的参数只写“按日志记录”或留在配置说明中 |
| 主线消融结果 | 比较 YOLO11n、P2、P2-CA、P2-CA-960、SmallObjAug | `main_comparison_for_paper.csv`, `ablation_results.csv` | 可写 | 不与外部 YOLO 版本混作单因素消融 |
| 分辨率公平对照 | 判断 960 输入和结构改进各自贡献 | 服务器完整 100 epoch 结果, `main_comparison_for_paper.csv` | 等待服务器 | 未完成前不能写结论 |
| 主流 YOLO 对照 | 比较 YOLOv5n、YOLOv8n、YOLO11n、YOLO11s 等轻量模型 | 完整 run, `main_comparison_for_paper.csv`, `model_complexity.csv` | 部分等待 | 区分同分辨率、跨版本和容量参考 |
| 小目标尺度分析 | VisDrone 中 small 目标占比高，主方法在尺度分组匹配中改善小目标召回 | `object_scale_distribution.csv`, `scale_group_results.csv`, `paper/figures/scale_analysis/` | 可写 | scale-group 是阈值匹配分析，不等同官方 AP |
| 类别级分析 | 分析行人、非机动车、车辆等类别的检测差异和混淆风险 | `per_class_results.csv`, 混淆矩阵图 | 可写 | 只讨论表中真实存在的类别和数值 |
| 速度复杂度分析 | 从参数量、GFLOPs、权重大小、延迟、FPS 分析部署折中 | `speed_results.csv`, `model_complexity.csv`, `accuracy_speed_tradeoff.csv` | 部分可写 | 新模型未测速度前不绘制或估计 |
| 可视化分析 | 展示密集目标、小目标、遮挡和失败案例 | `paper/figures/qualitative/`, `paper/figures/failure_cases/`, `figure_index.md` | 可写 | 图注不能含未验证指标 |
| 讨论 | 解释分辨率、结构、容量、速度和失败案例之间的关系 | 所有审计后的表格与图 | 等待最终结果 | 讨论必须反映负向结果和边界 |
| 结论 | 总结已证实贡献、局限和后续工作 | 最终审计后的正文表格 | 等待最终结果 | 结论最后写，不使用绝对化表述 |

## 3. 关键论点与证据要求

| 论点 | 可以成立的证据条件 | 若证据不足时的写法 |
| --- | --- | --- |
| P2 对小目标有效 | YOLO11n-P2 优于 YOLO11n；或 YOLO11n-P2-960 优于 YOLO11n-960 | “P2 在当前主线消融中带来增益，960 下独立贡献需由公平对照确认” |
| CoordAttention 有贡献 | P2-CA 优于 P2；或 P2-CA-960 优于 P2-960 | “CoordAttention 作为轻量位置增强模块，在当前实验中表现为辅助增益” |
| 960 输入是重要因素 | YOLO11n-960 明显优于 YOLO11n-640 | “高分辨率输入可能是关键因素，待公平实验完成后定量讨论” |
| 本方法优于 YOLOv8n | 同协议 YOLOv8n-960 完成且低于主方法 | “YOLOv8n 作为外部基线单独讨论，不做跨协议结论” |
| 本方法具备轻量化优势 | 精度接近或优于更大模型，同时参数、GFLOPs、速度有优势 | “本文关注轻量模型的精度-速度折中，不宣称绝对精度最优” |
| SmallObjAug 有效 | SmallObjAug 结果优于对应未增强模型 | “SmallObjAug 作为数据增强边界消融，如实分析其收益或不足” |

## 4. 结果回来后的正文更新顺序

1. 同步完整服务器 run，并更新 `paper/tables/`。
2. 重新生成速度、复杂度、类别级、尺度分组和折中图中受影响的材料。
3. 运行 `python tools/run_paper_audits.py`。
4. 先改实验结果节，再改讨论节。
5. 最后改摘要、贡献列表、题名和结论。
6. 编译 PDF 并检查图表位置。

## 5. 不能提前写入正文的内容

- 未完成公平实验的具体精度、速度或复杂度。
- 官方 VisDrone test-dev AP。
- 没有类别级表格支撑的“所有类别均提升”。
- 没有速度和复杂度表支撑的“无额外计算成本”。
- 没有同协议比较支撑的“优于主流 YOLO 方法”。


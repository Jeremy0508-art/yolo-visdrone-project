# IEEE Transactions 投稿升级计划

## 目标定位

本计划用于把当前 YOLO-VisDrone 项目从“中文期刊/会议投稿准备”切换到“IEEE Transactions 英文期刊投稿准备”。《计算机工程与应用》相关 Word 迁移、中文模板和 CEA 审计材料暂时搁置，后续不再作为主线推进；已有实验、图表、日志和可复现材料仍作为英文期刊工作的基础证据库。

需要特别说明：IEEE Transactions 录用结果受选题竞争、创新强度、实验完整性、英文写作质量和审稿意见影响，无法承诺必然录用。当前可控目标是把项目提升到具备认真投稿 IEEE Transactions 的工程和论文状态。

投稿准备必须遵守以下边界：

- 所有实验数值必须来自真实运行日志、`runs/` 目录、CSV 表格、验证输出或官方评测结果。
- 不编造未完成实验，不把推测写成结果。
- 不重复投稿；若中文期刊路线恢复，需避免与 IEEE 英文稿形成一稿多投或重复发表风险。
- IEEE 英文稿不是中文稿直译，而是围绕英文期刊审稿标准重新组织贡献、方法、实验和讨论。

官方准备入口：

- IEEE Article Templates: `https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/tools-for-ieee-authors/ieee-article-templates/`
- IEEE Template Selector: `https://template-selector.ieee.org/`
- IEEE submission and peer review policies: `https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/`

## 候选目标期刊

IEEE Transactions 级别期刊必须先确定目标刊物，因为不同刊物关注点不同。当前项目围绕无人机航拍、小目标检测、轻量 YOLO 改进和交通/城市监控场景，初步候选如下。

| 候选期刊 | 匹配点 | 主要风险 | 推荐程度 |
| --- | --- | --- | --- |
| IEEE Transactions on Intelligent Transportation Systems | VisDrone 场景包含交通道路、车辆、行人、非机动车，适合写无人机交通感知 | 需要突出智能交通应用价值，不能只写通用检测结构 | 高 |
| IEEE Transactions on Geoscience and Remote Sensing | 无人机航拍、低空遥感、小目标检测与遥感视觉相关 | 需要更强遥感数据集和遥感领域对比，当前 VisDrone 单数据集不足 | 中 |
| IEEE Transactions on Circuits and Systems for Video Technology | 关注视觉算法、检测网络、轻量模型和视频/图像处理 | 对方法创新要求高，需要更强结构创新和更广泛对比 | 中 |
| IEEE Transactions on Aerospace and Electronic Systems | UAV sensing、aerial surveillance、航空电子感知任务相关 | 需要更强系统应用背景，单纯 YOLO 改进可能偏弱 | 中低 |
| IEEE Transactions on Multimedia | 视觉理解与多媒体分析相关 | 竞争极强，需要显著算法创新和多数据集 SOTA 对比 | 低 |

阶段结论：优先分析 `IEEE Transactions on Intelligent Transportation Systems` 和 `IEEE Transactions on Geoscience and Remote Sensing`。如果导师没有指定具体刊物，建议先按 T-ITS 的交通感知叙事准备，同时保留 TGRS 的遥感叙事备选。

## 当前项目基础

当前项目已经具备英文期刊工作的基础证据，但还达不到 IEEE Transactions 的投稿强度。

| 类别 | 当前状态 |
| --- | --- |
| 数据集 | VisDrone2019-DET 已转换为 YOLO 格式，训练/验证/test-dev 目录完整 |
| 主线模型 | YOLO11n、YOLO11n-P2、YOLO11n-P2-CA、YOLO11n-P2-CA-960、SmallObjAug 已完成 |
| 公平对比 | YOLOv5n、YOLOv8n、YOLOv8n-960、YOLO11n-960、YOLO11n-P2-960、YOLO11s、YOLO11s-960 已完成并同步 |
| 结果证据 | `runs/`、`runs/logs/`、`paper/tables/`、审计报告已建立证据链 |
| 可视化 | 训练曲线、检测示例、失败案例、尺度分布和尺度召回图已整理 |
| 中文稿 | CEA 方向 Word/LaTeX/PDF/审计材料已形成，但现在暂停 |
| 主要风险 | 方法创新偏弱；单数据集不足；英语论文结构尚未建立；SOTA 对比不足 |

当前关键结果必须如实解释：

| 模型 | 输入 | Params/M | Best mAP50 | Best mAP50-95 | 论文含义 |
| --- | ---: | ---: | ---: | ---: | --- |
| YOLO11n | 640 | 2.592 | 0.32153 | 0.18238 | 轻量基线 |
| YOLO11n-960 | 960 | 2.592 | 0.42136 | 0.25067 | 高分辨率输入贡献显著 |
| YOLO11n-P2-960 | 960 | 2.894 | 0.42361 | 0.25552 | nano 级模型中较好的精度-速度折中 |
| YOLO11n-P2-CA-960 | 960 | 2.904 | 0.41996 | 0.25174 | 当前 960 设置下 CoordAttention 未带来进一步提升 |
| YOLOv8n-960 | 960 | 3.013 | 0.42016 | 0.25121 | 外部轻量参考基线 |
| YOLO11s-960 | 960 | 9.432 | 0.48901 | 0.29812 | 更大容量模型精度明显更高 |

因此，英文稿不能宣称当前方法全面优于更大模型；更合理的主张是：在 nano 级轻量模型中，通过高分辨率输入与 P2 分支实现更好的小目标定位和精度-速度-复杂度折中。

## 与 IEEE Transactions 的差距

| 差距 | 当前风险 | 升级动作 |
| --- | --- | --- |
| 创新点不足 | P2、CoordAttention 和 960 输入都容易被认为是已有模块组合 | 需要重新设计或强化一个可命名、可解释、可消融的方法贡献 |
| 数据集单一 | 只用 VisDrone val 难以证明泛化能力 | 至少补 UAVDT；若可行，再补 AI-TOD、TinyPerson 或其他 UAV/remote-sensing 小目标数据 |
| SOTA 对比不足 | 目前主要是 YOLO 系列内部和轻量 baseline | 增加近三年 UAV small-object detection / YOLO 改进方法对比，至少在公开可复现模型范围内跑公平实验 |
| 小目标专项指标不足 | 题目强调 small object，但 AP-small/尺度分组证据还不够强 | 增加 APs/APm/APl、尺度 bin Recall、密度场景统计、类别/尺度交叉分析 |
| 稳定性不足 | 单次训练结果可能被质疑偶然性 | 核心模型补 3 seeds 或重复实验，至少对主模型和关键 baseline 给均值/方差 |
| 方法论证偏工程 | 当前描述更像工程改配置 | 增加结构图、数学符号、模块公式、算法流程、复杂度分析 |
| 英文写作缺口 | 中文稿不能直接翻译 | 建立 IEEEtran 英文稿，按英文期刊叙事重写 |
| 官方测试不足 | VisDrone test-dev 官方平台此前受账号限制 | 若平台可恢复，尽量补官方 test-dev；若不可行，明确只报告 val 并用多数据集补强 |

## 拟定英文论文主线

暂定英文题目方向：

> HRPCA-YOLO11n: High-Resolution P2 and Coordinate Attention Enhanced Lightweight YOLO for Small Object Detection in UAV Aerial Images

这个题目后续可能调整。若 CoordAttention 继续没有稳定增益，应避免把 CA 放在题目核心位置，可改为：

> A Lightweight High-Resolution Multi-Scale YOLO Framework for Small Object Detection in UAV Aerial Images

建议最终主张：

> This work does not aim to outperform larger-capacity detectors. Instead, it investigates how high-resolution feature branches, input resolution, and lightweight attention affect small-object detection in UAV imagery, and develops a lightweight detector with a favorable accuracy-speed-complexity trade-off.

中文理解：

> 本工作不是要证明小模型全面超过大模型，而是系统研究无人机小目标检测中高分辨率特征分支、输入分辨率和轻量注意力对精度、速度与复杂度的影响，并构建一个更适合轻量部署的检测器。

## 方法升级路线

### 路线 A：保守增强当前方法

保留 YOLO11n-P2-960 作为主方法，将 CoordAttention 作为辅助/可选模块，重点强调：

- P2 high-resolution branch for shallow spatial detail preservation.
- High-resolution input for improving effective small-object pixels.
- Lightweight accuracy-speed-complexity trade-off.
- Scale-aware analysis validating small-object gains.

优点：风险低，当前实验已支撑。

缺点：创新强度可能不足以支撑 IEEE Transactions。

### 路线 B：增加一个真正可命名的新模块

在当前 P2 分支基础上设计一个小目标特化模块，例如：

- Scale-Aware High-Resolution Fusion (SAHRF)
- Tiny Object Feature Calibration (TOFC)
- Density-Aware P2 Feature Aggregation (DPFA)
- Small-Object Preserving Augmentation and Assignment (SOPA)

要求：

- 模块必须有清晰动机，而不是堆叠现成模块。
- 必须能通过消融证明单独贡献。
- 必须控制参数量和 FPS 损失。
- 必须至少在 VisDrone 和 UAVDT 上验证。

优点：更接近 IEEE Transactions 的创新要求。

缺点：需要新增代码、重新训练、实验周期更长。

### 当前建议

优先采用路线 B，但先做小规模可行性验证。若新模块在 1-2 轮试验中没有稳定增益，则回退到路线 A，把论文定位为系统实验研究和轻量折中方法，目标期刊也相应下调。

## 推荐补充实验矩阵

### 数据集

| 数据集 | 用途 | 状态 |
| --- | --- | --- |
| VisDrone2019-DET | 主数据集 | 已完成基础实验 |
| UAVDT | 泛化验证与交通 UAV 场景补强 | 需下载、转换、训练 |
| AI-TOD 或 TinyPerson | 极小目标专项验证 | 需评估标注格式和训练成本 |
| VisDrone test-dev | 官方评测 | 平台账号问题待解决，可作为可选补强 |

### Baseline 与对比

| 类型 | 建议模型 | 目的 |
| --- | --- | --- |
| 轻量 YOLO | YOLOv5n/s、YOLOv8n/s、YOLO11n/s | 公平基础对比 |
| 主线消融 | YOLO11n、YOLO11n-960、YOLO11n-P2、YOLO11n-P2-960、YOLO11n-P2-CA、主方法 | 区分分辨率、P2、注意力和新模块贡献 |
| 近期方法 | 近三年 UAV/YOLO small-object papers 中可复现模型 | 对齐 IEEE 审稿期待 |
| Transformer/DETR 参考 | RT-DETR 或轻量 DETR 变体 | 增加方法类别多样性，若训练成本可控 |

### 指标

| 指标 | 必要性 |
| --- | --- |
| mAP50、mAP50-95 | 必须 |
| Precision、Recall | 必须 |
| AP-small/AP-medium/AP-large 或自定义尺度分组 AP/Recall | 必须 |
| Params、GFLOPs、weight size | 必须 |
| FPS、latency、preprocess/inference/postprocess | 必须 |
| GPU memory | 推荐 |
| 多 seed 均值/方差 | 推荐，核心模型必须争取 |
| 失败案例统计 | 推荐 |

### 消融实验

| 消融项 | 目的 |
| --- | --- |
| baseline vs P2 | 证明高分辨率检测分支贡献 |
| 640 vs 960 | 分离输入分辨率贡献 |
| P2 vs P2+CA | 真实评估注意力模块是否有效 |
| P2-960 vs 新模块-960 | 证明新模块是否有独立价值 |
| SmallObjAug 参数组 | 评估训练策略是否稳定 |
| 不同目标尺度分组 | 证明小目标改善来自小目标而非整体偶然波动 |
| 不同随机种子 | 证明结果稳定性 |

## 英文稿文件规划

建议新增独立英文投稿目录，避免污染 CEA 中文稿。

| 文件/目录 | 作用 |
| --- | --- |
| `paper/ieee_trans/main.tex` | IEEEtran 英文主稿 |
| `paper/ieee_trans/references.bib` | IEEE 英文参考文献 |
| `paper/ieee_trans/figures/` | 英文稿图文件 |
| `paper/ieee_trans/tables/` | 英文稿表格源文件 |
| `paper/ieee_trans/README.md` | 英文稿构建说明 |
| `paper/ieee_trans/cover_letter_draft.md` | 投稿信草稿 |
| `paper/ieee_trans_response_plan.md` | 审稿问题预案 |
| `paper/ieee_experiment_matrix.csv` | IEEE 目标实验矩阵 |
| `paper/ieee_claim_audit.md` | 英文稿 claim 与证据审计 |
| `tools/export_ieee_tables.py` | 从真实结果导出英文表格 |
| `tools/check_ieee_claims.py` | 检查英文稿中数字和主张是否有证据 |
| `tools/build_ieee_figures.py` | 生成英文图表 |

## 英文稿章节规划

1. Introduction
   - UAV aerial small-object detection motivation.
   - VisDrone/UAVDT-like scenes: tiny scale, occlusion, density, category ambiguity.
   - Limitations of lightweight detectors.
   - Contribution list: method, systematic analysis, multi-dataset experiments, efficiency.

2. Related Work
   - UAV object detection.
   - Small object detection and multi-scale feature fusion.
   - Lightweight YOLO detectors.
   - Attention mechanisms and coordinate/location-aware modeling.

3. Method
   - Overall architecture.
   - High-resolution P2 branch.
   - Attention/fusion or new module.
   - Training/inference details.
   - Complexity discussion.

4. Experiments
   - Datasets and evaluation metrics.
   - Implementation details.
   - Comparison with baselines and SOTA.
   - Ablation studies.
   - Scale-wise and density-wise analysis.
   - Speed and complexity analysis.
   - Qualitative visualization.

5. Discussion
   - Why high-resolution helps.
   - Why larger models still outperform in absolute accuracy.
   - Failure cases and limitations.
   - Deployment trade-offs.

6. Conclusion
   - Summarize validated contributions.
   - No exaggerated claims.

## 分阶段执行计划

### Phase 0：任务切换与资产冻结

目标：明确从 CEA 中文期刊切换到 IEEE Transactions 英文期刊。

动作：

- 新增本计划文档。
- 保留 CEA 目录，但不再主动维护中文 Word 稿。
- 新建 IEEE 独立目录和后续审计文件。
- 更新项目路线图，标记 CEA 为 paused。

预计产出：

- `paper/IEEE_TRANS_SUBMISSION_PLAN.md`
- 后续新增 `paper/ieee_trans/`

### Phase 1：目标期刊与文献调研

目标：确定最合适的 IEEE Transactions 目标刊物，并学习该刊近三年 UAV/small-object/YOLO 论文写法。

动作：

- 检索 IEEE Xplore、Google Scholar、arXiv 中近三年 UAV object detection、小目标检测、YOLO 改进论文。
- 整理目标刊物范围、平均篇幅、常见实验设置和审稿关注点。
- 输出候选论文阅读表。

预计产出：

- `paper/ieee_target_journal_analysis.md`
- `paper/ieee_related_work_matrix.csv`
- `paper/ieee_required_experiment_gap.md`

### Phase 2：方法创新重构

目标：决定是否只强化当前 HRPCA-YOLO11n，还是新增更强的小目标模块。

动作：

- 审计当前 P2、CA、960、SmallObjAug 的真实贡献。
- 设计 1-2 个小目标特化模块候选。
- 评估新增模块对参数量、FLOPs、FPS 的影响。
- 小规模快速训练验证可行性。

预计产出：

- `paper/ieee_method_design_notes.md`
- 新增或修改模型配置文件，例如 `configs/models/...`
- 快速验证日志和初步结果表。

### Phase 3：补充完整实验

目标：达到英文期刊级实验证据。

动作：

- 下载并转换 UAVDT 或其他补充数据集。
- 运行必要 baseline 和主方法。
- 对核心模型做多 seed 实验。
- 补 AP-small/scale-wise/density-wise 指标。
- 补速度、复杂度、显存统计。

预计产出：

- 新增 `runs/detect/...`
- `paper/tables/ieee_main_results.csv`
- `paper/tables/ieee_ablation_results.csv`
- `paper/tables/ieee_cross_dataset_results.csv`
- `paper/tables/ieee_speed_complexity.csv`
- `paper/tables/ieee_scale_results.csv`

### Phase 4：英文稿初版

目标：从零建立 IEEEtran 英文论文，而不是翻译中文稿。

动作：

- 下载或引入 IEEEtran 模板。
- 新建 `paper/ieee_trans/main.tex`。
- 写英文 Abstract、Introduction、Related Work、Method。
- 从真实 CSV 自动导出 LaTeX 表格。
- 生成英文结构图和实验图。

预计产出：

- `paper/ieee_trans/main.tex`
- `paper/ieee_trans/main.pdf`
- `paper/ieee_trans/references.bib`
- `paper/ieee_trans/figures/*`

### Phase 5：结果整合与主张审计

目标：确保英文稿中每个数字和结论都有证据。

动作：

- 建立 claim-to-evidence 表。
- 检查所有结果是否能追溯到日志和 CSV。
- 删除没有充分证据的强主张。
- 对比 YOLO11s-960 等强 baseline，避免夸大轻量模型优势。

预计产出：

- `paper/ieee_claim_audit.md`
- `paper/ieee_number_trace_audit.md`
- `paper/ieee_result_interpretation_matrix.md`

### Phase 6：语言润色与投稿包

目标：形成可交导师和可投稿的英文材料。

动作：

- 英文语法、逻辑、术语统一。
- 检查 IEEE 引用、图表标题、单位、缩写。
- 准备 cover letter。
- 准备 GitHub 代码说明和匿名/非匿名版本。
- 根据目标刊物要求准备 ScholarOne 或投稿系统材料。

预计产出：

- `paper/ieee_trans/main.pdf`
- `paper/ieee_trans/cover_letter_draft.md`
- `paper/ieee_submission_checklist.md`
- `paper/ieee_advisor_review_package.zip`

## 近期优先任务

1. 完成 `paper/IEEE_TRANS_SUBMISSION_PLAN.md`。
2. 建立 `paper/ieee_target_journal_analysis.md`，对 T-ITS、TGRS、TCSVT 做针对性分析。
3. 建立 `paper/ieee_required_experiment_gap.md`，把 IEEE 缺口转成实验清单。
4. 检索并整理近三年 UAV/YOLO/small-object detection 论文。
5. 决定是否设计新增模块；如果设计，先做快速可行性实验。
6. 规划服务器实验队列和预算。

## 需要导师或用户确认的问题

1. 目标 IEEE Transactions 是否已有导师明确指定？如果没有，优先按 T-ITS 还是 TGRS 准备？
2. 是否允许为 IEEE 目标新增模型模块和重新训练，而不是只整理现有实验？
3. 是否继续使用 VisDrone 作为主数据集，并补 UAVDT 作为第二数据集？
4. 是否接受较长实验周期，例如多 seed 和跨数据集实验？
5. 是否需要匿名投稿版本？不同 IEEE 期刊双盲要求不同，需要按目标刊物确认。
6. 作者、单位、基金、数据可用性和代码开源策略如何填写？

## 当前结论

当前项目已经超过普通课程报告或中文会议短文的基础水平，但距离 IEEE Transactions 仍有明显距离。最关键的不是格式迁移，而是三件事：

1. 找到更强、更可解释的方法创新点。
2. 补足跨数据集、SOTA、公平对比、尺度指标和稳定性实验。
3. 用 IEEE 英文论文方式重写贡献和论证，避免把工程配置调整包装成过强结论。

下一步应先完成目标刊物分析和实验缺口文档，再决定是否进入新增模块与大规模补实验阶段。

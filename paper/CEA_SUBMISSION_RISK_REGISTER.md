# 《计算机工程与应用》投稿风险登记表

本文档用于跟踪 YOLO VisDrone 项目在投稿《计算机工程与应用》前最容易被审稿人追问的风险点。它不是论文正文，不提供新的实验数值，也不替代真实训练日志；它的作用是把风险、证据来源和缓解动作固定下来，避免后续写作偏离真实证据。

## 使用规则

- 只有来自 `runs/`、`runs/logs/`、`paper/tables/`、配置文件、编译产物或官方评测返回结果的证据，才能支撑论文结论。
- 未完成的服务器实验只能作为进度信息，不得进入论文结果表、摘要或结论。
- 如果公平对比结果不支持“方法全面优于其他模型”，论文主张必须改为精度、速度、参数量和小目标场景适用性的折中分析。
- 每次同步服务器完整实验后，应重新运行 `python tools/run_paper_audits.py` 并更新本文档涉及的风险状态。

## 风险清单

| ID | 风险类别 | 严重性 | 当前状态 | 主要风险 | 证据/监控文件 | 缓解策略 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 公平对比 | High | Pending | 960 输入带来的收益可能被误写成结构创新收益。 | `paper/cea_server_status_snapshot.md`; `paper/tables/cea_experiment_status.csv`; `paper/CEA_RESULT_INTERPRETATION_MATRIX.md` | 等 YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960 完整 100 epoch 后再改写主结果与结论。 |
| R2 | 方法创新性 | High | Active | P2、CoordAttention 和高分辨率输入可能被审稿人认为是模块堆叠。 | `paper/CEA_SECTION_EVIDENCE_MAP.md`; `paper/CEA_REVIEW_GAP_ANALYSIS.md`; `paper/manuscript_submission_candidate.tex` | 按“航拍小目标问题 - 模块设计 - 真实证据”重写方法动机，避免宣称单个模块带来未经隔离的收益。 |
| R3 | 外部基线 | High | Pending | YOLOv5n、YOLOv8n、YOLO11n、YOLO11s 训练协议不一致会削弱对比可信度。 | `configs/train/`; `paper/commands.md`; `paper/tables/cea_experiment_status.csv` | 只把同数据集、同训练轮数、同评估流程的复现实验作为主对比；不同输入分辨率分层讨论。 |
| R4 | 小目标主题证据 | Medium | Active | “小目标检测”主题如果只靠总 mAP 支撑，会显得论证不足。 | `paper/tables/object_scale_distribution.csv`; `paper/tables/scale_group_results.csv`; `paper/figures/scale_analysis/`; `paper/failure_case_taxonomy.md` | 保留目标尺度分布、尺度分组匹配、类别混淆和失败案例分析，说明收益边界与困难场景。 |
| R5 | 速度与复杂度 | Medium | Active | 只报告精度会被认为缺少工程实用性；不同硬件测速不能直接混用。 | `paper/tables/speed_results.csv`; `paper/tables/model_complexity.csv`; `paper/tables/accuracy_speed_tradeoff.csv` | 所有纳入最终对比的模型在同一硬件和脚本下补测速度，并在论文中说明测试设置。 |
| R6 | 数值可追溯性 | High | Active | 论文中的小数、百分比或提升幅度如果不能追溯，会影响可信度。 | `paper/manuscript_number_trace_audit.md`; `paper/evidence_audit.md`; `paper/tables/` | 所有正文数值必须来自表格、日志、配置常量或脚本计算；禁止手工编造。 |
| R7 | 参考文献 | Medium | Active | 参考文献数量、近年相关性或格式不足，会削弱中刊论文感。 | `paper/reference_verification_matrix.md`; `paper/tex_reference_audit.md` | 只使用已核验来源的文献，补足近年 YOLO、无人机、小目标、多尺度和注意力机制相关工作。 |
| R8 | 版式与 PDF | Medium | Active | 图表浮动、乱码、断词、PDF 抽取异常会造成投稿前质量问题。 | `paper/tex_figure_audit.md`; `paper/text_hygiene_audit.md`; `paper/pdf_text_readability_audit.md`; `paper/manuscript_submission_candidate.pdf` | 每次修改 LaTeX 后重新编译 PDF，运行文本卫生和 PDF 可读性审计，并人工检查关键页面。 |
| R9 | 官方 test-dev | Low | Accepted | VisDrone 官方提交平台不可用时，不能报告官方 test-dev AP。 | `paper/testdev_submission.md`; `paper/evidence_audit.md` | 仅报告验证集结果；如果以后取得官方返回值，再以官方结果文件作为唯一来源。 |
| R10 | 服务器连续性 | Medium | Active | 租用服务器可能中断、被释放或队列训练失败。 | `paper/cea_server_status_snapshot.md`; `paper/tables/cea_server_status_history.csv`; `paper/cea_server_progress_report.md` | 只同步完整 100 epoch 结果；若中断，优先从 checkpoint 恢复，无法恢复时保留完整已完成实验并说明边界。 |
| R11 | GitHub 展示 | Low | Active | README 如果写成内部进度汇报，会影响给导师或读者查看项目。 | `README.md`; `paper/README.md`; `paper/submission_material_manifest.md` | 根目录 README 保持项目介绍、方法、数据、复现与论文材料导航，不写未完成清单式进度。 |
| R12 | 结论边界 | High | Pending | 如果新对照实验结果不占优，原有结论可能需要大幅降调。 | `paper/CEA_RESULT_INTERPRETATION_MATRIX.md`; `paper/post_sync_update_checklist.md`; `paper/manuscript_submission_candidate.tex` | 实验完成后按解释矩阵重写摘要、主结果、讨论和结论；必要时转向系统评估与折中分析型论文。 |

## 当前最高优先级

1. 等待服务器公平对比实验完成，保持 partial 结果不进入论文。
2. 继续补强不依赖新数值的材料：文献核验、方法动机、失败案例归因和投稿前审计。
3. 服务器实验达到 100 epoch 后，先同步和审计，再决定论文主张，不提前锁定结论。

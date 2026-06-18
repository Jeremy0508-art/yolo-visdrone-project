# 《计算机工程与应用》投稿前最终交接清单

本文档由 `tools/build_cea_final_handoff_checklist.py` 生成，用于把当前 YOLO VisDrone 项目从“本地材料已整理”推进到“可交导师审阅/准备投稿系统上传”的最后人工步骤。它不新增实验数值，不替代期刊官网要求，也不声明论文已经正式投稿就绪。

## 当前可交付材料

| 材料 | 路径 | 状态 | 说明 |
| --- | --- | --- | --- |
| 投稿候选 PDF | `paper/manuscript_submission_candidate.pdf` | READY | 已重新编译，机械版式审计通过 |
| LaTeX 源文件 | `paper/manuscript_submission_candidate.tex` | READY | 当前论文主源文件 |
| CEA Word 迁移初稿 | `paper/cea_template_migration/manuscript_cea_template_draft.docx` | READY | 已从当前 LaTeX 候选稿迁入 CEA Word 模板，仍需人工排版终审 |
| 项目 README | `README.md` | READY | 面向导师/读者的项目介绍版 |
| 导师汇报简版 | `paper/advisor_progress_brief.md` | READY | 简要说明研究目标、最终实验结果和风险边界 |
| 投稿材料清单 | `paper/submission_material_manifest.md` | READY | 当前 84/84 ready，0 missing |
| 审计仪表盘 | `paper/submission_audit_dashboard.md` | READY | 当前 30/33 ready，0 partial，3 pending，0 missing |
| 导师审阅包 | `paper/advisor_review_package.zip` | READY | 当前 39 files ready，0 missing，排除数据集、runs 和权重 |
| 总目标完成审计 | `paper/GOAL_COMPLETION_AUDIT.md` | PENDING | 本地可控材料高度完整，但仍保留人工/外部门槛 |
| 数值证据审计 | `paper/evidence_audit.md` | READY | 论文数值与表格/日志对应 |
| 数值追踪审计 | `paper/manuscript_number_trace_audit.md` | READY | LaTeX 正文小数均可追踪 |
| 复现实验命令 | `paper/commands.md` | READY | 训练、验证、测速、导表和审计命令记录 |

## 已完成的核心本地门槛

| 门槛 | 证据 | 结论 |
| --- | --- | --- |
| 公平对比实验 | `paper/synced_fair_experiment_artifacts_audit.md` | YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960、YOLOv5n-640 均已同步并审计 |
| 小目标专项分析 | `paper/tables/object_scale_distribution.csv`; `paper/tables/scale_group_results.csv` | 已包含尺度分布和按尺度匹配分析 |
| 主流模型对比 | `paper/tables/main_comparison_for_paper.csv` | 已包含 YOLOv5n、YOLOv8n、YOLO11n、YOLO11s 和本文模型 |
| 速度与复杂度 | `paper/tables/speed_results.csv`; `paper/tables/model_complexity.csv` | 已在同一测速脚本下整理 |
| 论文边界 | `paper/claim_boundary_audit.md` | 未发现“全面优于”等不受支持的过度结论 |
| PDF 机械检查 | `paper/pdf_layout_health_audit.md`; `paper/pdf_text_readability_audit.md` | 无空白页、PDF 可读性和基础版式检查通过 |
| GitHub 公共访问 | `paper/github_public_view_audit.md` | 公开仓库、raw README、PDF 和关键审计链接可访问 |

## 必须人工确认的投稿项

| 项目 | 当前状态 | 人工动作 |
| --- | --- | --- |
| 官方模板 | READY | 已取得并归档 `paper/templates/计算机工程与应用论文模版.docx`，模板要求摘要见 `paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md` |
| 模板迁移终审 | PENDING | 已生成 CEA Word 迁移初稿；仍需在 Word/WPS 中人工检查题名、作者、图表、参考文献、页眉页脚和最终分页 |
| 投稿文件类型 | PENDING | 确认系统要求上传 Word、PDF、源文件、图表附件或压缩包 |
| 作者信息 | PENDING | 确认作者顺序、单位、通信作者、邮箱、电话、邮编和可能的 ORCID 信息 |
| 基金/致谢/声明 | PENDING | 确认是否需要基金项目、利益冲突、数据可用性、原创性或版权声明 |
| 中英文摘要和关键词 | PENDING | 导师确认中文题名、英文题名、摘要长度、关键词翻译和术语一致性 |
| PDF 逐页目视检查 | PENDING | 人工检查 15 页 PDF；可先查看 `paper/figures/pdf_review/manuscript_pages_contact_sheet.jpg` 定位重点页 |
| GitHub 公开展示 | PENDING | 自动链接审计已通过，但仍需浏览器人工确认 README、PDF、图片和表格渲染正常 |
| VisDrone test-dev | PENDING | 官方平台可用并返回结果前，不写官方 test-dev AP |

## 给导师说明时的主结论边界

1. YOLO11s-960 在当前验证集上精度最高，说明更大模型容量仍然重要。
2. YOLO11n-P2-960 是当前 nano 级轻量模型中的较好折中点，mAP50 为 0.42361，mAP50-95 为 0.25552，FPS 为 55.68。
3. 960 输入分辨率是主要增益来源，P2 分支在高分辨率设置下仍有额外收益。
4. CoordAttention 在 640 输入下有小幅收益，但在 960 输入下未超过 P2-960，因此只能写成辅助设计和边界结果。
5. 当前论文只报告 VisDrone 验证集结果；官方 test-dev 结果必须等待官方平台返回。

## 建议交导师审阅的顺序

1. 先看 `paper/advisor_review_note.md` 和 `paper/advisor_progress_brief.md`，快速理解研究定位和最终结果。
2. 再看 `paper/manuscript_submission_candidate.pdf`，审阅论文正文、图表和结论。
3. 如导师追问数值来源，再打开 `paper/evidence_audit.md` 和 `paper/manuscript_number_trace_audit.md`。
4. 如导师追问投稿准备情况，再打开 `paper/GOAL_COMPLETION_AUDIT.md`、`paper/submission_audit_dashboard.md` 和 `paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md`。

## 当前不能关闭的事项

- CEA Word 迁移初稿已生成，但尚未经过 Word/WPS 人工终审。
- 投稿系统上传文件类型和最终格式要求仍需人工确认。
- 作者、单位、基金和声明信息需要用户/导师提供最终版本。
- PDF 逐页目视检查需要人工完成。
- GitHub 公开页面浏览器渲染需要人工确认。
- VisDrone 官方 test-dev 评测平台未返回官方指标。

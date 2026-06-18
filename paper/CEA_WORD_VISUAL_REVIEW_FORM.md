# CEA Word 初稿人工终审表

本文档用于人工检查 `paper/cea_template_migration/manuscript_cea_template_draft.docx`。自动审计已经确认该 Word 文件可解析、首页单栏、正文双栏、图表中英文题名齐全、10 个表格和 25 条参考文献已迁入；正式投稿前仍需要在 Microsoft Word 或 WPS 中逐页人工查看排版。

## 基本信息

| 项目 | 内容 |
| --- | --- |
| Word 文件 | `paper/cea_template_migration/manuscript_cea_template_draft.docx` |
| 迁移审计 | `paper/cea_template_migration/cea_word_migration_audit.md` |
| 质量审计 | `paper/cea_template_migration/cea_word_draft_quality_audit.md` |
| 检查人 | 待填写 |
| 检查日期 | 待填写 |

## 首页与元信息

| 检查项 | 状态 | 备注 |
| --- | --- | --- |
| 中文题名是否准确、简洁，且导师认可 | PENDING |  |
| 英文题名是否与中文题名一致 | PENDING |  |
| 作者顺序、单位、通信作者和邮箱是否补齐 | PENDING |  |
| 中图分类号、文献标志码是否符合期刊要求 | PENDING |  |
| 中文摘要约 300 字，且目的、方法、结果、结论完整 | PENDING |  |
| 英文摘要与中文摘要含义一致 | PENDING |  |
| 中英文关键词数量和翻译是否一致 | PENDING |  |

## 正文与图表

| 检查项 | 状态 | 备注 |
| --- | --- | --- |
| 首页为单栏，正文为双栏 | PENDING | 自动审计已通过，仍需 Word/WPS 目视确认 |
| 引言不单独编号，后续章节编号连续 | PENDING |  |
| 图题和表题中英文齐全 | PENDING | 自动审计已通过，仍需目视确认 |
| 表格为可编辑表格，不是图片 | PENDING | 自动审计已通过 |
| 表格未超出栏宽或页面 | PENDING |  |
| 图片清晰，检测框和曲线文字可读 | PENDING |  |
| 图表均在正文引用之后合理位置出现 | PENDING |  |
| 参考文献编号、正文引用和顺序一致 | PENDING |  |

## 投稿声明与联系信息

| 检查项 | 状态 | 备注 |
| --- | --- | --- |
| 基金项目和项目编号已确认 | PENDING | 没有基金时按投稿系统要求处理 |
| 致谢、利益冲突、数据可用性和代码可用性声明已确认 | PENDING |  |
| 文后联系人、通讯地址、邮箱和电话已补齐 | PENDING | 模板要求提供联系信息 |
| 投稿系统要求的附件、图包或版权文件已确认 | PENDING |  |

## 处理规则

- 发现数值问题时，先查 `paper/evidence_audit.md` 和 `paper/manuscript_number_trace_audit.md`，不要手工重算。
- 发现排版问题时，优先在 Word 初稿中人工调整；如需重新生成，修改 `tools/build_cea_word_draft.py` 后重新运行 `python tools/run_paper_audits.py`。
- 作者、单位、基金、声明和联系人信息必须由用户/导师确认后填写。

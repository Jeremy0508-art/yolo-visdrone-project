# CEA 模板迁移记录

本文档用于记录从当前通用 LaTeX 稿件迁移到《计算机工程与应用》官方模板或投稿系统格式的过程。用户已于 2026-06-18 提供投稿要求链接和 Word 模板；由于期刊官网和投稿系统要求可能变化，最终上传格式仍需在临近投稿时人工确认。

## 当前本地稿件

| 项目 | 内容 |
| --- | --- |
| 当前主源 | `paper/manuscript_submission_candidate.tex` |
| 当前 PDF | `paper/manuscript_submission_candidate.pdf` |
| 当前页数 | 15 页 |
| 当前本地状态 | 实验、表格、图、审计和 PDF 预览已整理 |

## 官方模板核验记录

| 字段 | 当前记录 |
| --- | --- |
| 核验日期 | 2026-06-18 |
| 核验人 | 用户提供链接和模板，Codex 本地归档与抽取 |
| 官方页面 URL | `http://cea.ceaj.org/CN/column/column16.shtml` |
| 模板文件名 | `计算机工程与应用论文模版.docx` |
| 本地模板路径 | `paper/templates/计算机工程与应用论文模版.docx` |
| 模板文件大小 | 90132 bytes |
| 模板 SHA256 | `1132c4747ac421b9c6b2e6d3e02e1af54f90f5ade1391e1df365e9fe5210cc9b` |
| 模板发布日期/版本 | 模板文件未显式记录，需投稿前人工复核 |
| 投稿要求文件类型 | 仍需在投稿系统人工确认 |
| 是否要求 Word | 已取得 Word 模板，最终是否必须 Word 仍需投稿系统确认 |
| 是否接受 PDF | 仍需在投稿系统人工确认 |
| 是否需要单独上传图表 | 模板要求图件清晰并按类型提供可编辑/高分辨率文件，最终上传方式仍需投稿系统确认 |
| 是否需要版权/原创性/利益冲突声明 | 仍需在投稿系统人工确认 |

## 模板要求摘要

详见 `paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md`。当前已从 Word 模板抽取并整理以下关键要求：题名一般不超过 25 字；摘要约 300 字；关键词 3～8 个；正文按模板双栏排版；图表需有中英文题名；表格采用三线表且不能以图片插入；参考文献建议 20 篇以上，中文文献需给出原英文信息；文后需提供联系人、通讯地址、邮箱和电话等信息。

## 迁移任务清单

| 任务 | 状态 | 备注 |
| --- | --- | --- |
| 取得官方 Word 模板并纳入项目 | READY | `paper/templates/计算机工程与应用论文模版.docx` |
| 抽取模板格式要求摘要 | READY | `paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md` |
| 生成 CEA Word 迁移初稿 | READY | `paper/cea_template_migration/manuscript_cea_template_draft.docx`；由 `tools/build_cea_word_draft.py` 从当前 LaTeX 候选稿生成 |
| 生成 CEA Word 迁移审计 | READY | `paper/cea_template_migration/cea_word_migration_audit.md` |
| 将中文题名、英文题名迁入官方模板 | READY | 已迁入初稿，仍需导师确认题名 |
| 将作者、单位、通信作者和邮箱补齐 | PENDING | 当前仅保留占位，需用户/导师提供 |
| 将中英文摘要和关键词迁入模板 | READY | 已迁入初稿；英文摘要为翻译草稿，需导师确认 |
| 按模板调整一级/二级标题格式 | PENDING |  |
| 按模板调整图题、表题和编号格式 | PENDING |  |
| 按模板调整参考文献格式 | PENDING |  |
| 补齐基金、致谢、声明或作者简介 | PENDING |  |
| 检查公式、表格和图片在模板中的版式 | PENDING |  |
| 重新生成最终 PDF 或 Word 文件 | PENDING | 已有 Word 初稿，最终稿需人工终审后另存 |
| 重新做逐页目视检查 | PENDING |  |

## 当前稿件迁移注意事项

1. 当前 LaTeX 稿件中的实验数值均应保留，不要在迁移到模板时手工重算。
2. 图表源文件集中在 `paper/figures/`，表格源文件集中在 `paper/tables/`。
3. 如模板要求 Word，优先从当前 PDF/LaTeX 和 `paper/manuscript_tables.md` 迁移内容。
4. 如模板要求压缩包，建议包含 PDF/Word、图表源文件、必要补充材料和作者信息表。
5. 官方 test-dev 指标未获得前，不要在模板中增加官方测试集结果。

## 迁移后验证

| 验证项 | 状态 | 备注 |
| --- | --- | --- |
| 数值与 `paper/tables/` 一致 | PENDING |  |
| 参考文献无乱码和异常断词 | PENDING |  |
| 图表编号和正文引用一致 | PENDING |  |
| 摘要、关键词和结论边界一致 | PENDING |  |
| PDF/Word 文件可正常打开 | PENDING |  |
| 导师确认可投稿 | PENDING |  |

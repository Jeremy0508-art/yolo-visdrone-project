# PDF 逐页目视检查表

本文档用于人工检查 `paper/manuscript_submission_candidate.pdf`。自动审计已经确认 PDF 可编译、无空白页、基础版式健康，但投稿前仍需要逐页人工查看图表位置、文字遮挡、页底浮动图和参考文献显示。

## 基本信息

| 项目 | 内容 |
| --- | --- |
| PDF 文件 | `paper/manuscript_submission_candidate.pdf` |
| 当前页数 | 15 页 |
| 机械版式审计 | `paper/pdf_layout_health_audit.md` |
| 文本可读性审计 | `paper/pdf_text_readability_audit.md` |
| 检查人 | 待填写 |
| 检查日期 | 待填写 |

## 逐页检查

| 页码 | 检查重点 | 状态 | 备注 |
| ---: | --- | --- | --- |
| 1 | 标题、摘要、关键词、首页排版是否正常 | PENDING |  |
| 2 | 引言段落、贡献点和引用是否连贯 | PENDING |  |
| 3 | 相关工作排版、引用和段落间距 | PENDING |  |
| 4 | 方法结构表/图是否清晰，无越界 | PENDING |  |
| 5 | P2、CoordAttention、高分辨率输入描述是否连续 | PENDING |  |
| 6 | 实验设置表格是否完整，硬件和训练配置是否清楚 | PENDING |  |
| 7 | 主结果表、外部基线表是否未超出页面 | PENDING |  |
| 8 | 消融、尺度分布图表是否编号正确 | PENDING |  |
| 9 | 类别级结果和尺度分析是否可读 | PENDING |  |
| 10 | 速度复杂度表、精度-速度图是否清晰 | PENDING |  |
| 11 | 可视化检测图是否位置正常，图注完整 | PENDING |  |
| 12 | 失败案例图是否未挤压正文或结论 | PENDING |  |
| 13 | 讨论和结论是否连续，无图表插入中断 | PENDING |  |
| 14 | 参考文献是否无乱码、异常断词、URL 溢出 | PENDING |  |
| 15 | 参考文献结尾、页底和最后一页是否正常 | PENDING |  |

## 必查问题

| 问题 | 状态 | 备注 |
| --- | --- | --- |
| 图表是否都在正文引用之后附近出现 | PENDING |  |
| 表格是否有超出页面或字体过小 | PENDING |  |
| 图中文字是否清晰，尤其是混淆矩阵和检测框标签 | PENDING |  |
| 结论是否没有被图表打断 | PENDING |  |
| 参考文献是否无乱码、软连字符和异常断词 | PENDING |  |
| 正文是否没有 TODO、待补充、内部备注 | PENDING |  |
| 数值是否与 `paper/tables/` 和审计文件一致 | PENDING |  |

## 处理规则

- 如果只是图表位置问题，优先在 LaTeX 中调整浮动、宽度或 `FloatBarrier`。
- 如果发现数值不一致，先查 `paper/manuscript_number_trace_audit.md` 和 `paper/evidence_audit.md`，不要手工改数。
- 如果发现期刊模板要求与当前 PDF 不一致，先记录在 `paper/CEA_TEMPLATE_MIGRATION_RECORD.md`，再决定是否迁移到 Word 或官方模板。

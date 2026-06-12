# 投稿前检查清单

本清单用于把 `paper/manuscript_polished.md` 推进到正式中文会议投稿稿。当前阶段已经有完整论文文本、表格、图像、参考文献草案和证据审计，后续重点是模板适配与人工审阅。

## 已完成

| 项目 | 状态 | 位置 |
| --- | --- | --- |
| 完整中文论文润色稿 | 已完成 | `paper/manuscript_polished.md` |
| 精简投稿候选稿 | 已完成 | `paper/manuscript_submission_candidate.md` |
| LaTeX 投稿候选稿 | 已完成 | `paper/manuscript_submission_candidate.tex` |
| LaTeX PDF 预览 | 已完成 | `paper/manuscript_submission_candidate.pdf` |
| HTML 浏览器预览 | 已完成 | `paper/manuscript_polished.html` |
| 主结果表、消融表、速度表 | 已完成 | `paper/manuscript_tables.md` |
| 正文推荐图 | 已完成 | `paper/selected_figures.md` |
| 数值证据审计 | 已完成 | `paper/evidence_audit.md` |
| 参考文献草案 | 已完成 | `paper/references.md` |
| 复现实验命令 | 已完成 | `paper/commands.md` |

## 投稿前必须检查

| 检查项 | 当前建议 |
| --- | --- |
| 会议模板 | 等确定目标会议后，将 `manuscript_polished.md` 迁移到 Word 或 LaTeX 模板 |
| 篇幅 | 若模板限制较紧，优先保留表 1、表 2、表 3 和 3 张核心图 |
| 图像 | 正文建议使用 `selected_figures.md` 中的图 1、图 4、图 5，篇幅允许再加 PR 曲线和混淆矩阵 |
| 参考文献 | 目前为 GB/T 7714 风格草案，需按会议要求统一 |
| 官方测试集 | 当前不能写官方 AP，只能写“本地提交包已准备，官方结果后续补充” |
| 创新性表述 | 保持“构建并评估”“实验验证”“轻量化改进”这类稳健措辞 |
| 实验数值 | 任何新增数值都必须先加入 `paper/tables/` 或在 `evidence_audit.md` 中补证据 |

## 建议保留图表

短篇会议版本建议正文保留：

1. 表 1：主实验结果。
2. 表 2：消融实验结果。
3. 表 3：速度与复杂度结果。
4. 图 1：最佳模型训练曲线。
5. 图 4：验证集检测示例。
6. 图 5：困难样例或误差分析。

PR 曲线和混淆矩阵可作为篇幅充足时的补充图。

当前 `paper/manuscript_polished.md` 已嵌入 5 张推荐图。若目标会议篇幅较短，可删除正文中的图 2 和图 3，仅保留训练曲线、检测示例和困难样例。

`paper/manuscript_submission_candidate.md` 已按短篇会议思路保留 3 张核心图，可作为模板适配的优先版本。

当前已有通用 `ctexart` LaTeX 版本：`paper/manuscript_submission_candidate.tex`。如果目标会议提供专用 LaTeX 模板，优先把该文件中的正文、表格、图和参考文献迁移到模板中。

当前也已使用本地 Tectonic 引擎生成 PDF：`paper/manuscript_submission_candidate.pdf`。正式投稿前仍建议用目标会议模板重新编译并人工检查版面。

当前 LaTeX 预览版仍有少量 underfull 行距警告和一个 figure/table 分页相关的 overfull vbox 警告，但 PDF 可以稳定生成。正式模板适配时需要重新检查图表浮动位置。

## HTML 预览生成命令

```powershell
python tools/render_markdown_preview.py --input paper/manuscript_polished.md --output paper/manuscript_polished.html
```

该 HTML 只是阅读预览，不是正式投稿格式。

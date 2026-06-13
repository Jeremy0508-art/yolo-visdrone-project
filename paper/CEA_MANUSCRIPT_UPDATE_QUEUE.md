# 《计算机工程与应用》期刊长文更新队列

本文档用于服务器公平对照实验完成后的论文重写执行。它不是正文，不提供新数值；它规定“结果回来以后先改哪里、怎么改、用什么证据证明可以改”。

## 1. 当前稿件基线

当前可读稿件入口：

- LaTeX 候选稿：`paper/manuscript_submission_candidate.tex`
- PDF 预览：`paper/manuscript_submission_candidate.pdf`
- Markdown 候选稿：`paper/manuscript_submission_candidate.md`

当前稿件已经具备：

- YOLO11n 主线消融结果。
- YOLOv8n-640、YOLO11s-640 外部参考基线。
- 速度、复杂度、类别级结果、目标尺度分布、尺度分组召回和可视化分析。

当前稿件尚未具备：

- YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960 和 YOLOv5n-640 的完整公平对照结果。
- 基于上述公平对照结果重写后的最终摘要、结论和实验分析。
- 完整期刊长文版 `paper/manuscript_cea_journal.tex`。

## 2. 服务器结果完成后的处理顺序

服务器实验完成后，按以下顺序处理，不能直接先改摘要和结论。

1. 同步完整 run：
   - 运行 `.\tools\sync_cea_server_results.ps1 -MinEpochs 100`。
   - 只接受脚本判定为 `READY` 的 run。
   - 对 `PARTIAL:<epochs>` 的 run 不做论文集成。

2. 重建证据表：
   - 运行 `python tools/export_paper_tables.py`。
   - 运行 `python tools/audit_submission_readiness.py`。
   - 如果有新权重完成同步，再补跑速度、类别级、尺度分组和精度速度折中图。

3. 先更新结果表：
   - `paper/tables/main_comparison_for_paper.csv`
   - `paper/tables/model_complexity.csv`
   - `paper/tables/speed_results.csv`
   - `paper/tables/accuracy_speed_tradeoff.csv`
   - 必要时更新 `paper/tables/per_class_results.csv` 和 `paper/tables/scale_group_results.csv`

4. 再更新实验分析：
   - 公平分辨率对照。
   - 主流 YOLO 对照。
   - 消融解释。
   - 速度复杂度讨论。
   - 小目标尺度分析。

5. 最后更新摘要和结论：
   - 摘要中的最高指标、提升幅度和速度必须来自更新后的表格。
   - 结论不能提前写“全面优于”，必须由公平对照结果决定。

## 3. 需要新增或重写的正文小节

| 小节 | 更新条件 | 证据来源 | 写作重点 |
| --- | --- | --- | --- |
| 4.2 主实验结果 | 当前已可写，后续需补新模型 | `main_comparison_for_paper.csv` | 说明当前主方法相对 YOLO11n baseline 的提升 |
| 4.3 分辨率公平对照 | 960 对照完成后写 | YOLO11n-960、YOLO11n-P2-960、YOLO11n-P2-CA-960 | 隔离 960 输入与结构改进贡献 |
| 4.4 主流 YOLO 对照 | YOLOv5n/YOLOv8n/YOLO11s 完成后写 | 主流 baseline runs | 讨论版本、容量、输入分辨率和参数效率 |
| 4.5 消融实验 | 已可写，后续按公平结果修正措辞 | `ablation_results.csv` | P2、CA、960、SmallObjAug 的贡献边界 |
| 4.6 小目标尺度分析 | 已可写，后续可扩展新模型 | `object_scale_distribution.csv`, `scale_group_results.csv` | 证明 VisDrone 小目标占比高，收益集中在 small/medium |
| 4.7 类别级分析 | 已可写，后续可补最终模型 | `per_class_results.csv` | 分析易检类别和易混类别 |
| 4.8 速度与复杂度 | 新模型速度补测后写 | `speed_results.csv`, `model_complexity.csv` | 精度-速度-参数量折中 |
| 4.9 可视化与失败案例 | 已可写，后续按最终模型更新图 | `paper/figures/` | 密集、遮挡、极小目标、类别混淆 |

## 4. 根据结果选择论文主张

公平对照完成后，按结果选择主张，避免不公平比较。

### 情况 A：本文方法明显优于 YOLO11n-960

可写：

> 在相同 960 输入分辨率下，P2 高分辨率分支与 CoordAttention 仍带来稳定提升，说明本文方法的收益并非仅来自输入分辨率提高。

### 情况 B：本文方法与 YOLO11n-960 接近

可写：

> 高分辨率输入是主要增益来源，P2 分支和 CoordAttention 提供轻量级补充增强。本文贡献重点转为系统分析轻量 YOLO 在无人机小目标场景中的分辨率、结构和速度折中关系。

### 情况 C：YOLO11s-960 精度更高

可写：

> YOLO11s-960 体现出更大模型容量的精度上限，但其参数规模更高。本文方法更适合作为轻量级精度-速度折中方案。

只有在参数量、速度或综合效率指标支持时，才能强调“轻量化优势”。

### 情况 D：YOLOv8n-960 或 YOLOv5n 表现接近

可写：

> 外部基线结果说明，不同 YOLO 版本在 VisDrone 上具有接近的轻量化检测能力。本文方法的结论应限定在当前训练协议和 YOLO11n 改进体系内。

不能写：

> 本文方法全面优于所有 YOLO 模型。

## 5. 摘要更新模板

最终摘要应按以下信息填充：

1. 背景：无人机航拍小目标、密集遮挡、类别相似。
2. 方法：YOLO11n + P2 + CoordAttention + 960 输入。
3. 结果：
   - 最终主方法 mAP50 和 mAP50-95。
   - 相对公平 baseline 的提升，而不是只相对 640 baseline。
   - 参数量、速度或综合折中指标。
4. 结论：根据实际结果选择“结构有效”“分辨率主导”或“轻量折中”。

摘要中的任何数字必须来自 `paper/tables/` 或完整 run 日志。

## 6. 结论更新模板

最终结论应包含：

- 对 P2 分支作用的真实判断。
- 对 CoordAttention 作用的真实判断。
- 对 960 输入贡献的真实判断。
- 对外部 YOLO baseline 的公平解释。
- 对速度成本和部署边界的说明。
- 官方 test-dev 不可用时，只报告验证集结果。

结论中不能出现：

- 未完成实验名称作为已完成结果。
- 官方 AP 的推断值。
- 没有表格支撑的“全面优于”“显著优于所有方法”。

## 7. 最终长文文件计划

公平对照结果同步并审计通过后，创建或更新：

- `paper/manuscript_cea_journal.tex`
- `paper/manuscript_cea_journal.pdf`

建议从 `paper/manuscript_submission_candidate.tex` 迁移，但重新组织为期刊长文结构：

1. 引言。
2. 相关工作。
3. 方法。
4. 实验设置。
5. 实验结果与分析。
6. 讨论。
7. 结论。

当前阶段不提前创建含占位数值的最终长文 PDF，避免误认为已经具备投稿稿件。

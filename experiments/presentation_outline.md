# 项目汇报提纲：基于改进 YOLO 的无人机航拍小目标检测系统

本提纲用于课程答辩、项目汇报或 PPT 制作。建议控制在 10 到 12 页。

## 1. 封面

标题：基于改进 YOLO 的无人机航拍小目标检测系统

建议包含：

- 项目主题：VisDrone 小目标检测
- 基础模型：Ultralytics YOLO11n
- 改进方向：P2 小目标检测层、CoordAttention 注意力
- 系统实现：训练、验证、推理、Flask Web 展示

讲述重点：

本项目不是单一 demo，而是围绕 VisDrone 数据集构建了一套完整的目标检测工程，包括数据处理、模型训练、消融实验、可视化分析和 Web 应用。

## 2. 研究背景与问题

建议内容：

- 无人机航拍在交通监控、城市管理、应急巡检等场景中应用广泛。
- 航拍图像中目标通常尺度小、分布密集、遮挡严重。
- 传统检测模型容易出现漏检、类别混淆和定位不准。

可讲述句：

VisDrone 数据集中大量目标只占图像很小区域，因此小目标检测能力是系统效果的关键。

## 3. 数据集介绍

数据集：VisDrone2019-DET 图像目标检测任务。

当前使用规模：

| Split | Images | Boxes |
| --- | ---: | ---: |
| train | 6471 | 343204 |
| val | 548 | 38759 |
| test-dev | 1580 | 0 |

类别：

pedestrian、people、bicycle、car、van、truck、tricycle、awning-tricycle、bus、motor。

讲述重点：

项目编写了 VisDrone 到 YOLO 格式的转换脚本，并通过检查脚本验证图像、标签和目标框数量，保证训练数据可靠。

## 4. 工程结构

建议展示目录结构图：

```text
configs/      配置文件
data/         原始数据与转换后数据
scripts/      数据转换与检查
src/          可复用模块
tools/        训练、验证、推理入口
experiments/  实验记录与报告材料
web/          Flask Web 页面
runs/         训练和推理输出
```

讲述重点：

项目按工程化方式组织，训练脚本、模型配置、数据处理、Web 展示相互独立，方便后续扩展和消融实验。

## 5. Baseline 模型

基础模型：YOLO11n。

训练设置：

- 输入尺寸：640
- 训练轮数：100
- batch：8
- 数据集：VisDrone2019-DET

Baseline 最终结果：

| Precision | Recall | mAP50 | mAP50-95 |
| ---: | ---: | ---: | ---: |
| 0.45440 | 0.33922 | 0.31985 | 0.18066 |

建议配图：

```text
experiments/figures/curves/baseline_results.png
experiments/figures/curves/baseline_pr_curve.png
```

## 6. 改进一：P2 小目标检测层

改进思路：

- YOLO 默认检测头更偏向 P3/P4/P5。
- VisDrone 中大量目标尺度很小，浅层高分辨率特征更重要。
- 增加 P2 检测层，让模型利用更高分辨率特征预测小目标。

实验结果：

| Model | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-P2 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |

最佳指标提升：

| Model | Best mAP50 | Best mAP50-95 |
| --- | ---: | ---: |
| YOLO11n baseline | 0.32153 | 0.18238 |
| YOLO11n-P2 | 0.33013 | 0.19012 |

讲述重点：

P2 提升了 Recall、mAP50 和 mAP50-95，说明高分辨率检测层对无人机航拍小目标检测有效。

## 7. 改进二：P2 + CoordAttention

改进思路：

- 在 P2 高分辨率检测头基础上加入 CoordAttention。
- CoordAttention 同时编码水平和垂直方向位置信息，增强模型对关键空间区域的关注。
- 本项目将其放置在 P4/P5 语义特征路径，保留 P2 高分辨率分支。

实验结果：

| Model | Best mAP50 | Best mAP50-95 |
| --- | ---: | ---: |
| YOLO11n-P2 | 0.33013 | 0.19012 |
| YOLO11n-P2-CoordAttention | 0.33073 | 0.19044 |

讲述重点：

CoordAttention 在 P2 基础上带来轻微正提升，当前作为 Web 演示默认权重。

## 8. 消融实验总结

建议放置表格：

| Model | Main Change | Best mAP50 | Best mAP50-95 | 结论 |
| --- | --- | ---: | ---: | --- |
| YOLO11n baseline | 原始模型 | 0.32153 | 0.18238 | 基准实验 |
| YOLO11n-P2 | 小目标检测头 | 0.33013 | 0.19012 | 有效提升 |
| YOLO11n-P2-CoordAttention | P2 + 坐标注意力 | 0.33073 | 0.19044 | 当前最佳 |

建议配图：

```text
experiments/figures/curves/p2_results.png
experiments/figures/confusion/p2_confusion_matrix_normalized.png
```

讲述重点：

P2 是主要有效结构改进，CoordAttention 在其基础上带来小幅增益。

## 9. 定性案例分析

建议展示：

```text
experiments/cases/p2_case_contact_sheet.jpg
```

成功案例：

- 目标数量适中、目标清晰时，P2 召回较好。
- `0000360_06861_d_0000748.jpg` 粗略召回达到 0.96。

困难案例：

- 极小目标、密集人群和远距离车辆仍容易漏检。
- `0000276_03201_d_0000523.jpg` 粗略召回约 0.13。

讲述重点：

P2 能改善小目标检测，但 VisDrone 的远距离密集目标仍然具有挑战性，这也是后续继续优化的方向。

## 10. Flask Web 系统

功能：

- 上传图片或视频。
- 调用 P2+CoordAttention 最佳权重进行检测。
- 页面展示检测后的图片或视频。

启动命令：

```powershell
python web/app.py
```

访问地址：

```text
http://127.0.0.1:5000
```

默认权重：

```text
runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt
```

讲述重点：

Web 页面把训练好的模型封装成可交互应用，体现项目从算法实验到系统展示的完整闭环。

## 11. 项目完成情况

已完成：

- VisDrone 数据集转换脚本。
- YOLO 格式 dataset.yaml。
- Baseline 训练与验证。
- P2 小目标检测层消融。
- P2+CoordAttention 组合实验。
- 图片检测与视频检测脚本。
- 可视化结果整理。
- 成功/失败案例分析。
- Flask Web 上传检测页面。

## 12. 总结与展望

总结：

- 当前最佳模型是 YOLO11n-P2-CoordAttention。
- P2 相比 baseline 提升了小目标检测效果，CoordAttention 在 P2 基础上带来轻微正提升。
- 系统已形成数据、训练、验证、推理、Web 展示的完整流程。

后续方向：

- 增大输入尺寸到 960。
- 优化小目标数据增强策略。
- 分析 pedestrian、people、motor 等易混淆类别。
- 尝试模型压缩或部署优化。

# 基于改进 YOLO 的 VisDrone 无人机航拍小目标检测系统

针对无人机航拍场景中目标尺度小、分布密集、遮挡严重、类别外观相近，导致轻量化 YOLO 模型容易出现漏检和误检的问题，本项目提出并实现了一个基于改进 YOLO11n 的 VisDrone 小目标检测系统。

项目以 Ultralytics YOLO11n 为基线，从三个方面提升航拍小目标检测能力：一是在检测头中引入 P2 高分辨率小目标检测分支，增强浅层空间细节利用；二是在特征融合结构中加入 CoordAttention 注意力模块，提高位置敏感特征表达；三是采用 960 输入分辨率和小目标友好数据增强策略，提升小目标在输入图像和特征图中的有效像素占比。

系统完成了 VisDrone2019-DET 数据转换、YOLO 格式数据校验、baseline 训练、改进模型训练、消融实验、模型复杂度统计、推理速度测试、图片/视频推理、Flask Web 可视化检测页面和论文材料整理。当前数据集包含 6,471 张训练图像、548 张验证图像和 343,204 个训练标注框，覆盖 pedestrian、people、car、motor 等 10 类航拍目标。

在 100 epoch 训练设置下，YOLO11n-P2-960 在 nano 级轻量模型中取得较好的精度-速度折中，Best mAP50 达到 `0.42361`，Best mAP50-95 达到 `0.25552`，高于 YOLO11n-960 的 `0.42136` / `0.25067` 和 YOLO11n-P2-CoordAttention-960 的 `0.41996` / `0.25174`，单图 wall-clock 推理速度为 `55.68 FPS`。更大容量的 YOLO11s-960 达到 `0.48901` / `0.29812`，说明模型容量仍是提升检测精度的重要因素。当前结果表明，960 输入分辨率是主要增益来源，P2 高分辨率检测分支在高分辨率设置下仍能带来额外提升，CoordAttention 在当前设置下更适合作为辅助设计而不是主要性能来源。项目最终形成了一个可复现、可评估、可展示，并可同时支撑中文期刊论文与 IEEE Transactions 英文论文准备的无人机航拍小目标检测实验闭环。

## 方法思路

| 模块 | 作用 |
| --- | --- |
| YOLO11n baseline | 构建轻量化检测基线 |
| P2 高分辨率检测分支 | 利用浅层高分辨率特征，增强小目标定位能力 |
| CoordAttention | 引入方向位置信息，提高复杂背景下的特征表达能力 |
| 960 输入分辨率 | 增加小目标有效像素占比，改善小目标检测稳定性 |
| SmallObjAug | 调整 mosaic、scale、copy-paste 和 erasing，分析小目标友好增强效果 |

## 项目结构

```text
.
├── configs/                 # 数据集、模型结构、训练配置
│   ├── dataset/visdrone.yaml
│   ├── models/yolo11n_p2.yaml
│   ├── models/yolo11n_p2_coordatt.yaml
│   └── train/
├── data/
│   ├── raw/VisDrone/         # VisDrone 原始数据
│   └── processed/            # 转换后的 YOLO 格式数据
├── paper/                    # 论文稿件、表格、图表、PDF 和复现实验命令
├── runs/                     # Ultralytics 训练、验证、推理输出
├── scripts/                  # 数据集转换与检查脚本
├── src/                      # 可复用数据、模型和工具模块
├── tools/                    # 训练、验证、推理、测速和论文表格导出脚本
├── web/                      # Flask Web 检测页面
├── weights/                  # 模型权重目录
└── requirements.txt
```

## 环境安装

```powershell
pip install -r requirements.txt
```

推荐使用支持 CUDA 的 PyTorch 环境训练。若只做推理或 Web 展示，CPU 也可以运行，但速度会明显较慢。

项目自检：

```powershell
python tools/verify_project.py
```

## 数据集准备

本项目使用 VisDrone 图像目标检测任务，即 `VisDrone2019-DET`。原始数据应放在：

```text
data/raw/VisDrone/
├── VisDrone2019-DET-train/
├── VisDrone2019-DET-val/
└── VisDrone2019-DET-test-dev/
```

转换为 YOLO 格式：

```powershell
python scripts/convert_visdrone_to_yolo.py --raw-root data/raw/VisDrone --output-root data/processed/visdrone_yolo
```

检查转换结果：

```powershell
python scripts/check_dataset.py --dataset-root data/processed/visdrone_yolo
```

数据检查结果：

| Split | Images | Boxes |
| --- | ---: | ---: |
| train | 6471 | 343204 |
| val | 548 | 38759 |
| test-dev | 1580 | 0 |

## 训练与验证

训练 YOLO11n baseline：

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolo11n.yaml
```

训练 YOLO11n-P2：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_pretrained_init.pt
```

训练 YOLO11n-P2-CoordAttention：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_pretrained_init.pt
```

训练 YOLO11n-P2-CoordAttention-960：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_960.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_960_pretrained_init_full.pt
```

训练 YOLO11n-P2-CoordAttention-SmallObjAug：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml --pretrained-weights yolo11n.pt --pretrained-mode p2 --init-output weights/yolo11n_p2_coordatt_smallobj_aug_init.pt
```

验证模型：

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0
```

## 推理与 Web 演示

图片检测：

```powershell
python tools/detect_image.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --source data/processed/visdrone_yolo/images/val --save-dir runs/detect_image/p2_coordatt_960_val_samples
```

视频检测：

```powershell
python tools/detect_video.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --source path/to/video.mp4 --save-dir runs/detect_video/p2_coordatt_960_video
```

启动 Flask 页面：

```powershell
python web/app.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

Web 页面支持上传图片或视频，并在页面中展示检测结果。

![Web demo](paper/figures/web_demo.png)

## 实验结果

主实验验证集结果如下：

| Model | Main Change | Input | Best mAP50 | Best mAP50-95 | FPS |
| --- | --- | ---: | ---: | ---: | ---: |
| YOLO11n | baseline | 640 | 0.32153 | 0.18238 | 70.09 |
| YOLO11n baseline 960 | baseline at 960 input | 960 | 0.42136 | 0.25067 | 61.09 |
| YOLO11n-P2 | P2 high-resolution detection head | 640 | 0.33013 | 0.19012 | 65.38 |
| YOLO11n-P2-960 | P2 at 960 input | 960 | 0.42361 | 0.25552 | 55.68 |
| YOLO11n-P2-CoordAttention | P2 + CoordAttention | 640 | 0.33073 | 0.19044 | 62.39 |
| YOLO11n-P2-CoordAttention-960 | P2 + CoordAttention at 960 input | 960 | 0.41996 | 0.25174 | 52.63 |
| YOLO11n-P2-CoordAttention-SmallObjAug | small-object-friendly augmentation | 640 | 0.32780 | 0.18699 | 60.63 |

实验表明，P2 高分辨率检测分支能够提升浅层细节利用能力，960 输入分辨率是当前实验中最主要的性能提升来源。YOLO11n-P2-960 在 mAP50 和 mAP50-95 上均高于 YOLO11n-960，说明 P2 分支在高分辨率输入下仍有价值；YOLO11n-P2-CoordAttention-960 未超过 YOLO11n-P2-960，因此当前结论应避免把注意力模块夸大为决定性增益来源。YOLO11s-960 精度最高，但参数量更大，适合作为容量上限参考。

小目标尺度分析结果如下，统计口径采用 small `<32^2`、medium `32^2-96^2`、large `>=96^2` 的目标框面积划分：

| Split | Small | Medium | Large | Small Ratio |
| --- | ---: | ---: | ---: | ---: |
| train | 207604 | 116620 | 18980 | 60.49% |
| val | 26586 | 11105 | 1068 | 68.59% |

在 `conf=0.25`、`IoU=0.5` 的验证集匹配分析下，YOLO11n-P2-CoordAttention-960 的 small 目标召回率为 `0.45509`，高于 YOLO11n baseline 的 `0.30768`；该统计用于分析不同尺度目标的检测匹配情况，不等同于官方 AP。

外部参考基线结果如下，用于辅助分析不同 YOLO 版本和模型容量下的精度-速度关系，不作为 YOLO11n 改进模块的单因素消融：

| Model | Input | Params/M | Best mAP50 | Best mAP50-95 | FPS |
| --- | ---: | ---: | ---: | ---: | ---: |
| YOLOv8n baseline | 640 | 3.013 | 0.32520 | 0.18386 | 33.81 |
| YOLOv8n baseline 960 | 960 | 3.013 | 0.42016 | 0.25121 | 69.91 |
| YOLO11s baseline | 640 | 9.432 | 0.38937 | 0.22719 | 70.29 |
| YOLO11s baseline 960 | 960 | 9.432 | 0.48901 | 0.29812 | 62.13 |
| YOLOv5n baseline | 640 | 2.510 | 0.31030 | 0.17513 | 76.95 |

详细实验表格位于：

```text
paper/tables/main_results.csv
paper/tables/ablation_results.csv
paper/tables/model_complexity.csv
paper/tables/speed_results.csv
paper/tables/per_class_results.csv
paper/tables/object_scale_distribution.csv
paper/tables/scale_group_results.csv
```

## 论文材料

论文相关材料集中整理在 `paper/` 目录。本项目采用中文期刊与英文期刊双轨准备：中文稿面向《计算机工程与应用》等中文期刊投稿要求，英文稿面向 IEEE Transactions 路线，两条路线共享真实实验结果、图表、日志和复现脚本，但稿件结构、写作语言、目标期刊要求和投稿材料分别维护。

当前英文投稿路线的核心材料包括：

```text
paper/README.md
paper/DUAL_SUBMISSION_STRATEGY.md
paper/IEEE_TRANS_SUBMISSION_PLAN.md
paper/ieee_submission_dashboard.md
paper/ieee_target_journal_analysis.md
paper/ieee_tits_scope_fit_checklist.md
paper/ieee_method_selection_protocol.md
paper/ieee_reviewer_risk_register.md
paper/ieee_scale_result_interpretation.md
paper/ieee_scale_ap_interpretation.md
paper/ieee_trans/
paper/commands.md
paper/figures/
paper/tables/
```

其中 `paper/ieee_trans/` 保存 IEEE 英文稿规划、章节草稿、表格草稿和 `main.tex` 创建前检查清单；`paper/ieee_submission_dashboard.md` 汇总当前证据状态和未完成门槛；`paper/ieee_scale_result_interpretation.md` 与 `paper/ieee_scale_ap_interpretation.md` 分别记录尺度召回/精度和本地 scale-bin AP 诊断结果。中文期刊稿件、CEA 模板迁移、Word/PDF 预览和投稿前审计材料也保留在 `paper/` 中，作为当前中文投稿路线的一部分继续维护。

编译 LaTeX PDF：

```powershell
.\tools\build_paper_pdf.ps1
```

## 结果可复现说明

论文和 README 中的实验数值均来自真实训练日志、验证输出和 `paper/tables/` 汇总文件。项目保留训练、验证、测速、类别级指标收集和论文表格导出脚本，便于复现实验流程和继续扩展对比实验。

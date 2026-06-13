# 基于改进 YOLO 的 VisDrone 无人机航拍小目标检测系统

针对无人机航拍场景中目标尺度小、分布密集、遮挡严重、类别外观相近，导致轻量化 YOLO 模型容易出现漏检和误检的问题，本项目提出并实现了一个基于改进 YOLO11n 的 VisDrone 小目标检测系统。

项目以 Ultralytics YOLO11n 为基线，从三个方面提升航拍小目标检测能力：一是在检测头中引入 P2 高分辨率小目标检测分支，增强浅层空间细节利用；二是在特征融合结构中加入 CoordAttention 注意力模块，提高位置敏感特征表达；三是采用 960 输入分辨率和小目标友好数据增强策略，提升小目标在输入图像和特征图中的有效像素占比。

系统完成了 VisDrone2019-DET 数据转换、YOLO 格式数据校验、baseline 训练、改进模型训练、消融实验、模型复杂度统计、推理速度测试、图片/视频推理、Flask Web 可视化检测页面和论文材料整理。当前数据集包含 6,471 张训练图像、548 张验证图像和 343,204 个训练标注框，覆盖 pedestrian、people、car、motor 等 10 类航拍目标。

在 100 epoch 训练设置下，YOLO11n-P2-CoordAttention-960 在 VisDrone 验证集上的 Best mAP50 达到 `0.41996`，Best mAP50-95 达到 `0.25174`，相比 YOLO11n baseline 分别提升 `0.09843` 和 `0.06936`；当前单图 wall-clock 推理速度测试为 `19.68 FPS`。项目最终形成了一个可复现、可评估、可展示，并可支撑中文期刊论文写作的无人机航拍小目标检测实验闭环。

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
| YOLO11n | baseline | 640 | 0.32153 | 0.18238 | 24.94 |
| YOLO11n-P2 | P2 high-resolution detection head | 640 | 0.33013 | 0.19012 | 22.91 |
| YOLO11n-P2-CoordAttention | P2 + CoordAttention | 640 | 0.33073 | 0.19044 | 21.85 |
| YOLO11n-P2-CoordAttention-960 | input size 960 | 960 | 0.41996 | 0.25174 | 19.68 |
| YOLO11n-P2-CoordAttention-SmallObjAug | small-object-friendly augmentation | 640 | 0.32780 | 0.18699 | 20.02 |

实验表明，P2 高分辨率检测分支能够提升浅层细节利用能力，CoordAttention 在 P2 基础上带来一定增益，而 960 输入分辨率是当前实验中最主要的性能提升来源。小目标友好增强相较 baseline 有提升，但低于 P2 和 CoordAttention 结构改进模型。

小目标尺度分析结果如下，统计口径采用 small `<32^2`、medium `32^2-96^2`、large `>=96^2` 的目标框面积划分：

| Split | Small | Medium | Large | Small Ratio |
| --- | ---: | ---: | ---: | ---: |
| train | 207604 | 116620 | 18980 | 60.49% |
| val | 26586 | 11105 | 1068 | 68.59% |

在 `conf=0.25`、`IoU=0.5` 的验证集匹配分析下，YOLO11n-P2-CoordAttention-960 的 small 目标召回率为 `0.45509`，高于 YOLO11n baseline 的 `0.30768`；该统计用于分析不同尺度目标的检测匹配情况，不等同于官方 AP。

外部参考基线结果如下，用于辅助分析不同 YOLO 版本和模型容量下的精度-速度关系，不作为 YOLO11n 改进模块的单因素消融：

| Model | Input | Params/M | Best mAP50 | Best mAP50-95 | FPS |
| --- | ---: | ---: | ---: | ---: | ---: |
| YOLOv8n baseline | 640 | 3.013 | 0.32520 | 0.18386 | 23.65 |
| YOLO11s baseline | 640 | 9.432 | 0.38937 | 0.22719 | 25.66 |

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

论文相关材料集中整理在 `paper/` 目录：

```text
paper/README.md
paper/CEA_JOURNAL_MASTER_PLAN.md
paper/CEA_REVIEWER_RESPONSE_PREP.md
paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md
paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md
paper/PROJECT_ROADMAP.md
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
paper/submission_audit_dashboard.md
paper/evidence_audit.md
paper/commands.md
paper/figures/
paper/tables/
```

其中 `paper/manuscript_submission_candidate.pdf` 是当前 LaTeX 预览版本，`paper/CEA_REVIEWER_RESPONSE_PREP.md` 整理审稿问题应答准备，`paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md` 汇总投稿材料包，`paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md` 记录最终提交前人工核对项，`paper/submission_audit_dashboard.md` 汇总审计状态，`paper/commands.md` 记录复现实验命令，`paper/evidence_audit.md` 记录论文数值来源。

编译 LaTeX PDF：

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

## 结果可复现说明

论文和 README 中的实验数值均来自真实训练日志、验证输出和 `paper/tables/` 汇总文件。项目保留训练、验证、测速、类别级指标收集和论文表格导出脚本，便于复现实验流程和继续扩展对比实验。

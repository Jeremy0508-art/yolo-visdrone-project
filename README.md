# 基于改进 YOLO 的 VisDrone 无人机航拍小目标检测项目

本仓库围绕 VisDrone2019-DET 无人机航拍目标检测任务，整理了一个从数据转换、模型训练、验证评估、推理展示到论文材料生成的 YOLO 小目标检测项目。当前主线以 Ultralytics YOLO11n 为基线，已完成 YOLO11n、YOLO11n-P2、YOLO11n-P2-CoordAttention、YOLO11n-P2-CoordAttention-960 和 YOLO11n-P2-CoordAttention-SmallObjAug 的验证集实验整理。

项目正在向中文会议/小论文方向推进。论文材料集中放在 [`paper/`](paper/README.md)，包括 LaTeX 稿件、PDF 预览、表格、图表、实验命令、证据审计和路线图。所有论文中使用的指标都必须来自真实训练日志、验证输出、`paper/tables/` 或官方评测结果，不编造数值。

## 当前状态

| 模块 | 状态 |
| --- | --- |
| VisDrone 数据转换与校验 | 已完成，数据集不随 GitHub 上传 |
| YOLO11n 主线实验 | 已完成 5 组本地验证集实验 |
| 表格、图表、速度、类别级指标 | 已整理到 `paper/` |
| LaTeX/PDF 论文预览 | 已生成 `paper/manuscript_submission_candidate.pdf` |
| VisDrone test-dev 官方评测 | 本地提交包曾准备，官方账号验证未完成，暂无官方 AP |
| 外部对照实验 | 服务器补跑中，完成前不写入论文结论 |

当前已完成实验中，`YOLO11n-P2-CoordAttention-960` 在 VisDrone 验证集上取得最佳结果：Best mAP50 为 `0.41996`，Best mAP50-95 为 `0.25174`，单图 wall-clock 推理速度为 `56.39 FPS`。这些数值来自已有 `runs/` 结果和 `paper/tables/` 汇总文件。

## 仓库结构

```text
.
├── configs/                  # 数据集、模型结构、训练配置
│   ├── dataset/visdrone.yaml
│   ├── models/yolo11n_p2.yaml
│   ├── models/yolo11n_p2_coordatt.yaml
│   └── train/
├── data/                     # 本地数据目录，GitHub 不上传
├── paper/                    # 论文材料、表格、图表、PDF 和路线图
├── runs/                     # 本地训练/验证/推理输出，GitHub 不上传
├── scripts/                  # 数据转换与检查脚本
├── src/                      # 可复用数据、模型和工具模块
├── tools/                    # 训练、验证、推理、论文表格导出脚本
├── web/                      # Flask Web 检测页面
├── weights/                  # 本地权重目录，GitHub 不上传
└── requirements.txt
```

## 环境安装

```powershell
pip install -r requirements.txt
```

推荐使用支持 CUDA 的 PyTorch 环境训练。CPU 可用于代码检查和部分推理，但训练速度会明显较慢。

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

当前本地数据检查结果：

| Split | Images | Boxes |
| --- | ---: | ---: |
| train | 6471 | 343204 |
| val | 548 | 38759 |
| test-dev | 1580 | 0 |

## 已完成主实验

| Model | Main Change | Input | Best mAP50 | Best mAP50-95 | FPS |
| --- | --- | ---: | ---: | ---: | ---: |
| YOLO11n | baseline | 640 | 0.32153 | 0.18238 | 72.54 |
| YOLO11n-P2 | P2 high-resolution detection head | 640 | 0.33013 | 0.19012 | 68.74 |
| YOLO11n-P2-CoordAttention | P2 + CoordAttention | 640 | 0.33073 | 0.19044 | 65.16 |
| YOLO11n-P2-CoordAttention-960 | input size 960 | 960 | 0.41996 | 0.25174 | 56.39 |
| YOLO11n-P2-CoordAttention-SmallObjAug | small-object-friendly augmentation | 640 | 0.32780 | 0.18699 | 64.81 |

详细结果来源：

```text
paper/tables/main_results.csv
paper/tables/ablation_results.csv
paper/tables/model_complexity.csv
paper/tables/speed_results.csv
paper/tables/per_class_results.csv
```

## 训练命令

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

新增外部 baseline 配置：

```powershell
python tools/train_baseline.py --config configs/train/baseline_yolov8n.yaml
python tools/train_baseline.py --config configs/train/baseline_yolo11s.yaml
```

其中 YOLOv8n/YOLO11s 等外部对照实验用于增强论文说服力。只有在完整训练、验证和表格导出完成后，相关指标才会进入论文正文。

## 验证、速度和论文表格

验证模型：

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt --data configs/dataset/visdrone.yaml --imgsz 960 --batch 4 --device 0
```

导出论文表格：

```powershell
python tools/export_paper_tables.py
```

测速：

```powershell
python tools/benchmark_speed.py --warmup 10 --samples 100 --output paper/tables/speed_results.csv
```

收集类别级指标：

```powershell
python tools/collect_per_class_metrics.py
```

更多可复现实验命令见 [`paper/commands.md`](paper/commands.md)。

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

## 论文材料

论文工作区入口：

```text
paper/README.md
paper/PROJECT_ROADMAP.md
paper/manuscript_submission_candidate.tex
paper/manuscript_submission_candidate.pdf
paper/evidence_audit.md
paper/submission_checklist.md
```

推荐使用 TeX Live 或 MiKTeX 编译 LaTeX PDF：

```powershell
cd paper
xelatex manuscript_submission_candidate.tex
xelatex manuscript_submission_candidate.tex
```

如果本地已经有 `.tools/tectonic/tectonic.exe` 轻量构建工具，也可以使用：

```powershell
cd paper
..\.tools\tectonic\tectonic.exe manuscript_submission_candidate.tex
```

## GitHub 上传范围

GitHub 仓库保留代码、配置、论文材料、表格和必要图表。以下内容不会上传：

- VisDrone 原始数据和转换后的 YOLO 数据；
- `runs/` 训练、验证、推理输出；
- `weights/` 权重文件和 `.pt` 文件；
- 服务器上传用的 `.zip`、`.tar` 和分片文件；
- 本地 LaTeX 编译中间文件；
- `.tools/` 下的本地 Tectonic 可执行文件。

这样可以保证仓库可读、可复现，同时避免上传超大文件或数据集版权相关内容。

## 当前论文结论边界

当前论文只报告 VisDrone 验证集结果，不报告官方 test-dev/test-challenge AP。外部 baseline 和更多对照实验正在补充中，完成前不会写入论文结论。本文不宣称 SOTA，当前定位是一个证据可追溯、流程可复现的无人机航拍小目标检测改进实验。

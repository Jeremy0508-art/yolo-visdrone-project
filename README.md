# 基于改进 YOLO 的 VisDrone 无人机航拍小目标检测系统

本项目面向 VisDrone 图像目标检测任务，构建一个可复现实验、可扩展改进模块、可部署 Web 演示的 YOLO 小目标检测工程。当前已经完成数据转换、baseline 训练、ECA 注意力消融、P2 小目标检测层消融、图片/视频推理脚本，以及 Flask 上传检测页面。

## 项目结构

```text
.
├── configs/                 # 数据集、模型结构、训练配置
│   ├── dataset/visdrone.yaml
│   ├── models/yolo11n_eca.yaml
│   ├── models/yolo11n_p2.yaml
│   └── train/
├── data/
│   ├── raw/VisDrone/         # VisDrone 原始数据
│   └── processed/            # 转换后的 YOLO 格式数据
├── experiments/              # 实验记录、消融结果、报告材料
├── runs/                     # Ultralytics 训练、验证、推理输出
├── scripts/                  # 数据集转换与检查脚本
├── src/                      # 可复用模块
│   ├── datasets/
│   ├── models/
│   └── utils/
├── tools/                    # 训练、验证、推理入口脚本
├── web/                      # Flask Web 检测页面
├── weights/                  # 兼容保存的模型权重目录
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

本项目使用 VisDrone 的图像目标检测任务，也就是 `VisDrone2019-DET`，不需要下载跟踪或视频检测任务。

原始数据应放在：

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

当前数据检查结果：

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

训练 ECA 注意力改进模型：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_eca.yaml
```

训练 P2 小目标检测层改进模型：

```powershell
python tools/train_baseline.py --config configs/train/yolo11n_p2.yaml
```

验证模型：

```powershell
python tools/val.py --weights runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt --data configs/dataset/visdrone.yaml
```

## 推理

图片检测：

```powershell
python tools/detect_image.py --weights runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt --source data/processed/visdrone_yolo/images/val --save-dir runs/detect_image/p2_val_samples
```

视频检测：

```powershell
python tools/detect_video.py --weights runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt --source path/to/video.mp4 --save-dir runs/detect_video/p2_video
```

## Web 演示

启动 Flask 页面：

```powershell
python web/app.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

Web 页面默认使用当前效果最好的 P2 模型：

```text
runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt
```

支持上传图片或视频，并在页面中展示检测结果。

## 当前实验结果

| Model | Main Change | Precision | Recall | mAP50 | mAP50-95 |
| --- | --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 原始 YOLO11n | 0.45440 | 0.33922 | 0.31985 | 0.18066 |
| YOLO11n-ECA | P3/P4/P5 加入 ECA 注意力 | 0.43047 | 0.32856 | 0.30236 | 0.17121 |
| YOLO11n-P2 | 增加 P2 小目标检测层 | 0.44771 | 0.35475 | 0.32695 | 0.18689 |

最佳指标对比：

| Model | Best mAP50 | Epoch | Best mAP50-95 | Epoch |
| --- | ---: | ---: | ---: | ---: |
| YOLO11n baseline | 0.32153 | 80 | 0.18238 | 79 |
| YOLO11n-ECA | 0.30417 | 78 | 0.17239 | 88 |
| YOLO11n-P2 | 0.33013 | 86 | 0.19012 | 89 |

当前结论：单独加入 ECA 在现有训练设置下没有带来提升；增加 P2 小目标检测层提升了 mAP50 和 mAP50-95，更适合作为后续系统演示和进一步改进的主模型。

## 实验材料

核心实验记录位于：

```text
experiments/baseline/
experiments/ablations/
```

重点文档：

```text
experiments/baseline/baseline_yolo11n_visdrone_summary.md
experiments/ablations/yolo11n_eca_pretrained_adamw_visdrone_summary.md
experiments/ablations/yolo11n_p2_pretrained_visdrone_summary.md
experiments/ablations/ablation_summary.md
```

报告与答辩材料：

```text
experiments/report_outline.md
experiments/presentation_outline.md
experiments/demo_checklist.md
experiments/visual_assets.md
experiments/case_study.md
```

后续建议实验：

- P2 + ECA 组合改进，验证注意力机制在高分辨率检测头下是否有效。
- 尝试更大输入尺寸，例如 `imgsz=960`，进一步改善小目标检测。
- 针对 VisDrone 调整数据增强策略，例如 mosaic 关闭时机、scale 范围、copy-paste 等。

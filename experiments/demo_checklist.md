# 演示检查清单

本清单用于答辩或项目展示前快速确认系统状态。

## 1. 环境检查

```powershell
pip install -r requirements.txt
```

确认核心依赖：

- ultralytics
- opencv-python
- flask
- PyYAML
- Pillow

一键项目自检：

```powershell
python tools/verify_project.py
```

如果用于答辩前最终检查，可以使用严格模式：

```powershell
python tools/verify_project.py --strict
```

## 2. 数据检查

原始 VisDrone DET 数据应放在：

```text
data/raw/VisDrone/
├── VisDrone2019-DET-train/
├── VisDrone2019-DET-val/
└── VisDrone2019-DET-test-dev/
```

转换后数据：

```text
data/processed/visdrone_yolo/
```

检查命令：

```powershell
python scripts/check_dataset.py --dataset-root data/processed/visdrone_yolo
```

## 3. 权重检查

答辩演示推荐使用：

```text
runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt
```

该模型是当前实验中表现最好的 P2 + CoordAttention 改进模型。

## 4. 图片推理检查

```powershell
python tools/detect_image.py --weights runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt --source data/processed/visdrone_yolo/images/val --save-dir runs/detect_image/p2_coordatt_val_samples
```

结果目录：

```text
runs/detect_image/p2_coordatt_val_samples
```

## 5. Web 演示检查

启动：

```powershell
python web/app.py
```

访问：

```text
http://127.0.0.1:5000
```

演示步骤：

1. 打开 Web 页面。
2. 上传一张 VisDrone 验证集图片。
3. 设置置信度阈值，例如 0.25。
4. 点击检测。
5. 展示输出结果。

推荐测试图片：

```text
experiments/cases/selected_original/0000360_06861_d_0000748.jpg
experiments/cases/selected_original/0000295_02900_d_0000034.jpg
experiments/cases/selected_original/0000001_04527_d_0000008.jpg
```

## 6. 报告材料位置

核心文档：

```text
README.md
experiments/report_outline.md
experiments/presentation_outline.md
experiments/visual_assets.md
experiments/case_study.md
```

核心图表：

```text
experiments/figures/
experiments/cases/p2_case_contact_sheet.jpg
```

## 7. 常见问题回答

为什么使用 VisDrone DET？

VisDrone DET 是图像目标检测任务，和本项目“航拍图像小目标检测”目标一致；跟踪和视频任务不是当前阶段必须的数据。

为什么 P2 有效？

P2 检测头利用更高分辨率浅层特征，有助于保留小目标细节，因此更适合 VisDrone 航拍小目标场景。

Web 页面展示的是什么模型？

默认使用 `runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt`。

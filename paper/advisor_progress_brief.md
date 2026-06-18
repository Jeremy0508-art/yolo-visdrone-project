# 导师汇报简版

本文档由 `tools/build_advisor_progress_brief.py` 生成，用于向导师简要说明 YOLO VisDrone 项目从工程实现推进到《计算机工程与应用》投稿准备的当前状态。它是汇报材料，不是论文正文；所有论文数值仍以 `paper/tables/`、训练日志、验证输出和审计文件为准。

## 1. 研究目标

本项目围绕 VisDrone2019-DET 无人机航拍目标检测任务，关注小目标占比高、目标密集、遮挡频繁和类别外观相似等问题。当前论文主线是以 Ultralytics YOLO11n 为轻量基线，评估 P2 高分辨率检测分支、CoordAttention、960 输入分辨率和小目标友好增强策略对检测精度、速度和复杂度的影响。

## 2. 已完成实验和材料

- 已完成 100 epoch 本地训练/验证的模型数：12。
- YOLOv8n baseline：imgsz=640，best mAP50=0.32520，best mAP50-95=0.18386，结果目录 `runs/detect/baseline_yolov8n_visdrone`。
- YOLOv5n baseline：imgsz=640，best mAP50=0.31030，best mAP50-95=0.17513，结果目录 `runs/detect/baseline_yolov5n_visdrone`。
- YOLOv8n baseline 960：imgsz=960，best mAP50=0.42016，best mAP50-95=0.25121，结果目录 `runs/detect/baseline_yolov8n_960_visdrone`。
- YOLO11s baseline：imgsz=640，best mAP50=0.38937，best mAP50-95=0.22719，结果目录 `runs/detect/baseline_yolo11s_visdrone`。
- YOLO11s baseline 960：imgsz=960，best mAP50=0.48901，best mAP50-95=0.29812，结果目录 `runs/detect/baseline_yolo11s_960_visdrone`。
- YOLO11n baseline：imgsz=640，best mAP50=0.32153，best mAP50-95=0.18238，结果目录 `runs/detect/baseline_yolo11n_visdrone`。
- YOLO11n baseline 960：imgsz=960，best mAP50=0.42136，best mAP50-95=0.25067，结果目录 `runs/detect/baseline_yolo11n_960_visdrone`。
- YOLO11n-P2：imgsz=640，best mAP50=0.33013，best mAP50-95=0.19012，结果目录 `runs/detect/yolo11n_p2_pretrained_visdrone`。
- YOLO11n-P2-960：imgsz=960，best mAP50=0.42361，best mAP50-95=0.25552，结果目录 `runs/detect/yolo11n_p2_960_visdrone`。
- YOLO11n-P2-CoordAttention：imgsz=640，best mAP50=0.33073，best mAP50-95=0.19044，结果目录 `runs/detect/yolo11n_p2_coordatt_visdrone`。
- YOLO11n-P2-CoordAttention-960：imgsz=960，best mAP50=0.41996，best mAP50-95=0.25174，结果目录 `runs/detect/yolo11n_p2_coordatt_960_visdrone_full`。
- YOLO11n-P2-CoordAttention-SmallObjAug：imgsz=640，best mAP50=0.32780，best mAP50-95=0.18699，结果目录 `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone`。

## 3. 当前核心结果

当前已完成实验中，`YOLO11s baseline 960` 取得最高验证精度，best mAP50=0.48901、best mAP50-95=0.29812，说明更大模型容量仍是提升 VisDrone 检测精度的重要因素。

在 nano 级轻量模型中，`YOLO11n-P2-960` 取得 best mAP50=0.42361、best mAP50-95=0.25552。与 `YOLO11n baseline` 的 best mAP50=0.32153、best mAP50-95=0.18238 相比，分别提升 10.21 个百分点 和 7.31 个百分点。该结果支持把论文主张定位为轻量模型中的精度-速度-参数量折中，而不是对大容量模型的全面超越。

## 4. 小目标证据

- VisDrone YOLO 格式标注统计显示：训练集 small 目标占比 60.49%，验证集 small 目标占比 68.59%。
- 在 `conf=0.25`、`IoU=0.5` 的尺度分组匹配分析中，YOLO11n baseline 的 small 目标 recall 为 0.307681；YOLO11n-P2-CoordAttention-960 的 small 目标 recall 为 0.455089。
- 上述尺度分组结果用于分析不同尺度目标的匹配情况，不等同于官方 AP。

## 5. 服务器公平对比实验

为回答审稿人最可能追问的公平性问题，服务器补跑的 YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960、YOLOv5n-640 已达到 100 epoch 并同步到本地证据链。
- 最近服务器状态时间：2026-06-16 13:16:44 +08:00
- 当前 YOLO11n-960 状态：READY，100/100 epoch
- 训练进程：`STOPPED pid=43554`
- 所有进入论文结果表的公平对比数值均来自本地 `runs/`、训练日志和 `paper/tables/` 汇总文件。

## 6. 投稿准备状态

- 当前审计仪表盘：共 34 个报告，30 ready，0 partial，4 pending，0 missing。
- 已建立 LaTeX/PDF、图表、复现命令、证据审计、参考文献核验、投稿风险登记表和服务器状态追踪。
- 当前核心阻塞已从实验训练转为期刊投稿前人工检查，包括官方模板、作者信息、最终 PDF 目视检查和投稿材料包整理。

## 7. 给导师的风险说明

- 不建议使用“全面领先主流 YOLO”这类绝对表述。
- YOLO11s-960 精度最高，论文应明确其作为容量上限参考。
- YOLO11n-P2-960 是当前 nano 级轻量模型中较好的折中点，应强调参数规模、速度和精度之间的平衡。
- CoordAttention 在 960 输入下未超过 P2-960，论文中应把它解释为辅助设计和负向/边界结果，而不是决定性增益来源。

## 8. 下一步

1. 按 `paper/CEA_RESULT_INTERPRETATION_MATRIX.md` 完成投稿版结果讨论和结论边界打磨。
2. 对照《计算机工程与应用》模板做版式、篇幅、参考文献和图表源文件检查。
3. 完成最终 PDF 目视检查，确认图表浮动、页码、引用和数值追溯。
4. 整理投稿材料包和 GitHub 展示页，再提交给导师审阅。

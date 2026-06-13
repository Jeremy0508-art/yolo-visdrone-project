# 导师汇报简版

本文档由 `tools/build_advisor_progress_brief.py` 生成，用于向导师简要说明 YOLO VisDrone 项目从工程实现推进到《计算机工程与应用》投稿准备的当前状态。它是汇报材料，不是论文正文；所有论文数值仍以 `paper/tables/`、训练日志、验证输出和审计文件为准。

## 1. 研究目标

本项目围绕 VisDrone2019-DET 无人机航拍目标检测任务，关注小目标占比高、目标密集、遮挡频繁和类别外观相似等问题。当前论文主线是以 Ultralytics YOLO11n 为轻量基线，评估 P2 高分辨率检测分支、CoordAttention、960 输入分辨率和小目标友好增强策略对检测精度、速度和复杂度的影响。

## 2. 已完成实验和材料

- 已完成 100 epoch 本地训练/验证的模型数：7。
- YOLOv8n baseline：imgsz=640，best mAP50=0.32520，best mAP50-95=0.18386，结果目录 `runs/detect/baseline_yolov8n_visdrone`。
- YOLO11s baseline：imgsz=640，best mAP50=0.38937，best mAP50-95=0.22719，结果目录 `runs/detect/baseline_yolo11s_visdrone`。
- YOLO11n baseline：imgsz=640，best mAP50=0.32153，best mAP50-95=0.18238，结果目录 `runs/detect/baseline_yolo11n_visdrone`。
- YOLO11n-P2：imgsz=640，best mAP50=0.33013，best mAP50-95=0.19012，结果目录 `runs/detect/yolo11n_p2_pretrained_visdrone`。
- YOLO11n-P2-CoordAttention：imgsz=640，best mAP50=0.33073，best mAP50-95=0.19044，结果目录 `runs/detect/yolo11n_p2_coordatt_visdrone`。
- YOLO11n-P2-CoordAttention-960：imgsz=960，best mAP50=0.41996，best mAP50-95=0.25174，结果目录 `runs/detect/yolo11n_p2_coordatt_960_visdrone_full`。
- YOLO11n-P2-CoordAttention-SmallObjAug：imgsz=640，best mAP50=0.32780，best mAP50-95=0.18699，结果目录 `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone`。

## 3. 当前最强已完成模型

当前已完成实验中，`YOLO11n-P2-CoordAttention-960` 在 VisDrone 验证集上取得 best mAP50=0.41996、best mAP50-95=0.25174。与 `YOLO11n baseline` 的 best mAP50=0.32153、best mAP50-95=0.18238 相比，分别提升 9.84 个百分点 和 6.94 个百分点。

需要注意：这一结论目前只说明当前已完成实验中的表现。由于 960 输入分辨率本身可能贡献较大，最终论文结论必须等待 YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960 等公平对比实验完成后再定稿。

## 4. 小目标证据

- VisDrone YOLO 格式标注统计显示：训练集 small 目标占比 60.49%，验证集 small 目标占比 68.59%。
- 在 `conf=0.25`、`IoU=0.5` 的尺度分组匹配分析中，YOLO11n baseline 的 small 目标 recall 为 0.307681；YOLO11n-P2-CoordAttention-960 的 small 目标 recall 为 0.455089。
- 上述尺度分组结果用于分析不同尺度目标的匹配情况，不等同于官方 AP。

## 5. 服务器公平对比实验

为回答审稿人最可能追问的公平性问题，服务器正在按队列补跑以下实验：YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960、YOLOv5n-640。
- 最近服务器状态时间：2026-06-14 03:21:28 +08:00
- 当前 YOLO11n-960 状态：PARTIAL，43/100 epoch
- 训练进程：`43554 Rl      05:19:58 99.9`
- 未完成 100 epoch 的服务器结果只作为进度信息，不能进入论文结果表、摘要或结论。

## 6. 投稿准备状态

- 当前审计仪表盘：共 23 个报告，17 ready，1 partial，5 pending，0 missing。
- 已建立 LaTeX/PDF、图表、复现命令、证据审计、参考文献核验、投稿风险登记表和服务器状态追踪。
- 当前核心阻塞仍是公平对比实验尚未全部完成；实验完成后需要同步完整日志和结果、重建表格、补测速度/复杂度，并按结果解释矩阵重写摘要、结果分析和结论。

## 7. 给导师的风险说明

- 目前不建议使用“全面优于主流 YOLO”这类绝对表述。
- 如果 YOLO11n-960 接近主方法，论文应强调高分辨率输入是主要贡献来源，P2/CA 是结构补充。
- 如果 YOLO11s-960 更强，论文应转向轻量化折中、参数效率和部署成本分析。
- 如果新增对照结果整体不支持方法优势，论文仍可转为系统评估和实证分析型稿件，但必须如实呈现负结果。

## 8. 下一步

1. 等服务器公平对比实验完成 100 epoch。
2. 用 `tools/sync_cea_server_results.ps1 -MinEpochs 100` 同步完整结果。
3. 重新生成 `paper/tables/`、速度/复杂度/尺度分析和审计报告。
4. 按 `paper/CEA_RESULT_INTERPRETATION_MATRIX.md` 重写论文主张。
5. 编译 PDF，检查排版、引用、图表和数值追溯后再给导师审阅。

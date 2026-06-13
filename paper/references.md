# 参考文献候选清单

本文档用于《计算机工程与应用》期刊稿的参考文献整理。正式投稿前需要按期刊要求统一为 GB/T 7714 或编辑部指定格式，并逐条核对作者、题名、期刊/会议、年份、卷期页码和 DOI。

## 已核验基础文献

以下文献或文档已有明确来源链接，可优先用于当前稿件：

[1] Du D, Zhu P, Wen L, et al. VisDrone-DET2019: The Vision Meets Drone Object Detection in Image Challenge[C]//Proceedings of the IEEE/CVF International Conference on Computer Vision Workshops. 2019.

[2] Hou Q, Zhou D, Feng J. Coordinate Attention for Efficient Mobile Network Design[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2021: 13713-13722.

[3] Khanam R, Hussain M. YOLOv11: An Overview of the Key Architectural Enhancements[EB/OL]. arXiv:2410.17725, 2024.

[4] Ultralytics. YOLO11 Documentation[EB/OL]. https://docs.ultralytics.com/models/yolo11/.

[5] Ultralytics. VisDrone Dataset Documentation[EB/OL]. https://docs.ultralytics.com/datasets/detect/visdrone/.

## 近年相关工作候选

以下文献方向与本文高度相关，适合支撑相关工作和讨论部分。正式引用前仍需核验题录格式。

| 方向 | 候选文献 | 与本文关系 | 核验状态 |
| --- | --- | --- | --- |
| UAV 小目标 YOLO | SOD-YOLO: Small-object-detection algorithm based on improved YOLOv8 for UAV images | 轻量 YOLOv8、小目标、无人机图像 | 已找到开放页面，待核验正式题录 |
| UAV 小目标 P2 分支 | BPD-YOLO: lightweight UAV small-object detection with deep semantic integration | 与 P2、高分辨率特征和轻量化检测高度相关 | 已找到开放页面，待核验正式题录 |
| 航拍轻量检测 | LPAE-YOLOv8: lightweight aerial small object detection | 与轻量化小目标检测头和注意力机制相关 | 已找到开放页面，待核验正式题录 |
| 遥感小目标 YOLO | OD-YOLO: robust small object detection model in remote sensing images | 与多尺度特征融合和 YOLOv8n 小目标检测相关 | 已找到开放页面，待核验正式题录 |
| 小目标 P2 检测头 | SMA-YOLO or similar P2-head UAV/remote-sensing detectors | 可支撑 P2 检测头的合理性 | 已找到开放页面，待核验正式题录 |
| 注意力机制 | SE, CBAM, SimAM, Coordinate Attention | 用于说明注意力机制发展脉络 | 需要补齐经典文献 |
| 多尺度融合 | FPN, PANet, BiFPN, AFPN/GFPN 等 | 用于说明多尺度特征融合背景 | 需要补齐经典文献 |

## 正文引用建议

- 引言中介绍 VisDrone 数据集和无人机检测挑战时引用 [1]。
- 实验设置中说明 VisDrone 数据组织和类别背景时引用 [1] 与 [5]。
- 相关工作中介绍 YOLO11/YOLOv11 架构背景时引用 [3] 与 [4]。
- 方法中介绍 CoordAttention 的位置编码注意力机制时引用 [2]。
- 相关工作中讨论 UAV 小目标检测和 P2 检测头时，引用 SOD-YOLO、BPD-YOLO、LPAE-YOLOv8、OD-YOLO 等近年工作，正式引用前以 `paper/reference_verification_matrix.md` 为准。

## 当前缺口

正式期刊稿建议最终参考文献达到 25-35 篇，其中近三年相关文献不少于 12 篇。当前还需要补齐：

1. YOLO 系列核心文献和综述。
2. 无人机航拍检测文献。
3. 小目标检测和尺度增强文献。
4. 多尺度特征融合经典文献。
5. 注意力机制经典文献。
6. 近三年中文学术论文中与改进 YOLO、小目标检测、无人机检测相关的研究。

## 来源链接

- VisDrone-DET2019 paper: https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Du_VisDrone-DET2019_The_Vision_Meets_Drone_Object_Detection_in_Image_Challenge_ICCVW_2019_paper.pdf
- Coordinate Attention paper: https://openaccess.thecvf.com/content/CVPR2021/papers/Hou_Coordinate_Attention_for_Efficient_Mobile_Network_Design_CVPR_2021_paper.pdf
- Coordinate Attention arXiv page: https://arxiv.org/abs/2103.02907
- YOLOv11 overview: https://arxiv.org/abs/2410.17725
- Ultralytics YOLO11 docs: https://docs.ultralytics.com/models/yolo11/
- Ultralytics VisDrone docs: https://docs.ultralytics.com/datasets/detect/visdrone/
- SOD-YOLO open page: https://pmc.ncbi.nlm.nih.gov/articles/PMC11514239/
- BPD-YOLO open page: https://pmc.ncbi.nlm.nih.gov/articles/PMC12397394/
- LPAE-YOLOv8 open page: https://pmc.ncbi.nlm.nih.gov/articles/PMC12749428/
- OD-YOLO open page: https://www.mdpi.com/1424-8220/24/11/3596

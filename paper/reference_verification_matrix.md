# Reference Verification Matrix

This matrix tracks candidate references for the 《计算机工程与应用》 journal manuscript. A reference should be moved into the final manuscript only after its bibliographic metadata has been checked against the official publisher, arXiv, CVF Open Access, or another reliable academic page.

## Verified Core Sources

| ID | Topic | Source | URL | Manuscript Use | Status |
| --- | --- | --- | --- | --- | --- |
| R01 | VisDrone benchmark | VisDrone-DET2019 ICCV Workshop paper | https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Du_VisDrone-DET2019_The_Vision_Meets_Drone_Object_Detection_in_Image_Challenge_ICCVW_2019_paper.pdf | Dataset motivation and benchmark description | Verified source link |
| R02 | Coordinate attention | Coordinate Attention for Efficient Mobile Network Design, CVPR 2021 | https://openaccess.thecvf.com/content/CVPR2021/papers/Hou_Coordinate_Attention_for_Efficient_Mobile_Network_Design_CVPR_2021_paper.pdf | Method background for CoordAttention | Verified source link |
| R03 | Coordinate attention | Coordinate Attention arXiv page | https://arxiv.org/abs/2103.02907 | Cross-check title/authors and mechanism summary | Verified source link |
| R04 | YOLO11 framework | Ultralytics YOLO11 documentation | https://docs.ultralytics.com/models/yolo11/ | Framework/model-family background | Official documentation |
| R05 | VisDrone data config | Ultralytics VisDrone documentation | https://docs.ultralytics.com/datasets/detect/visdrone/ | Dataset organization and class context | Official documentation |
| R06 | YOLO11 overview | YOLOv11: An Overview of the Key Architectural Enhancements | https://arxiv.org/abs/2410.17725 | YOLO11 architecture context, if retained | arXiv source; still verify final citation style |
| R07 | YOLO lineage | You Only Look Once: Unified, Real-Time Object Detection | https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html | YOLO series background | CVF source link |
| R08 | YOLO lineage | YOLOv3: An Incremental Improvement | https://arxiv.org/abs/1804.02767 | YOLO series background | arXiv source |
| R09 | Multi-scale fusion | Feature Pyramid Networks for Object Detection | https://openaccess.thecvf.com/content_cvpr_2017/papers/Lin_Feature_Pyramid_Networks_CVPR_2017_paper.pdf | Multi-scale feature fusion background | CVF source link |
| R10 | Multi-scale fusion | Path Aggregation Network for Instance Segmentation | https://openaccess.thecvf.com/content_cvpr_2018/papers/Liu_Path_Aggregation_Network_CVPR_2018_paper.pdf | Neck/path aggregation background | CVF source link |
| R11 | Attention module | Squeeze-and-Excitation Networks | https://openaccess.thecvf.com/content_cvpr_2018/html/Hu_Squeeze-and-Excitation_Networks_CVPR_2018_paper.html | Channel attention background | CVF source link |
| R12 | Attention module | CBAM: Convolutional Block Attention Module | https://openaccess.thecvf.com/content_ECCV_2018/papers/Sanghyun_Woo_Convolutional_Block_Attention_ECCV_2018_paper.pdf | Channel/spatial attention background | CVF source link |

## UAV and Small-Object YOLO Candidates

| ID | Topic | Candidate Source | URL | Why It Matters | Status |
| --- | --- | --- | --- | --- | --- |
| C01 | UAV small-object detection | SOD-YOLO: Small-object-detection algorithm based on improved YOLOv8 for UAV images | https://pmc.ncbi.nlm.nih.gov/articles/PMC11514239/ | Recent YOLOv8-based UAV small-object work; useful for related work and comparison framing | Open page found; verify formal citation |
| C02 | P2/high-resolution UAV detection | BPD-YOLO: lightweight small object detection for UAV images based on deep semantic integration | https://pmc.ncbi.nlm.nih.gov/articles/PMC12397394/ | Related to P2/high-resolution feature extraction and lightweight detection | Open page found; verify formal citation |
| C03 | Lightweight aerial small-object detection | LPAE-YOLOv8: lightweight aerial small object detection via LSE and PPE | https://pmc.ncbi.nlm.nih.gov/articles/PMC12749428/ | Related to lightweight aerial detection, small-object heads, and attention | Open page found; verify formal citation |
| C04 | Remote-sensing small-object detection | OD-YOLO: robust small object detection model in remote sensing images | https://www.mdpi.com/1424-8220/24/11/3596 | Related to YOLOv8n, multi-scale feature fusion, remote-sensing small objects | Publisher page found; verify formal citation |
| C05 | P2 detection head | SMA-YOLO with additional P2 detection head for small objects | https://www.mdpi.com/2072-4292/17/14/2421 | Supports the rationale for P2 small-object heads in aerial/remote-sensing tasks | Publisher page found; verify formal citation |
| C06 | Tiny-object detection | LE-YOLO lightweight and efficient tiny-object detection | https://www.mdpi.com/2504-446X/8/7/276 | Helps frame lightweight tiny-object detection and deployment trade-off | Publisher page found; verify formal citation |
| C07 | Attention-based lightweight YOLO | TA-YOLO lightweight small-object model with multidimensional attention | https://link.springer.com/article/10.1007/s40747-024-01448-6 | Related attention-based lightweight small-object work | Publisher page found; verify access/citation |

## Still Needed

| Area | Needed References | Notes |
| --- | --- | --- |
| YOLO core lineage | YOLOv5/YOLOv8/YOLO11 or authoritative docs/papers | Avoid overloading the paper with model history; cite only what supports method choice |
| Multi-scale fusion | FPN, PANet, BiFPN, GFPN/AFPN if discussed | Needed if related work expands multi-scale feature fusion |
| Attention modules | SE, CBAM, SimAM, CoordAttention | Needed to position CoordAttention fairly |
| Chinese journal references | Recent Chinese improved-YOLO target-detection papers | Prefer 《计算机工程与应用》 or similar Chinese journals, but verify title and metadata manually |
| Dense detection post-processing | NMS/Soft-NMS or dense-scene post-processing | Useful only if discussion expands post-processing limitations |

## Chinese Journal Candidates

These items were found through web search as relevant 《计算机工程与应用》 or adjacent Chinese-journal leads. They are useful for positioning, but must be verified against CNKI, Wanfang, the journal site, or an institutional database before entering the final bibliography.

| ID | Topic | Candidate Source | URL or Search Lead | Manuscript Use | Status |
| --- | --- | --- | --- | --- | --- |
| CJ01 | YOLO survey | 面向通用目标检测的YOLO方法研究综述，《计算机工程与应用》，2024，60(21):38-54 | https://dianda.cqvip.com/Qikan/Article/Detail?id=7113226431 | YOLO family related work and taxonomy | Search lead found; verify metadata |
| CJ02 | UAV YOLOv8 | 优化改进YOLOv8无人机视角下目标检测算法，《计算机工程与应用》相关引用条目 | https://front-sci.com/journal/article?doi=10.12238%2Facair.v3i1.11894 | UAV-view YOLO comparison framing | Search lead found; verify metadata |
| CJ03 | UAV small object YOLOv5 | 改进YOLOv5的无人机影像小目标检测算法，《计算机工程与应用》，2023，59(9):198-206 | https://search.ebscohost.com/login.aspx?AN=163829120 | UAV small-object writing and experiment matrix | Search lead found; verify metadata |
| CJ04 | UAV small object YOLOv8 | 改进YOLOv8的无人机航拍小目标检测算法，《计算机工程与应用》，2025年第11期检索条目 | https://cnki.istiz.org.cn/kcms/detail/detail.aspx?dbcode=CJFD&dbname=CJFD2025&filename=JSGG202511009 | Multi-scale fusion and lightweight UAV small-object positioning | Search lead found; verify metadata |
| CJ05 | Lightweight object detection | LMUAV-YOLOv8: low-altitude UAV lightweight network, 《计算机工程与应用》，2025，61(3):94-110 | Search result from PDF reference list | Lightweight UAV detection comparison | Search lead found; verify metadata |
| CJ06 | Improved YOLOv5 UAV small object | 改进YOLOv5的无人机小目标检测方法研究，《计算机工程与应用》，2024，60(10):276-284 | Search result from PDF reference list | Related work for UAV small targets | Search lead found; verify metadata |

## Rules

1. Do not copy literature-reported metrics into the main experiment table unless the training and evaluation protocol is identical.
2. If a literature number is mentioned, label it as a reported result from that paper.
3. Prefer official publisher pages, CVF Open Access, arXiv, or official documentation for metadata.
4. Keep non-peer-reviewed pages as search leads, not final references.
5. Re-check all capitalization before LaTeX/BibTeX export, especially terms such as YOLO, VisDrone, CoordAttention, P2, and UAV.

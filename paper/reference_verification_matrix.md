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

## Rules

1. Do not copy literature-reported metrics into the main experiment table unless the training and evaluation protocol is identical.
2. If a literature number is mentioned, label it as a reported result from that paper.
3. Prefer official publisher pages, CVF Open Access, arXiv, or official documentation for metadata.
4. Keep non-peer-reviewed pages as search leads, not final references.
5. Re-check all capitalization before LaTeX/BibTeX export, especially terms such as YOLO, VisDrone, CoordAttention, P2, and UAV.

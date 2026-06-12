# Literature Comparison Seed Table

This file collects related UAV/VisDrone small-object detection work for the next paper-strengthening phase. Literature metrics should not be mixed into our main result table unless the dataset split, training schedule, input size, and evaluation protocol are clearly comparable.

## Related Work Table

| Work | Base Model | Dataset Mentioned | Main Idea | Reported Direction | How It Helps Our Paper |
| --- | --- | --- | --- | --- | --- |
| VisDrone-DET2019 | Challenge benchmark | VisDrone2019-DET | UAV object detection benchmark and evaluation setting | Establishes dataset difficulty and task context | Dataset citation and motivation |
| CoordAttention | Mobile CNN attention | General vision benchmarks | Direction-aware coordinate attention | Lightweight attention with positional information | Justifies choosing CoordAttention |
| SOD-YOLO | YOLOv8 | VisDrone2019 | Improved feature fusion for UAV small objects | Reports mAP50 gain over YOLOv8 baselines | Shows our paper needs YOLOv8-family comparison |
| BPD-YOLO | YOLOv8n + P2 | VisDrone, TinyPerson | Deep semantic integration and lightweight FPN | Reports gains over YOLOv8n+P2 on VisDrone | Strongly related to our P2/high-resolution direction |
| LPAE-YOLOv8 | YOLOv8 | UAV aerial small objects | Lightweight small-object head and adaptive attention | Targets accuracy-background-model-size trade-off | Related to lightweight attention and head design |
| SL-YOLO | YOLO-family | UAV small-object scenes | Stronger/lighter YOLO for drone detection | Focuses on real-time small-object detection | Useful for framing accuracy-speed trade-off |
| DSSFF / dynamic scale-sequence fusion | YOLO-style aerial detector | VisDrone2019, DIOR | Extra small-target head and dynamic feature fusion | Reports gains from x-small target detection head | Supports our claim that shallow high-resolution heads help VisDrone |

## Literature Gaps to Address

Our current paper still needs to answer:

1. Is the proposed configuration stronger than common lightweight baselines such as YOLOv8n and YOLO11s under the same training protocol?
2. Is P2 the main source of the gain, or is the gain mostly from input size?
3. Does CoordAttention provide enough improvement to justify being included?
4. Is the accuracy-speed trade-off better than simply using a larger model?
5. Which VisDrone classes benefit most from the proposed configuration?

## Immediate Local Experiments Suggested

| Experiment | Config | Expected Output |
| --- | --- | --- |
| YOLOv8n baseline | `configs/train/baseline_yolov8n.yaml` | External lightweight YOLO baseline under our protocol |
| YOLO11s baseline | `configs/train/baseline_yolo11s.yaml` | Larger YOLO11 model comparison for accuracy-speed trade-off |
| Best model re-validation | existing 960 best weights | Confirm final reported best metrics after table updates |

## Source Links

- VisDrone-DET2019 paper: https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Du_VisDrone-DET2019_The_Vision_Meets_Drone_Object_Detection_in_Image_Challenge_ICCVW_2019_paper.pdf
- CoordAttention paper: https://openaccess.thecvf.com/content/CVPR2021/papers/Hou_Coordinate_Attention_for_Efficient_Mobile_Network_Design_CVPR_2021_paper.pdf
- SOD-YOLO: https://www.mdpi.com/2072-4292/16/16/3057
- BPD-YOLO: https://www.nature.com/articles/s41598-025-16878-6
- LPAE-YOLOv8: https://www.nature.com/articles/s41598-025-28741-9
- SL-YOLO: https://arxiv.org/html/2411.11477
- Dynamic scale-sequence fusion: https://arxiv.org/html/2406.12285

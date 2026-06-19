# IEEE Related Work Outline

Status: planning draft. This is not a final literature review.

Primary source table: `paper/ieee_related_work_matrix.csv`.

## 1. UAV Aerial Object Detection Datasets

Purpose in manuscript:
- Establish why UAV images differ from ground-view detection.
- Justify VisDrone as the primary dataset and UAVDT as the immediate second dataset.
- Support a T-ITS framing through traffic-related categories and aerial surveillance scenes.

Key sources to cite:
- VisDrone official dataset/challenge paper and official repository.
- UAVDT benchmark paper/project page.
- AU-AIR if the paper needs stronger traffic-surveillance context.
- HIT-UAV only as adjacent thermal UAV detection, not as a direct comparison.

Draft logic:
1. VisDrone provides a large UAV object detection benchmark with dense multi-class annotations and challenging scale/occlusion conditions.
2. UAVDT complements VisDrone with vehicle-oriented UAV traffic scenes, scene attributes, camera views, occlusion, and altitude variation.
3. AU-AIR is relevant to low-altitude traffic surveillance and multimodal UAV sensing, but should remain optional unless experiments are added.
4. These datasets motivate lightweight, scale-aware models that can handle dense small objects under deployment constraints.

Evidence boundary:
- Do not claim cross-dataset generalization until UAVDT experiments are complete.

## 2. Tiny and Small Object Detection

Purpose in manuscript:
- Explain why small objects need more than overall mAP.
- Motivate scale-wise AP/Recall and tiny-object-specific analysis.
- Place AI-TOD/AI-TOD-v2/TinyPerson as method motivation, not necessarily as core experiments.

Key sources to cite:
- AI-TOD / AI-TOD-v2 / NWD-RKA.
- Scale Match for Tiny Person Detection.
- Recent UAV small-object YOLO variants from the related-work matrix.

Draft logic:
1. Tiny objects have very limited pixels, making localization error and feature loss more harmful than in normal-scale detection.
2. AI-TOD and AI-TOD-v2 emphasize that tiny-object benchmarks require careful assignment/evaluation and that IoU-based matching can be fragile for very small boxes.
3. TinyPerson highlights scale mismatch and the need to consider object-size distribution.
4. Therefore, this project must report scale-wise metrics before making small-object improvement claims.

Evidence boundary:
- Do not say the proposed model improves tiny-object detection directly until `paper/tables/ieee_scale_results_visdrone.csv` exists.

## 3. Multi-Scale Feature Fusion and High-Resolution Prediction

Purpose in manuscript:
- Support the P2 branch and high-resolution feature argument.
- Connect the project to established feature-pyramid designs.

Key sources to cite:
- FPN.
- PANet.
- EfficientDet/BiFPN.
- TPH-YOLOv5.

Draft logic:
1. Feature pyramid methods fuse semantic and spatial information across scales to improve detection across object sizes.
2. Bottom-up and bidirectional fusion designs show that the path of information flow matters, especially when shallow spatial details are needed.
3. UAV small-object detectors often add or strengthen high-resolution prediction heads to reduce feature loss for tiny targets.
4. The current P2 branch should be positioned as a lightweight high-resolution prediction adaptation, not as a brand-new concept by itself.

Evidence boundary:
- The P2 branch can be discussed structurally now; quantitative claims must use exact completed VisDrone values.

## 4. Lightweight YOLO Detectors for UAV Scenes

Purpose in manuscript:
- Explain why YOLO11n and nano/small baselines are used.
- Separate fair ablation from broader family-level comparison.

Key sources to cite:
- Ultralytics YOLO documentation only for implementation context.
- YOLOv5n/YOLOv8n/YOLO11n/YOLO11s local baseline results.
- Recent UAV YOLO papers such as SOD-YOLO, SOD-YOLOv8, MASF-YOLO, and SRTSOD-YOLO after citation verification.

Draft logic:
1. YOLO-family detectors are widely used where inference speed matters.
2. Nano-size detectors are attractive for lightweight UAV deployment, but they often lose small-object recall and localization quality.
3. A fair paper must distinguish same-backbone ablation from cross-family or larger-capacity comparison.
4. Existing local results show that larger YOLO11s-960 has higher absolute accuracy, so the paper should focus on lightweight trade-offs.

Evidence boundary:
- Do not compare YOLOv8n and YOLO11n-P2-CA-960 as if they are a controlled ablation.
- Do not claim the nano model beats larger-capacity models.

## 5. Attention and Feature Calibration

Purpose in manuscript:
- Give the background for CoordAttention and TOFC-like calibration.
- Avoid over-centering CoordAttention when the completed evidence does not support it as the primary gain source.

Key sources to cite:
- CoordAttention.
- Lightweight/mobile attention modules if added later.
- TOFC only as this project's candidate module after experiments.

Draft logic:
1. Attention mechanisms can improve feature selectivity and encode spatial or positional cues.
2. CoordAttention is relevant because it preserves directional position information while keeping low overhead.
3. In the current completed VisDrone evidence, CoordAttention should be treated as an ablation component rather than a decisive improvement source.
4. A stronger IEEE contribution may require a task-specific feature calibration module that is validated through full training and scale-wise analysis.

Evidence boundary:
- Do not make TOFC a final method claim until its full result evidence exists.

## Literature Table Rules

When preparing the final IEEE literature comparison:

- Separate reproduced local experiments from reported literature results.
- Record dataset, split, input size, metric definition, backbone/model size, and whether the result is reproduced.
- Do not mix validation-set results with official test-dev/test-challenge results in one ranking table.
- Do not compare papers across different datasets as if they are direct SOTA rankings.
- Use the literature table to show context and novelty pressure, not to fabricate superiority.

## Next Citation Tasks

1. Convert high-priority rows in `paper/ieee_related_work_matrix.csv` to BibTeX.
2. Verify recent UAV YOLO papers through primary paper pages or publisher pages.
3. Identify which methods have public code and can realistically be reproduced.
4. Create a separate reproduced-vs-reported comparison table before writing the final IEEE Results section.

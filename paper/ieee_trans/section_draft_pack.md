# IEEE Transactions Section Draft Pack

Status: planning draft, not a submission manuscript.

This file collects evidence-bounded English section drafts for the IEEE Transactions route. It is intentionally not named `main.tex` and must not be treated as a final manuscript. The paragraphs below may be moved into an IEEEtran manuscript only after the evidence gates in `paper/ieee_claim_boundary.md` and `paper/ieee_submission_dashboard.md` are satisfied.

## Evidence Rules for This Draft Pack

- Use only values traced to `paper/tables/main_comparison_for_paper.csv`, `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv`, `paper/tables/ieee_scale_results_visdrone.csv`, and `paper/tables/ieee_scale_ap_results_visdrone.csv`.
- Do not claim best published performance.
- Do not claim cross-dataset generalization from the completed UAVDT runs; the audited UAVDT evidence currently shows a static-P2 validity boundary.
- Do not present TOFC as a proven small-object improvement over YOLO11n-P2-960; current evidence supports only aggregate-mAP improvement with weaker small-object diagnostics.
- Do not present ScaleAwareP2Gate as a result-bearing method until its VisDrone and UAVDT runs are complete, synced, and audited.
- Discuss AP-style scale results as local scale-bin AP only, not official COCO or VisDrone AP-small/AP-medium/AP-large.
- Acknowledge that YOLO11s-960 remains the strongest completed reference in absolute VisDrone accuracy.

## Current Evidence Snapshot

| Evidence Item | Status | Source |
| --- | --- | --- |
| VisDrone main comparison | Ready | `paper/tables/main_comparison_for_paper.csv` |
| Speed and complexity | Ready | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` |
| Scale-wise recall/precision | Ready | `paper/tables/ieee_scale_results_visdrone.csv` |
| Local scale-bin AP | Ready | `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| TOFC aggregate result | Ready with caveat | `runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt`, `paper/tables/main_comparison_for_paper.csv`, and scale diagnostic CSVs |
| UAVDT cross-dataset result | Ready with negative-transfer caveat | `paper/tables/ieee_uavdt_results_for_paper.csv` |
| ScaleAwareP2Gate candidate | Build-ready, result-locked | `configs/models/yolo11n_p2_scalegate.yaml`, `paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md` |

## Working Title Options

Use a title only after the final method is selected from real results.

1. Scale-Aware High-Resolution Prediction for Lightweight UAV Small-Object Detection
2. ScaleGate-YOLO11n: Adaptive High-Resolution Prediction for UAV Traffic Object Detection
3. Revisiting High-Resolution Prediction Branches for Lightweight UAV Object Detection

Titles 1 and 2 are locked until ScaleGate or a later adaptive-P2 method passes
the VisDrone/UAVDT evidence gates. Title 3 is the conservative fallback if the
new method evidence is mixed.

## Abstract Draft Boundary

Do not finalize the abstract yet. A safe abstract can be assembled after the ScaleGate decision is complete. The final abstract should include:

1. UAV traffic small-object detection problem.
2. Static P2 boundary evidence and the selected adaptive method, if validated.
3. Exact VisDrone and cross-dataset values from audited tables only.
4. A conclusion framed as an accuracy-efficiency-scale trade-off, not universal superiority.

## Introduction Draft

Unmanned aerial vehicles provide flexible viewpoints for traffic monitoring, emergency response, and urban scene understanding. However, object detection in UAV imagery remains challenging because targets often occupy only a small number of pixels, appear in dense groups, and suffer from occlusion, scale variation, and viewpoint-induced appearance changes. These factors are particularly visible in traffic-oriented aerial datasets such as VisDrone2019-DET, where pedestrians, vehicles, and non-motorized traffic participants are frequently observed at small scales.

Lightweight detectors are attractive for UAV-assisted perception because they reduce model size and inference cost. Nevertheless, compact YOLO models may lose fine spatial details when small objects are represented mainly by deep low-resolution features. A direct way to reduce this limitation is to strengthen shallow high-resolution prediction while preserving the efficiency advantage of a nano-scale detector. This motivates an evidence-bounded study of YOLO11n variants with a P2 high-resolution prediction branch, input-resolution adjustment, and feature attention calibration.

The current completed experiments show that high-resolution input and P2 prediction can improve the small-object behavior of YOLO11n on the VisDrone validation split, but the results also show clear capacity and cross-dataset trade-offs. In particular, larger YOLO11s-960 remains stronger in absolute validation accuracy, and UAVDT does not support a static-P2 transfer claim. Therefore, the paper should be framed around lightweight accuracy-efficiency trade-offs, small-object analysis, and adaptive-method validation rather than a claim that the nano model dominates larger detectors.

The current validated and result-locked contributions should be separated as follows:

1. A reproducible VisDrone2019-DET evaluation of lightweight YOLO baselines and YOLO11n variants under traced training logs, speed measurements, and complexity statistics.
2. An analysis of high-resolution prediction for YOLO11n, showing how a P2 branch and 960 input resolution affect detection accuracy, efficiency, scale-wise recall/precision, local scale-bin AP, and UAVDT transfer behavior.
3. An evidence-bounded discussion of CoordAttention and TOFC as auxiliary ablations, where gains are interpreted cautiously rather than treated as universally positive modules.
4. A result-locked adaptive P2 design, ScaleAwareP2Gate, motivated by the completed UAVDT boundary and described structurally before performance claims are allowed.

The following contribution statements are locked until additional evidence is available:

1. TOFC as a proven small-object improvement over YOLO11n-P2-960.
2. ScaleAwareP2Gate as a final method before completed runs.
3. Cross-dataset generalization claims.
4. Official AP-small/AP-medium/AP-large claims.

## Related Work Draft

### UAV Object Detection Benchmarks

UAV object detection benchmarks provide the evaluation basis for aerial traffic perception and small-object analysis. VisDrone2019-DET contains diverse UAV-captured scenes with dense object distributions and has been widely used to evaluate detection methods under aerial viewpoints \cite{du2019visdrone_det}. UAVDT further emphasizes vehicle detection and tracking in UAV traffic scenes \cite{du2018uavdt}. Other aerial or UAV-related datasets, including AI-TOD, AU-AIR, TinyPerson, and HIT-UAV, highlight the difficulty of tiny objects, low-altitude traffic surveillance, and modality variation \cite{wang2021aitod,xu2022aitodv2_nwd,bozcan2020auair,yu2020tinyperson,suo2023hituav}.

For the current manuscript, VisDrone is the main completed evidence source and UAVDT is the completed cross-dataset boundary source. The UAVDT results currently weaken a static-P2 generalization claim and should be used as motivation for adaptive high-resolution design rather than ignored.

### Feature Pyramids and High-Resolution Prediction

Feature pyramid designs are widely used to improve multi-scale object detection. FPN introduces top-down feature fusion to combine semantic and spatial information across scales \cite{lin2017fpn}, while PANet enhances path aggregation for information flow \cite{liu2018panet}. EfficientDet further studies scalable feature fusion and compound scaling for efficient detection \cite{tan2020efficientdet}. In UAV scenes, small objects often rely on shallow spatially detailed features; therefore, adding or strengthening high-resolution prediction branches can be a practical strategy for lightweight detectors.

The P2 branch used in this project follows this general motivation: it adds a higher-resolution detection scale to the nano model so that small objects can be represented before spatial detail is excessively downsampled. This should be described as a high-resolution prediction strategy, not as a novel feature pyramid theory.

### Lightweight YOLO Detectors

YOLO-family detectors are commonly used when real-time or near-real-time deployment is required. Nano-scale models reduce parameters and model size, but they also have limited capacity under dense small-object scenes. This project compares YOLOv5n, YOLOv8n, YOLO11n, and YOLO11s variants on VisDrone under traceable experimental settings. The comparison should be used to support a practical trade-off discussion: smaller models are easier to deploy, while larger models can still achieve stronger absolute accuracy.

### Attention and Feature Calibration

Attention modules can recalibrate feature responses and may help compact detectors emphasize informative spatial or channel cues. Coordinate Attention encodes positional information into lightweight attention maps for mobile networks \cite{hou2021coordinate_attention}. In the current completed experiments, CoordAttention is available as an ablation around the YOLO11n-P2 design. It should be discussed as an auxiliary calibration module and interpreted according to the measured results, because the 960-input P2-CA model does not dominate all metrics compared with the P2-only model.

## Method Draft

### Baseline Detector

The baseline detector is Ultralytics YOLO11n, a nano-scale YOLO model used here as the primary lightweight reference. The baseline is evaluated at 640 and 960 input resolutions on VisDrone2019-DET. The 960-input baseline provides the fairest comparison point for P2-based 960-input variants because it separates input-resolution effects from architectural effects.

### P2 High-Resolution Prediction Branch

The P2 variant extends YOLO11n with an additional high-resolution prediction branch. Compared with the standard P3/P4/P5 prediction structure, the P2/P3/P4/P5 structure introduces a shallower detection scale designed to preserve more spatial detail for small targets. This modification increases model complexity from 2.592 M parameters and 6.5 GFLOPs in YOLO11n-960 to 2.894 M parameters and 10.7 GFLOPs in YOLO11n-P2-960, based on the audited complexity table.

### CoordAttention Ablation

CoordAttention is added after feature fusion as an auxiliary attention ablation. The P2-CA design contains 2.904 M parameters and 10.7 GFLOPs at the audited model scale. It should be described as a position-aware feature recalibration experiment. The completed results support a nuanced interpretation: P2-CA-960 improves validation recall and small-object recall relative to YOLO11n-960, but P2-only obtains a slightly higher best mAP50 and mAP50-95 in the current VisDrone experiments.

### TOFC Candidate Module

Tiny Object Feature Calibration is a candidate module for the IEEE route. Its completed VisDrone run gives higher aggregate best mAP than YOLO11n-P2-960, but the current small-object diagnostic metrics are weaker than P2-960. It should therefore be described as an aggregate calibration ablation or candidate, not as a proven small-object diagnostic improvement.

### ScaleAwareP2Gate Candidate

ScaleAwareP2Gate is the current post-UAVDT redesign candidate. It inserts an identity-initialized gate after the P2 high-resolution feature block. The motivation is to keep the useful shallow detail pathway while allowing the P2 response to be adapted rather than statically amplified on every dataset.

Let \(F_2\) denote the fused P2 feature map. The gate computes local context \(L_2\), channel gate \(G_c\), spatial gate \(G_s\), and modulation \(M_2=G_s\odot G_c\). The output is:

\[
\hat{F}_2 = F_2 + \Delta_{\max}\tanh(\gamma) L_2 \odot M_2,
\]

where \(\gamma\) is initialized to zero. Therefore, the module starts as the static P2 path and learns only a bounded residual modulation. At present, this module has structural build evidence only. It must not be described as improving accuracy or robustness until its VisDrone and UAVDT runs are complete and audited.

## Experimental Setup Draft

### Dataset

The completed experiments use the VisDrone2019-DET validation split. Scale-wise analysis groups ground-truth boxes by area into small objects below 32 x 32 pixels, medium objects from 32 x 32 to below 96 x 96 pixels, and large objects at 96 x 96 pixels or above. The recall/precision table is computed by GT scale groups, while the local scale-bin AP diagnostic filters both ground-truth and predicted boxes by the configured scale bin. The latter should not be described as an official COCO or VisDrone AP-small metric.

### Implementation Details

The completed training logs record 100 training epochs and seed 42 for the compared VisDrone runs. Existing 640-input runs use batch size 8 for nano-scale models, while 960-input nano runs use batch size 4. The larger YOLO11s-960 run uses batch size 2. Speed measurements use single-image GPU wall-clock timing with 10 warm-up runs and 100 measured samples, and the table also records Ultralytics preprocess, inference, and postprocess timing.

Any final manuscript should report hardware and software exactly as recorded in the audited tables and manuscript material. Do not add unverified NMS, optimizer, or pretraining details.

## Results Draft

### Main VisDrone Results

At 960 input resolution, YOLO11n-960 obtains a best mAP50 of 0.42136 and best mAP50-95 of 0.25067 on the VisDrone validation split. Adding the P2 high-resolution branch gives YOLO11n-P2-960 a best mAP50 of 0.42361 and best mAP50-95 of 0.25552. The P2-CA-960 variant obtains a best mAP50 of 0.41996 and best mAP50-95 of 0.25174. YOLO11n-P2-TOFC-960 obtains the strongest completed nano-scale aggregate metrics in the current table, with best mAP50 of 0.42837 and best mAP50-95 of 0.26054. These values indicate that P2 provides a modest improvement over the resolution-matched YOLO11n baseline, while TOFC improves aggregate mAP but must still be interpreted together with scale-wise diagnostics.

The larger YOLO11s-960 reference obtains a best mAP50 of 0.48901 and best mAP50-95 of 0.29812. This result should be explicitly acknowledged: the current nano-scale variants do not outperform the larger model in absolute accuracy. Their value lies in a smaller model footprint and a lightweight trade-off analysis.

### Speed and Complexity

YOLO11n-960 has 2.592 M parameters, 6.5 GFLOPs, a 5.25 MB weight file, and 21.31 ms wall-clock latency in the recorded speed test. YOLO11n-P2-960 increases complexity to 2.894 M parameters and 10.7 GFLOPs, with a 6.06 MB weight file and 22.88 ms latency. YOLO11n-P2-CA-960 has 2.904 M parameters, 10.7 GFLOPs, a 6.09 MB weight file, and 23.36 ms latency. YOLO11n-P2-TOFC-960 has 2.896 M parameters, 10.8 GFLOPs, a 6.07 MB weight file, and 22.61 ms latency. These results show that the P2-family variants add measurable computational cost, so their accuracy gains should be interpreted together with efficiency.

YOLO11s-960 has 9.432 M parameters, 21.6 GFLOPs, an 18.32 MB weight file, and 24.02 ms measured latency in the current single-image timing table. The much larger parameter count and file size should be discussed as a deployment trade-off rather than ignored.

### Scale-Wise Recall and Precision

Scale-wise analysis gives more direct evidence for the small-object motivation. Compared with YOLO11n-960, YOLO11n-P2-960 improves small-object recall from 0.420259 to 0.450124, a gain of 0.029865. YOLO11n-P2-CA-960 further reaches 0.455089 small-object recall, a gain of 0.034830 over YOLO11n-960. YOLO11n-P2-TOFC-960 records small-object recall of 0.430828, which is above YOLO11n-960 but below YOLO11n-P2-960. The small-object precision values are 0.661952 for YOLO11n-960, 0.674799 for YOLO11n-P2-960, 0.666036 for YOLO11n-P2-CA-960, and 0.677857 for YOLO11n-P2-TOFC-960.

The same table also shows trade-offs on other scales. YOLO11n-P2-960 has medium-object recall of 0.778928 and large-object recall of 0.887640, both slightly below the YOLO11n-960 values of 0.789464 and 0.890449. YOLO11n-P2-CA-960 shows medium-object recall of 0.781450 and large-object recall of 0.882022. YOLO11n-P2-TOFC-960 records medium-object recall of 0.765421 and large-object recall of 0.874532. Therefore, the appropriate interpretation is that high-resolution prediction improves small-object recall in the completed VisDrone analysis, while gains are not uniform across all object scales.

YOLO11s-960 remains the strongest completed reference in scale-wise recall, with small-object recall of 0.492703, medium-object recall of 0.827555, and large-object recall of 0.899813. The final manuscript should use this result to present an honest trade-off narrative.

### Local Scale-Bin AP Diagnostic

The local scale-bin AP output provides an additional AP-style diagnostic for the same completed VisDrone models. This evaluation should be described as local scale-bin AP because it is computed from YOLO-format labels and prediction scale bins, not from an official COCO or VisDrone AP-small evaluator.

For the small-object bin, YOLO11n-960 obtains AP50 of 0.229995 and mAP50-95 of 0.116295. YOLO11n-P2-960 increases these values to 0.247659 and 0.131540, respectively. YOLO11n-P2-CA-960 obtains 0.239473 AP50 and 0.126067 mAP50-95. YOLO11n-P2-TOFC-960 obtains 0.229853 AP50 and 0.120661 mAP50-95, which confirms that its aggregate mAP gain does not translate into a small-bin AP50 gain over P2-960. YOLOv8n-960 obtains 0.237713 AP50 and 0.122135 mAP50-95, while YOLO11s-960 remains the strongest completed small-bin reference with 0.302540 AP50 and 0.159421 mAP50-95.

The AP-style diagnostic supports the same cautious interpretation as the recall/precision analysis: the P2 branch improves the small-bin behavior of YOLO11n, but the benefit is not uniform across all scales. In the medium bin, YOLO11n-960 records 0.452575 AP50 and 0.309690 mAP50-95, while YOLO11n-P2-960 records 0.438392 and 0.300511. In the large bin, YOLO11n-960 records 0.577546 AP50 and 0.459221 mAP50-95, while YOLO11n-P2-960 records 0.456420 and 0.368950. Therefore, the manuscript should present P2 as improving small-object diagnostics at the cost of some medium/large-bin trade-offs.

## Discussion Draft

The completed VisDrone results suggest that increasing input resolution and adding a high-resolution P2 prediction branch help a compact YOLO11n detector recover more small objects. This observation is consistent with the intuition that shallow features preserve spatial detail that can be lost in deeper low-resolution maps. However, the measured gains are modest in aggregate mAP, and the scale-wise analysis shows that improvements concentrate mainly on the small-object group.

CoordAttention changes the feature calibration behavior of the P2 model. The 960-input P2-CA model records a higher final recall than P2-only in the main comparison table, and it records the highest small-object recall among the completed nano-scale YOLO11n variants in the scale-wise table. At the same time, P2-only has a slightly higher best mAP50 and mAP50-95. The method discussion should therefore avoid claiming that attention universally improves detection; instead, it should explain that the attention module shifts the precision-recall and scale-wise behavior.

The comparison with YOLO11s-960 is important for an IEEE-level manuscript. The larger model provides a stronger accuracy reference in aggregate accuracy, small-object recall, and local small-bin AP. This means the paper should not be built on an absolute best-performance claim. A stronger and safer contribution is to analyze how lightweight high-resolution prediction affects small-object detection and deployment cost under a reproducible experimental protocol.

## Locked Paragraphs for Future Results

### TOFC Result Paragraph

Locked until `runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt` and its audited metrics exist.

When evidence exists, report exact mAP50, mAP50-95, precision, recall, parameters, GFLOPs, weight size, latency, FPS, and scale-wise recall/precision. Compare TOFC against YOLO11n-960, YOLO11n-P2-960, YOLO11n-P2-CA-960, and YOLO11s-960. If TOFC does not improve the target trade-off, do not present it as the main method.

### UAVDT Boundary Paragraph

Unlocked as boundary evidence for static P2. The completed UAVDT rows should be used to state that YOLO11n-P2-960 is weaker than the matched YOLO11n-960 baseline and other completed references under the current setting. This prevents a static-P2 generalization claim and motivates the ScaleAwareP2Gate candidate.

Locked for ScaleGate until the ScaleGate UAVDT run is complete. When evidence exists, report exact UAVDT validation metrics and discuss whether the adaptive P2 design repairs, reduces, or fails to repair the static-P2 degradation.

### Official AP-Small Paragraph

Locked until an official COCO-style or VisDrone-compatible AP-small/AP-medium/AP-large evaluator is used and documented.

The current project now has a local scale-bin AP diagnostic, but this must not be converted into official AP-small wording. If used, state the local metric definition clearly.

## Conclusion Draft

The completed VisDrone experiments show that a high-resolution P2 prediction branch can improve the small-object diagnostics of YOLO11n under traceable validation protocols. At 960 input resolution, YOLO11n-P2-960 improves best mAP50-95 from 0.25067 to 0.25552 compared with YOLO11n-960, improves small-object recall by 0.029865, and improves local small-bin AP50 from 0.229995 to 0.247659. Adding CoordAttention further increases small-object recall to 0.455089, but does not uniformly improve all aggregate or scale-bin AP metrics. These results support an accuracy-efficiency trade-off view of lightweight UAV object detection.

The current manuscript should remain incomplete until the ScaleGate result and final method decision are available. The final conclusion must reflect the full evidence rather than the current planning state. If ScaleGate passes the gates, the conclusion should explain whether adaptive P2 improves the small-object/efficiency/cross-dataset trade-off. If it fails, the conclusion should not hide the failure; the paper should either become a boundary study or move to a second-cycle method design.

## Source Traceability

| Claim Type | Current Source |
| --- | --- |
| Main validation metrics | `paper/tables/main_comparison_for_paper.csv` |
| Speed values | `paper/tables/speed_results.csv` |
| Complexity values | `paper/tables/model_complexity.csv` |
| Scale-wise recall/precision | `paper/tables/ieee_scale_results_visdrone.csv` |
| Local scale-bin AP | `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| UAVDT cross-dataset boundary | `paper/tables/ieee_uavdt_results_for_paper.csv` |
| ScaleGate redesign plan | `paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md` |
| Scale-wise interpretation | `paper/ieee_scale_result_interpretation.md` |
| Locked evidence gates | `paper/ieee_submission_dashboard.md` |

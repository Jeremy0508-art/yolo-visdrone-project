# IEEE Citation Plan

Status: planning draft. This document maps seed references to manuscript roles. It does not replace final citation verification.

## Citation Groups

| Group | Seed Keys | Manuscript Role |
| --- | --- | --- |
| Primary UAV benchmark | `du2019visdrone_det`, `visdrone_dataset_repo` | Introduce VisDrone and justify primary dataset. |
| Cross-dataset UAV traffic benchmark | `du2018uavdt`, `uavdt_project_page` | Justify UAVDT as the required second dataset for T-ITS framing. |
| Drone YOLO prior | `zhu2021tph_yolov5` | Position high-resolution/multi-head drone detection work and novelty pressure. |
| Recent UAV/YOLO small-object methods | `li2024sod_yolo`, `qu2025sma_yolo`, `lu2025masf_yolo`, `xu2025srtsod_yolo`, `khalili2024sod_yolov8` | Establish recent novelty pressure and separate literature-only context from reproduced comparisons. |
| Feature pyramid background | `lin2017fpn`, `liu2018panet`, `tan2020efficientdet` | Support multi-scale fusion and high-resolution feature-branch discussion. |
| Attention background | `hou2021coordinate_attention` | Explain CoordAttention as an auxiliary lightweight positional attention module. |
| Tiny-object benchmark and assignment | `wang2021aitod`, `xu2022aitodv2_nwd`, `aitod_repo`, `aitodv2_project_page` | Motivate scale-wise metrics and tiny-object evidence rules. |
| Optional traffic UAV dataset | `bozcan2020auair`, `auair_api_repo` | Backup dataset discussion if AU-AIR is used later. |
| Adjacent tiny/thermal datasets | `yu2020tinyperson`, `suo2023hituav` | Background only unless the experiment scope expands. |

## High-Priority Citations by Section

| Section | Must-Have Citations | Notes |
| --- | --- | --- |
| Introduction | VisDrone, UAVDT, FPN/P2-related background, lightweight YOLO prior | Keep motivation concise and tied to traffic UAV scenes. |
| Related Work: UAV datasets | VisDrone, UAVDT, AU-AIR | Mention AI-TOD separately under tiny-object benchmarks. |
| Related Work: small/tiny objects | AI-TOD, AI-TOD-v2/NWD, TinyPerson | Use to justify scale-wise metrics, not to claim our result yet. |
| Related Work: feature fusion | FPN, PANet, EfficientDet, TPH-YOLOv5 | Connect to P2 branch and high-resolution prediction. |
| Related Work: recent UAV/YOLO methods | SOD-YOLO, SMA-YOLO, MASF-YOLO, SRTSOD-YOLO, SOD-YOLOv8 | Use as context and novelty pressure; do not turn into a direct ranking table unless evaluation settings are aligned. |
| Related Work: attention/calibration | CoordAttention | Add more lightweight attention references only after final method is fixed. |
| Method | FPN/PANet/EfficientDet, CoordAttention if used | Avoid over-citing in method; cite core mechanism sources. |
| Experiments | VisDrone, UAVDT | Dataset citations should appear in dataset subsection. |
| Discussion | AI-TOD-v2/NWD, TinyPerson | Use for limitations around tiny-object localization and scale. |

## Verification Rules

- Final `references.bib` should be created from `references_seed.bib` only after final target journal and method are fixed.
- Every seed entry with `misc` should be reconsidered before submission; if a citable paper exists, prefer the paper.
- Publisher/proceedings metadata should be checked again before final PDF compilation.
- Literature-reported performance values must not be copied into result tables unless dataset, split, input size, and metric definitions are directly comparable.
- Reproduced results and reported-only results must be separated in the final manuscript.

## Missing Citation Work

| Need | Action |
| --- | --- |
| Recent 2024-2026 UAV YOLO papers | Seed BibTeX entries added; verify publisher metadata again before final `references.bib`. |
| YOLO11 / Ultralytics implementation citation | Decide whether to cite official docs, an overview paper, or only mention implementation. |
| RT-DETR or Transformer detector baseline | Add only if a real comparison experiment is planned. |
| IEEE T-ITS examples | Add after selecting 3-5 highly relevant recent T-ITS UAV/traffic perception papers. |

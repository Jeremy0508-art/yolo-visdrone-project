# Failure Case Taxonomy for VisDrone Detection

This document organizes qualitative failure modes for the journal manuscript. It is based on the project task characteristics and existing qualitative assets, not on new numeric claims.

## Source Assets

| Asset | Use |
| --- | --- |
| `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | Main failure-case contact sheet |
| `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | Representative validation predictions |
| `paper/figures/qualitative/p2_coordatt_960_val_batch1_pred.jpg` | Representative validation predictions |
| `paper/figures/qualitative/p2_coordatt_960_val_batch2_pred.jpg` | Representative validation predictions |

## Failure Categories

| Category | Typical Cause | Manuscript Discussion Angle |
| --- | --- | --- |
| Extremely small missed objects | Targets occupy very few pixels after aerial imaging; texture and contour cues are weak | Explain why high-resolution input and P2 features help but cannot fully recover invisible detail |
| Dense occlusion | Pedestrians, vehicles, and non-motor vehicles overlap in crowded street scenes | Discuss limits of NMS, feature separation, and one-stage dense prediction |
| Category confusion | `pedestrian` vs `people`, or `bicycle`/`tricycle`/`awning-tricycle` have similar top-view appearance | Connect to per-class results and aerial viewpoint ambiguity |
| Background false positives | Road markings, signs, shadows, or small structures resemble target shapes | Discuss need for stronger context modeling or hard-negative mining |
| Truncated boundary objects | Objects at image edges are only partially visible | Explain localization uncertainty and annotation/prediction mismatch |
| Scale imbalance | Small targets dominate the dataset while large targets are fewer but easier | Connect to scale-distribution statistics and scale-group matching results |

## Recommended Manuscript Wording

The visualization section should avoid claiming that the model solves all dense small-object cases. A safer wording is:

> Qualitative results show that the model can detect many vehicles and pedestrians in dense aerial scenes. However, missed detections still occur for extremely small or heavily occluded targets, and category confusion remains possible among visually similar non-motor vehicle classes. These cases indicate that high-resolution input and shallow feature prediction improve small-object sensitivity but do not fully eliminate the difficulty of dense aerial object detection.

## Follow-up Work Ideas

The limitation discussion can mention these future directions:

- Sliced inference or SAHI-style inference for extremely small targets.
- Post-processing tuned for dense scenes.
- Context-enhanced feature fusion for category confusion.
- Hard-negative mining for background false positives.
- Official test-dev evaluation when the platform is available.

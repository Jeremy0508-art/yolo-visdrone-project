# Research Strengthening Plan

This document records the next phase after the initial paper draft. The current manuscript is a solid project-to-paper baseline, but it is not yet strong enough as a competitive submission. The next work should strengthen novelty, external comparison, and discussion depth.

## Current Assessment

The current paper is closer to an organized technical report or first manuscript draft than a strong conference submission. Its main value is that experiments are reproducible and all numbers are traceable, but the paper still lacks:

- External method comparison under the same training/evaluation protocol.
- A stronger explanation of why the proposed combination is preferable to existing UAV small-object detection methods.
- More detailed analysis of small-object categories, failure modes, and accuracy-speed trade-offs.
- A clearer method figure and more complete related-work positioning.
- Official test-dev/test-challenge evidence, if the VisDrone platform becomes usable.

## Strengthening Direction

The paper should move from:

```text
YOLO11n + P2 + CoordAttention + 960 input works on our project
```

to:

```text
For lightweight UAV small-object detection, high-resolution shallow-feature detection and input resolution are the dominant contributors; attention and augmentation provide secondary gains. The proposed configuration gives a reproducible accuracy-speed trade-off on VisDrone.
```

## Required Additional Comparisons

All new metrics must come from real local runs or official results. Literature numbers may be discussed only as background, not mixed directly into our result table unless the protocol is identical.

Recommended local baselines:

| Priority | Experiment | Purpose |
| --- | --- | --- |
| High | YOLOv8n on VisDrone, 640 | Compare against a widely used lightweight YOLO baseline |
| High | YOLOv8n-P2 or YOLOv8n with high-resolution head, if feasible | Check whether P2 gain is specific to YOLO11n or a general small-object effect |
| Medium | YOLO11s or YOLOv8s, 640 | Compare lightweight-nano model against a stronger small model |
| Medium | YOLO11n-P2-CoordAttention, 1280 or multi-scale val only | Test whether the 960 gain continues or saturates |
| Medium | YOLO11n-P2-CoordAttention with SAHI/sliced inference on val | Evaluate inference-time small-object enhancement without retraining |
| Low | Alternative attention module, e.g. SE/CBAM if already supported | Show CoordAttention is a reasonable attention choice |

## Additional Analysis Needed

| Analysis | Output |
| --- | --- |
| Per-class gain table versus baseline and P2 | Show which VisDrone classes benefit most |
| Accuracy-speed Pareto plot | Show mAP50-95 versus FPS/latency |
| Method structure diagram | Make P2 + CoordAttention + 960 pipeline visually clear |
| Failure case taxonomy | Separate tiny target miss, dense occlusion, category confusion, background false positives |
| Literature comparison table | Summarize related methods, dataset, baseline, improvement type, and reported gains |

## Paper Writing Upgrades

1. Expand related work into three clearer threads: UAV small-object detection, high-resolution/small-object detection heads, and attention/lightweight detection.
2. Add a method overview figure instead of only textual architecture description.
3. Add a "Discussion" subsection explaining why 960 input dominates the gain while SmallObjAug does not.
4. Add a "Threats to Validity" or "Limitations" paragraph: validation-set only, no official server AP, limited external baselines.
5. Avoid claiming SOTA. Claim reproducible accuracy-speed improvement under the project protocol.

## Near-Term Action Plan

1. Fix LaTeX/PDF formatting warnings enough for readable review.
2. Build a literature comparison table from primary papers and official documentation.
3. Add local YOLOv8n and YOLO11s/YOLOv8s baselines if GPU time is acceptable.
4. Re-export paper tables and update the manuscript after the new runs finish.
5. Revisit official VisDrone upload only if account verification becomes possible.

## Sources to Review

- VisDrone-DET2019 benchmark paper.
- CoordAttention CVPR 2021 paper.
- Ultralytics YOLO11 documentation.
- Recent UAV small-object detection papers such as SOD-YOLO, BPD-YOLO, LPAE-YOLOv8, and SL-YOLO.

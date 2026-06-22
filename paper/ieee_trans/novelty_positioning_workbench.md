# IEEE Novelty Positioning Workbench

Status: planning draft. This file is for contribution design and related-work
positioning. It is not a claim that the current method is already accepted or
superior.

## Why Positioning Must Be Tight

Recent UAV small-object YOLO papers already use many ingredients that look
similar at a surface level: extra high-resolution heads, attention modules,
multi-scale fusion, lightweight blocks, and larger input sizes. Therefore, the
paper cannot be positioned as "we add P2" or "we add attention" and expect an
IEEE Transactions-level contribution. The contribution must be tied to a
specific, evidence-backed problem:

> Static high-resolution prediction can improve small-object diagnostics on a
> tiny-object-heavy dataset, but it can also degrade under a different UAV
> traffic distribution. The method and analysis should explain, measure, and
> if possible reduce this brittleness.

## Existing Work Pressure

| Prior direction | Representative entries in current matrix | What it already covers | Risk for this paper |
| --- | --- | --- | --- |
| Extra detection heads for drone objects | TPH-YOLOv5 | High-resolution/tiny-object prediction heads are established | A static P2 branch alone is not novel enough |
| Attention-enhanced UAV YOLO | SOD-YOLO, SMA-YOLO, CoordAttention-related work | Attention and multi-scale fusion are common | "Add an attention module" is too generic |
| YOLO11-based UAV small-object methods | MASF-YOLO, SRTSOD-YOLO | Recent work already uses YOLO11 and adaptive/multi-scale language | The manuscript must show a sharper mechanism and evidence boundary |
| Tiny-object assignment/scale diagnostics | AI-TOD-v2, NWD/RKA, TinyPerson scale match | Scale mismatch is a known issue | Local scale-bin diagnostics are useful, but not enough as a method contribution |
| Traffic-oriented UAV datasets | UAVDT, AU-AIR | Cross-dataset traffic framing exists | A VisDrone-only claim is weak for T-ITS-style positioning |

## Current Defensible Position

Before ScaleGate finishes, the defensible position is:

1. The project provides a controlled evidence chain for YOLO11n resolution,
   P2, CoordAttention, TOFC, speed, complexity, and scale-wise diagnostics.
2. Static P2 has a real boundary: it helps some VisDrone small-object
   diagnostics but fails to transfer to UAVDT in the current matched setting.
3. ScaleAwareP2Gate is a motivated adaptive-P2 candidate, not a completed
   contribution.

This is a strong planning position but not yet a final IEEE method paper.

## If ScaleGate Passes

If completed evidence satisfies the method-selection protocol, the final
novelty can be written around:

- an identity-initialized bounded adaptive P2 gate, rather than a static extra
  head;
- cross-dataset motivation from the observed static-P2 UAVDT degradation;
- paired evidence on VisDrone and UAVDT;
- scale-wise diagnostics showing where the gate changes small-object behavior;
- efficiency reporting that keeps the model near the nano-scale regime.

Possible contribution wording:

> A scale-aware, identity-initialized P2 gating module is proposed to make
> shallow high-resolution prediction selective rather than uniformly active.
> The design is motivated by cross-dataset evidence showing that a static P2
> branch can be beneficial for VisDrone small-object diagnostics but brittle on
> UAVDT traffic scenes.

This wording is allowed only after the ScaleGate runs, speed tests, scale
diagnostics, and audits are complete.

## If ScaleGate Does Not Pass

If ScaleGate fails the acceptance rules, do not force it into the title,
abstract, or contribution list. The next paper route must be one of:

| Route | What the paper becomes | Extra work needed |
| --- | --- | --- |
| Boundary-analysis paper | A rigorous study of when high-resolution prediction helps or fails | Tighten analysis, add more datasets or official-compatible scale metrics |
| Second-cycle method paper | A new adaptive high-resolution method based on ScaleGate failure mode | Implement and train a stronger module |
| Chinese-journal route first | Keep the English route as extended future work | Polish CEA manuscript and use English materials as preparation |

For IEEE Transactions-level ambition, the preferred route is the second-cycle
method paper if ScaleGate is not competitive.

## Contribution Statements To Avoid

Do not write:

- "The proposed method is state-of-the-art."
- "P2 improves UAV object detection generally."
- "CoordAttention/TOFC/ScaleGate improves small-object detection" without
  scale-diagnostic evidence.
- "The method generalizes across datasets" before UAVDT and any additional
  evidence support it.
- "Local scale-bin AP is AP-small."

## Related-Work Paragraph Target

The final related-work positioning paragraph should say, in substance:

> Prior UAV small-object YOLO studies have strengthened high-resolution heads,
> attention, and multi-scale fusion. Unlike reported-only comparisons across
> different training protocols, this work uses locally reproduced lightweight
> baselines and cross-dataset validation to study when high-resolution
> prediction is beneficial or brittle. The adaptive-P2 route is motivated by
> this measured boundary rather than by adding another static head.

This paragraph should be revised after the ScaleGate result determines whether
the final manuscript is a method paper or a boundary-analysis paper.

# YOLO-World CVPR 2024 Benchmark Study for the IEEE Redesign

Status: active benchmark study for the major paper-structure and figure-system
redesign.

This file selects one top-tier reference paper and converts its paper-level
organization into concrete redesign rules for our IEEE manuscript. It is not a
claim source for our metrics. All quantitative claims in our paper must still
come from audited local logs, CSV files, and generated tables.

## Selected Benchmark Paper

Primary benchmark:

- Paper: YOLO-World: Real-Time Open-Vocabulary Object Detection
- Venue: CVPR 2024
- Official page:
  `https://openaccess.thecvf.com/content/CVPR2024/html/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.html`
- Official PDF:
  `https://openaccess.thecvf.com/content/CVPR2024/papers/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.pdf`

Why this paper is the main benchmark:

1. It is a top-conference detection paper, so its figure and structure quality
   are a useful upper-bound reference.
2. It is in the YOLO / real-time detection family, so its writing logic is much
   closer to our project than a generic transformer or segmentation paper.
3. It shows a complete research-paper pattern: task motivation, clear method
   overview, module-level explanation, efficiency-aware experiments, ablations,
   and qualitative evidence.
4. Its style can be imitated without copying its scientific claims. Our work is
   still UAV small-object detection, not open-vocabulary detection.

## What We Imitate

The benchmark paper is useful because it makes the reader understand the whole
paper quickly before entering details. Our current draft still reads too much
like an experiment report. The redesign should imitate the following functions.

| Benchmark Function | What It Achieves | Our Equivalent |
| --- | --- | --- |
| Early positioning figure | Shows why the method matters before dense tables appear | Add a front-facing accuracy-efficiency / validity-boundary figure near the introduction |
| Clean paradigm or architecture figure | Explains the method route with few visual elements | Redraw the high-resolution P2 + cross-scale CSGate overview as the main method figure |
| Module schematic | Makes the proposed block reproducible at a glance | Keep and polish the CSGate schematic with equations and identity-initialized bounded correction |
| Efficiency-aware tables and plots | Avoids accuracy-only storytelling | Keep mAP, recall, latency, FPS, GFLOPs, parameters, and weight size together |
| Ablation sequence | Turns variants into evidence rather than a model zoo | Reorder P2, CA, TOFC, ScaleGate, and CSGate around research questions |
| Qualitative panel | Shows typical gains and failures without raw clutter | Replace raw YOLO batch/contact sheets with curated comparison panels |

## What We Must Not Imitate

The benchmark paper should not push us into unsupported claims.

- Do not claim open-vocabulary capability.
- Do not claim foundation-model scale, large-scale pretraining, or SOTA status.
- Do not imply that our CSGate route is universally better than all YOLO-family
  baselines.
- Do not hide negative evidence from ScaleGate or the UAVDT static-P2 boundary.
- Do not copy figure layouts so closely that the visual identity becomes a
  derivative imitation rather than a paper-quality redesign.

## Structure Lessons for Our Manuscript

The redesigned paper should be organized around a small number of research
questions instead of a chronological list of model attempts.

### 1. Introduction

Target logic:

1. UAV traffic perception requires small-object sensitivity and compact models.
2. High-resolution prediction is a natural but costly solution.
3. Static P2 helps on VisDrone but has a cross-dataset validity boundary.
4. A self-conditioned P2 gate failed to solve the boundary.
5. Cross-scale P2/P3 consistency is a bounded repair hypothesis.

The introduction should contain one compact contribution list:

- evidence-bounded analysis of high-resolution prediction;
- scale-wise and efficiency-aware diagnostics;
- CSGate as a cross-scale, identity-initialized bounded correction;
- explicit validity-boundary discussion across VisDrone and UAVDT.

### 2. Related Work

Target logic:

1. UAV traffic and aerial small-object benchmarks;
2. multi-scale / high-resolution prediction heads;
3. lightweight YOLO and efficient detection;
4. attention and feature-gating modules;
5. our position: not another generic YOLO tweak, but a bounded study of when
   high-resolution prediction helps and fails.

### 3. Method

Target logic:

1. Overall framework and notation;
2. static P2 as the baseline high-resolution mechanism;
3. evidence gate for accepting or rejecting a method claim;
4. ScaleGate as the first-cycle negative/mixed adaptive gate;
5. CSGate as the second-cycle cross-scale consistency route;
6. computational-cost discussion.

### 4. Experiments

Target logic:

1. datasets and reproducibility protocol;
2. main VisDrone comparison;
3. UAVDT cross-dataset boundary test;
4. scale-wise diagnostics;
5. speed and complexity;
6. ablations and method-selection evidence;
7. qualitative and failure-case analysis.

### 5. Discussion and Conclusion

The discussion should make the paper more mature by saying what the evidence
does and does not prove. The conclusion should not become a sales pitch.

## Figure-System Lessons

The current draft needs a coherent figure system. The redesigned figures should
have stable roles, shared colors, and direct links to the argument.

| New Figure Role | Benchmark-Inspired Purpose | Current Action |
| --- | --- | --- |
| F1: visual abstract / method overview | Give the whole paper route in one figure | Redraw as "problem -> static P2 boundary -> CSGate repair -> evidence outputs" |
| F2: CSGate module | Explain the proposed block at implementation level | Keep the current script-generated CSGate figure, then polish typography and spacing |
| F3: evidence-boundary flow | Convert negative evidence into a research narrative | Create a flow diagram from VisDrone gain, UAVDT failure, ScaleGate rejection, CSGate bounded repair |
| F4: scale-wise diagnostics | Show why aggregate mAP is insufficient | Regenerate recall and local AP plots with consistent palette and clearer direct labels |
| F5: accuracy-efficiency trade-off | Show model choice under deployment constraints | Redraw as a clean scatter/bubble figure with model families and CSGate highlighted |
| F6: qualitative comparison | Replace raw outputs with curated evidence | Build small panels with original image, selected baseline, CSGate, and failure notes |
| F7: failure taxonomy | Make limitations visible and organized | Group typical failures into tiny distant targets, dense occlusion, and class ambiguity |

## Visual Rules Derived from the Benchmark

These rules should be applied before a figure enters `main_draft.tex`.

1. Every figure must have one message. If a figure needs a paragraph to explain
   what it is, split it.
2. Use direct labels near visual elements when possible; do not rely only on a
   large legend.
3. Use color semantics consistently: baseline, static P2, rejected gate, and
   CSGate should have stable colors across all plots.
4. Keep architectural figures sparse. Do not draw every YOLO layer.
5. Put the key method block near the center or right-center of the figure, not
   as a small appendix-like box.
6. Use panel labels only when there are real subpanels.
7. Put long explanations in captions and manuscript text, not inside images.
8. For quantitative figures, show uncertainty only if real repeated-run data
   exists; otherwise do not invent error bars.

## Direct Gap Diagnosis for Our Current Draft

| Area | Current Problem | Redesign Requirement |
| --- | --- | --- |
| Paper identity | The draft still feels like a progress report | Reframe around a single technical question: bounded high-resolution prediction for UAV small objects |
| Method center | P2, ScaleGate, and CSGate appear as a sequence of attempts | Make CSGate the main bounded method and use P2/ScaleGate as evidence leading to it |
| Figure hierarchy | Method figures and diagnostic plots do not yet form a story | Reorder figures from overview, module, evidence flow, diagnostics, trade-off, qualitative cases |
| Visual consistency | Some plots and schematics use different styles | Apply one palette, one font rule, and one label density rule |
| Qualitative evidence | Raw detector images are visually crowded | Curate fewer examples with larger panels and cleaner labels |
| Claim discipline | Negative evidence is present but not yet elegant | Turn negative/mixed results into validity-boundary discussion, not embarrassment |

## Redesign Execution Order

1. Update the target-journal benchmark plan to name YOLO-World as the primary
   top-conference structural benchmark.
2. Redraw F1 as a graphical argument figure, not only a network diagram.
3. Redraw F3 evidence-boundary flow before rewriting the introduction.
4. Regenerate F4 and F5 in the unified style guide.
5. Replace qualitative/failure figures with curated panels.
6. Rewrite the introduction and method opening around the new figure order.
7. Run `python tools/run_ieee_audits.py` and compile `main_draft.tex`.

## Claim Boundary

This benchmark study only authorizes structural and visual redesign. It does
not authorize stronger results, new numerical claims, or new SOTA language.
The paper can become more mature without changing the evidence standard:
numbers must remain traceable, and weak or mixed evidence must remain visible.

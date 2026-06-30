# Target Journal, Benchmark Articles, and Structure Plan

Status: active execution plan for the IEEE English-journal route.

This plan records the target journal choice, benchmark-paper strategy, and
manuscript-structure imitation rules requested after advisor feedback. It does
not replace the evidence audits. All claims and numbers in the manuscript must
still come from audited local tables, logs, or generated reports.

## Advisor Feedback Interpreted as Tasks

The advisor feedback has four practical requirements:

1. Select a target journal before continuing major writing.
2. Select target articles and imitate their paper structure at the level of
   section logic, figure placement, and contribution framing.
3. Improve the visual quality of all paper-facing figures, especially method
   overview and graphical-summary style figures.
4. Avoid a plain experiment-report style; the paper should look and read like a
   mature research article.

The linked WeChat visual reference cannot be treated as a scientific source, but
it is useful as a visual-style reference: soft color blocks, clear panel
separation, visual hierarchy, and an overview figure that explains the whole
paper at a glance.

## Target Journal Decision

| Rank | Journal | Decision | Reason | Risk |
| --- | --- | --- | --- | --- |
| 1 | IEEE Transactions on Intelligent Transportation Systems | Primary target | The project can be framed as UAV-assisted traffic perception, road-user detection, lightweight deployment, and UAVDT cross-dataset validation. | The paper must not read like generic YOLO tuning. |
| 2 | IEEE Transactions on Geoscience and Remote Sensing | Backup target | UAV imagery and small-object detection fit remote-sensing interpretation. | Current contribution is traffic-perception oriented and may need stronger remote-sensing novelty. |
| 3 | IEEE Transactions on Circuits and Systems for Video Technology | High-risk backup only | Possible if the method becomes substantially stronger as a visual-detection architecture. | Current evidence is not strong enough for broad video-technology novelty. |
| 4 | IEEE Transactions on Multimedia | Not recommended now | Very high bar for broad multimedia novelty and SOTA comparison. | Current bounded CSGate evidence is too narrow. |

Current choice:

> Write primarily for IEEE Transactions on Intelligent Transportation Systems,
> with TGRS kept as a backup only if the advisor redirects the paper toward
> remote-sensing methodology.

## Target Article Shortlist

The target articles below are not copied. They are used to decide how to
organize our manuscript, what kinds of figures are expected, and what level of
experimental discipline the paper should reach.

| Role | Target Article / Resource | Why It Matters | How We Imitate It |
| --- | --- | --- | --- |
| Primary top-conference structure benchmark | YOLO-World, CVPR 2024 | It is a top-tier YOLO-family real-time detection paper with mature method figures, efficiency-aware experiments, and a clear paper-level narrative. | Use it as the main template for section order, figure roles, method overview, ablation logic, and speed/accuracy presentation; do not imitate its open-vocabulary claims. |
| Journal-scope reference | IEEE T-ITS author/scope page | Confirms that the manuscript must emphasize transportation-system sensing and technical contribution. | Keep traffic perception visible in title, abstract, introduction, datasets, qualitative cases, and conclusion. |
| Backup-scope reference | IEEE TGRS author/scope page | Confirms remote-sensing backup direction. | Use only if the paper pivots to remote-sensing interpretation rather than ITS. |
| Drone small-object structure benchmark | TPH-YOLOv5 | Uses drone-captured scenarios and high-resolution/tiny-object head logic. | Imitate the section logic: motivation, module overview, training setup, ablation, comparison, qualitative cases. |
| Recent UAV YOLO journal benchmark | SOD-YOLO / SOD-YOLOv8 / SRTSOD-YOLO | Shows how recent UAV YOLO papers frame small-object improvements and figures. | Imitate their organization of method modules, ablation tables, and visual comparisons, but keep our bounded evidence. |
| Novelty-pressure benchmark | MASF-YOLO and other YOLO11 UAV small-object work | Very close to our YOLO11 setting and therefore important for novelty positioning. | Explicitly explain that our paper is not merely another YOLO11 fusion variant; it studies boundaries and CSGate partial repair. |
| Visual-style reference | Advisor-provided WeChat graphic example | Shows high-level graphical-summary style: pastel palette, panel boundaries, icon-like blocks, and clear flow. | Redraw our method and diagnostic figures with consistent palette, line weight, and panel organization. |

## Structure to Imitate

Following the YOLO-World-style paper logic, the upgraded manuscript should
follow this structure:

1. Abstract
   - One paragraph.
   - Problem, method, exact evidence, limitation.
   - No SOTA claim.
2. Introduction
   - UAV traffic-perception problem.
   - Why small objects are difficult.
   - Why lightweight YOLO needs high-resolution prediction.
   - Why static P2 can fail.
   - Contributions with CSGate as a bounded partial-repair method.
3. Related Work
   - UAV traffic and aerial object detection datasets.
   - Small/tiny object detection and scale-aware evaluation.
   - Feature pyramids and high-resolution prediction heads.
   - Lightweight YOLO and attention/fusion methods.
   - Position of this study.
4. Method
   - Overall framework figure.
   - Static P2 and cost-aware problem formulation.
   - Evidence-bounded selection rule.
   - ScaleGate as negative/mixed first-cycle evidence.
   - CSGate with equations and structural figure.
5. Experiments
   - Dataset and setup.
   - Main VisDrone comparison.
   - UAVDT boundary comparison.
   - Ablation and scale diagnostics.
   - Speed and complexity.
   - Qualitative and failure-case analysis.
6. Discussion
   - What the evidence proves.
   - What the evidence does not prove.
   - Why CSGate is useful but bounded.
7. Conclusion
   - Concise, evidence-bounded, no universal superiority.

## Figure System Target

The paper should move from ordinary generated plots to a coherent figure system:

| Figure | Target Role | Required Upgrade |
| --- | --- | --- |
| Fig. 1 | Graphical method overview | Redraw as a two-column, high-level graphical abstract with pastel blocks, subpanels, and clear CSGate route. |
| Fig. 2 | CSGate module | Redraw as a clean module schematic with \(F_2\), \(F_3\), alignment, gate, bounded residual, and output. |
| Fig. 3 | Evidence-flow / claim-boundary diagram | Show static P2 gain on VisDrone, failure on UAVDT, ScaleGate negative result, and CSGate partial repair. |
| Fig. 4 | Scale-wise diagnostics | Redraw recall/AP plots in the new style, with consistent color and typography. |
| Fig. 5 | Accuracy-efficiency trade-off | Redraw bubble/scatter plot with model families and CSGate highlighted. |
| Fig. 6 | Qualitative comparison | Use clean image grids with consistent labels, not raw YOLO batch images if possible. |
| Fig. 7 | Failure cases | Use a taxonomy figure: tiny distant objects, dense occlusion, and class ambiguity. |

## Immediate Execution Order

1. Use `yoloworld_cvpr2024_benchmark_study.md` as the primary structural and
   figure-role guide.
2. Redraw method overview and CSGate module using a unified palette.
3. Regenerate scale and trade-off plots using the same style.
4. Replace raw qualitative YOLO batch images with curated panels if source
   detections are available.
5. Update `main_draft.tex` figure order and captions.
6. Compile PDF and run `python tools/run_ieee_audits.py`.

## Source Links

- YOLO-World CVPR 2024 page: `https://openaccess.thecvf.com/content/CVPR2024/html/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.html`
- YOLO-World CVPR 2024 PDF: `https://openaccess.thecvf.com/content/CVPR2024/papers/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.pdf`
- IEEE T-ITS: `https://ieee-itss.org/pub/t-its/`
- IEEE TGRS: `https://www.grss-ieee.org/publications/author-resources/tgrs-information-for-authors/`
- IEEE TCSVT: `https://ieee-cas.org/publication/tcsvt`
- Advisor visual reference: `https://mp.weixin.qq.com/s/ND9JbNmsg-IBL4ttNi6h0Q`
- Existing local related-work matrix: `paper/ieee_related_work_matrix.csv`

# IEEE Reviewer Risk Register

Status: living planning document. This is not manuscript text.

This register lists the main risks that an IEEE Transactions reviewer may raise against the current YOLO-VisDrone route. Each mitigation must be supported by real artifacts before it enters the final manuscript.

## Summary

| Risk Area | Current Risk | Severity | Current Mitigation Status |
| --- | --- | --- | --- |
| Target fit | Exact IEEE Transactions journal is not finalized | High | T-ITS is the leading direction; advisor confirmation pending |
| Novelty | Static P2/960/attention is incremental | High | ScaleGate failed as main method; CSGate is the bounded adaptive-P2/P3 candidate |
| Generalization | Static P2 does not transfer to UAVDT | High | UAVDT boundary evidence is complete; CSGate partially repairs the static-P2 degradation but remains below stronger references |
| Larger model comparison | YOLO11s-960 is stronger in absolute accuracy | High | Narrative reframed as lightweight trade-off |
| Small-object proof | Official AP-small is unavailable | Medium | Scale-wise recall/precision and local scale-bin AP are ready |
| Stability | Most results are single seed | Medium | Multi-seed remains optional/needed for stronger claims |
| Literature coverage | Direct SOTA comparison is not yet sufficient | Medium | 25-paper seed matrix exists; final fair-comparison table pending |
| Reproducibility | Many artifacts exist but final `main.tex` is not assembled | Medium | Audit runner and evidence map are ready |
| Server continuity | Long server runs can be interrupted or only partially synced | Low | Current ScaleGate/CSGate runs are complete; guarded sync remains the only result intake path for future runs |

## Detailed Risks and Actions

| ID | Reviewer Concern | Why It Matters | Current Evidence | Mitigation Before Submission | Do Not Do |
| --- | --- | --- | --- | --- | --- |
| R1 | The paper does not clearly match the selected IEEE Transactions scope | IEEE venues expect a precise community framing | `paper/ieee_target_journal_analysis.md` | Confirm T-ITS/TGRS/other exact target with advisor; adapt title, abstract, related work, and datasets accordingly | Do not write a generic YOLO paper without a venue-specific framing |
| R2 | The method is only a combination of common YOLO tweaks | Incremental module stacking is weak for Transactions | P2/CA/960 evidence; TOFC mixed evidence; ScaleGate negative evidence; CSGate Route B/C evidence | Make the novelty hinge on cross-scale P2/P3 consistency and bounded repair; explicitly acknowledge Route A failure | Do not present CoordAttention, TOFC, ScaleGate, or input resolution as major novelty if metrics do not support it |
| R3 | Cross-dataset generalization is weak or negative | Single-dataset validation is fragile, and static P2 fails on UAVDT | VisDrone complete; UAVDT static-P2 boundary complete; CSGate partial-repair evidence complete | Use UAVDT honestly as a validity-boundary test and present CSGate only as partial repair, not general superiority | Do not claim generalization from VisDrone or hide the UAVDT static-P2 degradation |
| R4 | Larger models outperform the proposed lightweight model | Reviewers may reject absolute superiority claims | YOLO11s-960 best mAP50/mAP50-95 and strongest small-bin AP | Position around accuracy-efficiency trade-offs; report parameters, FLOPs, weight size, latency, and scale diagnostics | Do not claim the nano model is best overall |
| R5 | Small-object improvement is not directly proven | Overall mAP can hide small-object behavior | `ieee_scale_results_visdrone.csv`; `ieee_scale_ap_results_visdrone.csv` | Use scale-wise recall/precision and local scale-bin AP; keep official AP wording locked | Do not call local scale-bin AP official AP-small |
| R6 | Local AP metric may be questioned | Custom diagnostics need clear definitions | `tools/evaluate_scale_ap.py`; `paper/ieee_scale_ap_protocol.md` | Explain scale-bin policy, thresholds, and limitations; optionally add official-compatible AP evaluator later | Do not mix local AP with official benchmark AP in one table |
| R7 | Results may be seed-sensitive | Small gains can be random | Current results are mostly seed 42 | If compute allows, repeat key baseline and final method with seeds 43/44 | Do not state robustness without repeated evidence |
| R8 | Baseline comparison may be insufficient | IEEE reviewers expect recent relevant methods | `paper/ieee_related_work_matrix.csv` | Separate reproduced baselines from literature-only reported results; add fair comparisons where feasible | Do not merge literature-reported numbers with local reproduced numbers as if identical |
| R9 | Qualitative figures may look anecdotal | Figures need to support, not replace, metrics | Existing qualitative/failure figures and figure manifest | Use figures only to explain dense occlusion, tiny distant targets, and class ambiguity | Do not use qualitative examples as proof of superiority |
| R10 | The final manuscript may overclaim in abstract/conclusion | Abstract and conclusion are high-risk sections | Claim scanner and section draft pack exist | Write title, abstract, contribution list, and conclusion last after final results | Do not draft final-facing `main.tex` before evidence gates are settled |
| R11 | Server-side experiments may be incomplete or inaccessible | Partial logs cannot support claims | Guarded sync/status tools; completed ScaleGate/CSGate histories | Use only complete synced runs with `results.csv`, `args.yaml`, logs, and `best.pt` | Do not manually copy partial metrics into tables |
| R12 | The adaptive module may fail to improve the key baselines | A negative adaptive result can block a method-paper claim | ScaleGate rejection audit; CSGate Route B/C and Route A failure audit | Present ScaleGate as negative evidence and CSGate as bounded partial repair; keep limitations visible | Do not force a positive title, abstract, or conclusion around weak or mixed evidence |

## Current Strong Points

- VisDrone baseline and ablation suite is traceable to local run directories.
- Speed, complexity, scale-wise recall/precision, and local scale-bin AP are all available for completed 960-input models.
- YOLO11n-P2-960 has a defensible small-object diagnostic gain over YOLO11n-960.
- UAVDT has already exposed the static-P2 transfer boundary, which strengthens the motivation for adaptive P2 rather than leaving the paper single-dataset.
- The project now has guardrails against unsupported TOFC, ScaleGate, official AP-small, cross-dataset, and best-performance claims.

## Current Blocking Items

| Blocker | Required Evidence |
| --- | --- |
| CSGate as final named method | Advisor approval that the bounded partial-repair claim is strong enough for the target journal |
| Cross-dataset adaptive-method validation | Completed CSGate audit supports partial repair only; no universal superiority claim |
| Official AP-small wording | Official or fully compatible AP-small/AP-medium/AP-large evaluator |
| Final IEEE manuscript | Exact target journal, final method decision, complete evidence tables, verified references |

## Recommended Reviewer-Proof Narrative

The safest current narrative is:

> This work presents an evidence-bounded study and redesign of high-resolution lightweight YOLO for UAV traffic small-object detection. The completed VisDrone results show that a P2 high-resolution prediction branch improves several small-object diagnostics for YOLO11n, while UAVDT shows that static P2 does not transfer under the completed setting. ScaleGate is kept as an informative negative adaptive-gate result, and CSGate is framed as a bounded partial repair rather than a universal or state-of-the-art detector.

This narrative should be strengthened only if new complete experiments support stronger claims.

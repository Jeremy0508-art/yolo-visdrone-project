# IEEE Reviewer Risk Register

Status: living planning document. This is not manuscript text.

This register lists the main risks that an IEEE Transactions reviewer may raise against the current YOLO-VisDrone route. Each mitigation must be supported by real artifacts before it enters the final manuscript.

## Summary

| Risk Area | Current Risk | Severity | Current Mitigation Status |
| --- | --- | --- | --- |
| Target fit | Exact IEEE Transactions journal is not finalized | High | T-ITS is the leading direction; advisor confirmation pending |
| Novelty | P2/960/attention may look incremental | High | TOFC candidate exists structurally; result pending |
| Generalization | Evidence is still VisDrone-only | High | UAVDT config/converter ready; raw data and runs pending |
| Larger model comparison | YOLO11s-960 is stronger in absolute accuracy | High | Narrative reframed as lightweight trade-off |
| Small-object proof | Official AP-small is unavailable | Medium | Scale-wise recall/precision and local scale-bin AP are ready |
| Stability | Most results are single seed | Medium | Multi-seed remains optional/needed for stronger claims |
| Literature coverage | Direct SOTA comparison is not yet sufficient | Medium | 25-paper seed matrix exists; final fair-comparison table pending |
| Reproducibility | Many artifacts exist but final `main.tex` is not assembled | Medium | Audit runner and evidence map are ready |
| Server continuity | Remote status check is currently unstable | Medium | Local work continues; guarded sync remains the only result intake path |

## Detailed Risks and Actions

| ID | Reviewer Concern | Why It Matters | Current Evidence | Mitigation Before Submission | Do Not Do |
| --- | --- | --- | --- | --- | --- |
| R1 | The paper does not clearly match the selected IEEE Transactions scope | IEEE venues expect a precise community framing | `paper/ieee_target_journal_analysis.md` | Confirm T-ITS/TGRS/other exact target with advisor; adapt title, abstract, related work, and datasets accordingly | Do not write a generic YOLO paper without a venue-specific framing |
| R2 | The method is only a combination of common YOLO tweaks | Incremental module stacking is weak for Transactions | P2/CA/960 evidence; TOFC code and YAML build | Use TOFC only if real results support it; otherwise frame as a systematic lightweight high-resolution analysis | Do not present CoordAttention or input resolution as major novelty if metrics do not support it |
| R3 | Cross-dataset generalization is missing | Single-dataset validation is fragile | VisDrone complete; UAVDT setup ready | Convert UAVDT and run at least YOLO11n-960 and YOLO11n-P2-960, plus final method if validated | Do not claim generalization beyond VisDrone |
| R4 | Larger models outperform the proposed lightweight model | Reviewers may reject absolute superiority claims | YOLO11s-960 best mAP50/mAP50-95 and strongest small-bin AP | Position around accuracy-efficiency trade-offs; report parameters, FLOPs, weight size, latency, and scale diagnostics | Do not claim the nano model is best overall |
| R5 | Small-object improvement is not directly proven | Overall mAP can hide small-object behavior | `ieee_scale_results_visdrone.csv`; `ieee_scale_ap_results_visdrone.csv` | Use scale-wise recall/precision and local scale-bin AP; keep official AP wording locked | Do not call local scale-bin AP official AP-small |
| R6 | Local AP metric may be questioned | Custom diagnostics need clear definitions | `tools/evaluate_scale_ap.py`; `paper/ieee_scale_ap_protocol.md` | Explain scale-bin policy, thresholds, and limitations; optionally add official-compatible AP evaluator later | Do not mix local AP with official benchmark AP in one table |
| R7 | Results may be seed-sensitive | Small gains can be random | Current results are mostly seed 42 | If compute allows, repeat key baseline and final method with seeds 43/44 | Do not state robustness without repeated evidence |
| R8 | Baseline comparison may be insufficient | IEEE reviewers expect recent relevant methods | `paper/ieee_related_work_matrix.csv` | Separate reproduced baselines from literature-only reported results; add fair comparisons where feasible | Do not merge literature-reported numbers with local reproduced numbers as if identical |
| R9 | Qualitative figures may look anecdotal | Figures need to support, not replace, metrics | Existing qualitative/failure figures and figure manifest | Use figures only to explain dense occlusion, tiny distant targets, and class ambiguity | Do not use qualitative examples as proof of superiority |
| R10 | The final manuscript may overclaim in abstract/conclusion | Abstract and conclusion are high-risk sections | Claim scanner and section draft pack exist | Write title, abstract, contribution list, and conclusion last after final results | Do not draft final-facing `main.tex` before evidence gates are settled |
| R11 | Server-side experiments may be incomplete or inaccessible | Partial logs cannot support claims | Guarded sync/status tools; latest SSH status check failed | Use only complete synced runs with `results.csv`, `args.yaml`, logs, and `best.pt` | Do not manually copy partial metrics into tables |

## Current Strong Points

- VisDrone baseline and ablation suite is traceable to local run directories.
- Speed, complexity, scale-wise recall/precision, and local scale-bin AP are all available for completed 960-input models.
- YOLO11n-P2-960 has a defensible small-object diagnostic gain over YOLO11n-960.
- The project now has guardrails against unsupported TOFC, UAVDT, official AP-small, and best-performance claims.

## Current Blocking Items

| Blocker | Required Evidence |
| --- | --- |
| TOFC as final method | Complete TOFC VisDrone run, refreshed speed/complexity, scale-wise recall/precision, and local scale-bin AP |
| Cross-dataset validation | Converted UAVDT plus completed baseline and method runs |
| Official AP-small wording | Official or fully compatible AP-small/AP-medium/AP-large evaluator |
| Final IEEE manuscript | Exact target journal, final method decision, complete evidence tables, verified references |

## Recommended Reviewer-Proof Narrative

The safest current narrative is:

> This work presents an evidence-bounded study of high-resolution lightweight YOLO design for UAV traffic small-object detection. The completed VisDrone results show that a P2 high-resolution prediction branch improves small-object diagnostics for YOLO11n, while larger YOLO11s remains stronger in absolute accuracy. The contribution is therefore framed as a reproducible accuracy-efficiency and scale-behavior analysis, with TOFC and UAVDT reserved for final validation before any stronger method or generalization claims.

This narrative should be strengthened only if TOFC and UAVDT results support it.

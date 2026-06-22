# IEEE Second-Cycle Method Backlog

Status: second-cycle design backlog and selected-candidate record. This
document must not be cited as experimental evidence. It records why the project
moves beyond ScaleAwareP2Gate and why CSGate is the next controlled candidate.

## Purpose

The current evidence already shows why a static P2-centered paper is risky:
YOLO11n-P2-960 improves several VisDrone small-object diagnostics, but it is
weaker than YOLO11n-960, YOLOv8n-960, and YOLO11s-960 on UAVDT. ScaleAwareP2Gate
was the first adaptive-P2 response to this boundary. Its completed VisDrone and
UAVDT evidence failed the predeclared main-method routes, so the next step is a
targeted second-cycle method, not a forced positive interpretation.

## Decision Trigger

This backlog is now open because all of the following are complete:

1. ScaleGate VisDrone run reaches 100 epochs and is synced locally.
2. ScaleGate UAVDT run reaches 100 epochs and is synced locally.
3. Speed, complexity, scale-wise recall/precision, and local scale-bin AP are
   refreshed for ScaleGate.
4. `paper/ieee_scalegate_result_gate_audit.md` reports
   `OPEN_FOR_POST_RESULT_INTEGRATION`.
5. `paper/ieee_scalegate_method_decision_audit.md` has applied the fixed A/B/C
   acceptance routes.
6. `paper/ieee_method_selection_protocol.md` has been applied.
7. `python tools/run_ieee_audits.py` has passed without missing evidence.

Do not start or interpret second-cycle training from partial CSGate metrics.
CSGate has no paper-facing performance claim until complete runs and audits
exist.

## Failure-Mode Mapping

| Observed ScaleGate outcome | Likely problem | Preferred second-cycle direction |
| --- | --- | --- |
| VisDrone improves slightly, UAVDT remains below static P2 and far below YOLO11n-960 | P2 is still dataset-distribution sensitive and self-gating is insufficient | Cross-scale consistency gate between P2 and P3/P4 |
| Aggregate mAP improves, small-bin AP/recall does not | Gate is optimizing non-target scales | Scale-conditioned feature selection with explicit small-object route |
| VisDrone does not improve over static P2 | Gate is too weak or poorly placed | Move adaptation into P2-P3 fusion instead of post-P2 modulation |
| UAVDT improves, VisDrone degrades | Gate suppresses useful tiny-object details | Add scale-aware lower bound or dual-path small-object preservation |
| Accuracy improves but latency/FLOPs becomes unattractive | Module is too expensive for lightweight claim | Slim the adaptive block or restrict it to one projection path |

## Candidate E: Cross-Scale P2-P3 Consistency Gate

Status: selected second-cycle candidate.

Implementation:

- Source: `src/models/attention/cross_scale_p2_p3_gate.py`
- Model config: `configs/models/yolo11n_p2_csgate.yaml`
- VisDrone train config: `configs/train/yolo11n_p2_csgate_960.yaml`
- UAVDT train config: `configs/train/yolo11n_p2_csgate_960_uavdt.yaml`
- Launcher: `tools/start_ieee_csgate_queue.sh`

### Motivation

Static P2 uses shallow high-resolution features, while deeper P3/P4 features
contain stronger semantics. UAVDT degradation may indicate that shallow P2
features become noisy when small/tiny object density is lower or categories are
more homogeneous. A consistency gate can use P3 context to decide how much P2
detail should enter the detection head.

### Structure

```text
P2 feature -> local projection ----\
                                     -> consistency gate -> adapted P2 -> Detect
P3 feature -> upsample + projection /
```

Suggested formulation:

\[
A_2 = \sigma(f([P_2, \mathrm{Up}(P_3)])), \qquad
\hat{P}_2 = P_2 + \lambda A_2 \odot (g(P_2) - h(\mathrm{Up}(P_3))).
\]

The intent is not to replace P2 with P3, but to suppress P2 activations that
are inconsistent with nearby semantic context.

### Required Ablations

| Run | Purpose |
| --- | --- |
| YOLO11n-P2-960 | static P2 baseline |
| YOLO11n-P2-ScaleGate-960 | first adaptive candidate |
| YOLO11n-P2-CSGate-960 | cross-scale consistency gate |
| YOLO11n-960 | resolution-matched baseline |
| YOLO11s-960 | capacity reference |

## Candidate F: Scale-Conditioned Feature Selector

### Motivation

If ScaleGate improves aggregate mAP but not small-bin diagnostics, the detector
may still be optimizing medium or large objects. A scale-conditioned selector
should explicitly route feature emphasis according to estimated object-scale
evidence rather than applying one gate to all P2 locations.

### Structure

Use a lightweight scale prior predicted from the feature pyramid:

```text
P2/P3/P4 pooled descriptors -> scale logits -> feature-selection weights
P2, P3, P4 feature paths -> weighted shallow/deep response -> Detect
```

Suggested formulation:

\[
w = \mathrm{softmax}(q([s_2, s_3, s_4])), \qquad
\hat{P}_2 = P_2 + w_2 r_2(P_2) + w_3 r_3(\mathrm{Up}(P_3)).
\]

This candidate is more invasive than ScaleGate and should be launched only if
ScaleGate reveals that a single post-P2 gate is too coarse.

## Candidate G: Small-Object Preserving Training Policy v2

### Motivation

If architectural changes remain weak, the failure may come from assignment or
augmentation rather than feature design. The earlier SmallObjAug evidence was
not strong enough to be a main contribution, but a second version can be used
as a controlled companion to a validated architecture.

### Controlled Variables

- conservative scale jitter;
- later or earlier mosaic close, chosen from real ablation;
- small-object-density image sampling;
- copy-paste only if label quality and occlusion behavior are audited;
- no changes to validation preprocessing.

This route is not enough for an IEEE method claim by itself unless it is paired
with strong diagnostic and cross-dataset evidence.

## Launch Rules

Do not launch all candidates blindly. Choose one candidate from the failure
mode:

1. If UAVDT is the main problem, start Candidate E. This is the current route.
2. If small-bin diagnostics are the main problem, start Candidate F.
3. If architecture is stable but gains are small, test Candidate G as a paired
   training-policy ablation.

Every launched candidate must use matched input size, epoch count, seed,
dataset split, optimizer policy, and result-audit pipeline. Partial runs remain
progress evidence only.

## Manuscript Implication

If a second-cycle method succeeds, the final manuscript can become a true
method paper centered on adaptive high-resolution prediction. If all
second-cycle candidates fail, the manuscript should not be forced into a
method-success story. The honest route would be a boundary-analysis paper or a
lower-risk journal route, using the completed evidence to explain when static
and adaptive high-resolution prediction are useful or harmful.

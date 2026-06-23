# CrossScaleP2P3ConsistencyGate Method Section Draft

Status: completed bounded method-candidate draft. This file defines the CSGate
candidate and records the claim boundary supported by the audited results.

## Motivation

Completed VisDrone and UAVDT evidence shows that a static P2 branch is useful
for some VisDrone small-object diagnostics but does not transfer reliably to
UAVDT under the current 960-input setting. The completed ScaleAwareP2Gate run
also fails the predeclared main-method decision routes: self-conditioned P2
modulation does not preserve the audited small-object diagnostics and does not
repair the UAVDT boundary.

CSGate is therefore designed from the observed failure mode. Instead of
modulating P2 from P2 alone, it uses adjacent P3 semantic context to condition
the shallow high-resolution response.

## Module Definition

Let \(F_2 \in \mathbb{R}^{C_2 \times H \times W}\) be the fused P2 feature and
let \(F_3 \in \mathbb{R}^{C_3 \times H/2 \times W/2}\) be the adjacent P3
feature. After nearest-neighbor alignment, CSGate computes

\[
C_2 = g_2(F_2), \qquad C_3 = g_3(\mathrm{Up}(F_3)),
\]

where \(g_2\) is a local depthwise-separable projection and \(g_3\) is a
\(1\times1\) projection. The cross-scale consistency map is

\[
A_{23} = \sigma(q([C_2, C_3])),
\]

where \(q\) is a lightweight gate and \([\cdot,\cdot]\) denotes channel-wise
concatenation. The adapted P2 feature is

\[
\tilde{F}_2 = F_2 + \lambda A_{23} \odot (C_2 - C_3), \qquad
\lambda = \Delta_{\max}\tanh(\eta).
\]

The scalar \(\eta\) is initialized to zero. Thus \(\lambda=0\) at
initialization and the candidate starts from the static P2 path with a bounded
learnable correction.

## Insertion Point

The current implementation is defined in
`src/models/attention/cross_scale_p2_p3_gate.py` and used by
`configs/models/yolo11n_p2_csgate.yaml`. The training configs are:

- `configs/train/yolo11n_p2_csgate_960.yaml`
- `configs/train/yolo11n_p2_csgate_960_uavdt.yaml`

The server launcher is `tools/start_ieee_csgate_queue.sh`. The strict UAVDT
100-epoch rerun is represented locally by
`configs/train/yolo11n_p2_csgate_960_uavdt_full100.yaml`.

## Claim Boundary

The completed audit permits bounded CSGate claims, but still forbids:

- CSGate improves cross-dataset robustness.
- CSGate is state-of-the-art.
- CSGate outperforms YOLO11n-960, YOLOv8n-960, or YOLO11s-960 on UAVDT.
- CSGate dominates every small-object diagnostic.

The allowed post-result statement is:

> CSGate is a bounded cross-scale adaptation candidate that conditions P2 detail
> on adjacent P3 semantic context. It improves VisDrone aggregate accuracy and
> small-object recall and partially repairs the UAVDT static-P2 degradation, but
> it remains below the strongest UAVDT baselines and cannot support a
> cross-dataset superiority claim.

## Required Evidence Before Manuscript Use

| Evidence | Required source |
| --- | --- |
| Model builds | `configs/models/yolo11n_p2_csgate.yaml`; server smoke test |
| VisDrone accuracy | `runs/detect/yolo11n_p2_csgate_960_visdrone/results.csv` after 100 epochs |
| UAVDT accuracy | `runs/detect/yolo11n_p2_csgate_960_uavdt_full100/results.csv` after 100 epochs |
| Complexity | `paper/tables/model_complexity.csv` after CSGate export |
| Speed | `paper/tables/speed_results.csv` after CSGate benchmark |
| Scale diagnostics | Refreshed VisDrone scale recall/precision and local scale-bin AP outputs |
| Method decision | `paper/ieee_csgate_method_decision_audit.md`; accepted routes B and C, route A not accepted |

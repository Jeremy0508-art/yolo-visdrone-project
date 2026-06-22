# CrossScaleP2P3ConsistencyGate Method Section Draft

Status: second-cycle method-text draft only. This file defines the CSGate
candidate and its claim boundary. It contains no performance claim.

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

The server launcher is `tools/start_ieee_csgate_queue.sh`.

## Claim Boundary

Do not write any of the following statements until complete VisDrone and UAVDT
CSGate runs are synced and audited:

- CSGate improves VisDrone detection.
- CSGate improves small-object AP or recall.
- CSGate repairs the UAVDT degradation of static P2.
- CSGate improves cross-dataset robustness.
- CSGate is the final proposed method.

The allowed pre-result statement is:

> CSGate is a second-cycle adaptive high-resolution candidate that conditions
> P2 detail on adjacent P3 semantic context. It is result-locked until complete
> audited VisDrone and UAVDT runs are available.

## Required Evidence Before Manuscript Use

| Evidence | Required source |
| --- | --- |
| Model builds | `configs/models/yolo11n_p2_csgate.yaml`; server smoke test |
| VisDrone accuracy | `runs/detect/yolo11n_p2_csgate_960_visdrone/results.csv` after 100 epochs |
| UAVDT accuracy | `runs/detect/yolo11n_p2_csgate_960_uavdt/results.csv` after 100 epochs |
| Complexity | `paper/tables/model_complexity.csv` after CSGate export |
| Speed | `paper/tables/speed_results.csv` after CSGate benchmark |
| Scale diagnostics | Refreshed VisDrone scale recall/precision and local scale-bin AP outputs |
| Method decision | Future CSGate decision audit or manually reviewed gate derived from the same acceptance discipline |


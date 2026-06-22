# ScaleAwareP2Gate Method Section Draft

Status: completed first-cycle method-text draft. ScaleAwareP2Gate now has
complete VisDrone and UAVDT evidence, but the generated method-decision audit
rejects it as the main method. Use this file only as background for a
mixed/negative ablation or for motivating the second-cycle CSGate route.

## Motivation

The completed evidence shows that a static P2 branch is useful for VisDrone
small-object diagnostics but degrades on UAVDT under the matched 960-input
setting. This suggests that the problem is not simply whether shallow
high-resolution features are useful, but whether the detector should rely on
them with the same strength across datasets and object-scale distributions.

ScaleAwareP2Gate is designed as a lightweight adaptive layer for the P2 branch.
It keeps the plain P2 behavior at initialization and gradually learns bounded
feature modulation from the training data. The design goal is conservative:
retain small-object detail when it is useful, while avoiding an unconditional
amplification of shallow high-resolution features.

## Module Definition

Let \(F_2 \in \mathbb{R}^{C \times H \times W}\) denote the fused P2 feature
map before the high-resolution detection path continues to the four-scale
prediction head. ScaleAwareP2Gate first computes a local context tensor:

\[
L_2 = \phi(\mathrm{BN}(\mathrm{Conv}_{1\times1}(
      \phi(\mathrm{BN}(\mathrm{DWConv}_{3\times3}(F_2)))))),
\]

where \(\mathrm{DWConv}_{3\times3}\) is a depthwise convolution and \(\phi\)
denotes the SiLU activation. The local context preserves the P2 spatial
resolution while allowing each channel to collect neighborhood evidence.

A channel gate is obtained from global average pooled local context:

\[
G_c = \sigma(\mathrm{Conv}_{1\times1}(
      \phi(\mathrm{Conv}_{1\times1}(\mathrm{GAP}(L_2))))),
\]

where \(\sigma\) is the sigmoid function. A spatial gate is computed from the
channel-average and channel-maximum maps of \(L_2\):

\[
G_s = \sigma(\mathrm{Conv}_{5\times5}(
      [\mathrm{Avg}_c(L_2), \mathrm{Max}_c(L_2)])).
\]

The two gates are multiplied to obtain a spatial-channel modulation tensor:

\[
M_2 = G_s \odot G_c.
\]

The final output is an identity-initialized bounded residual modulation:

\[
\hat{F}_2 = F_2 + \delta L_2 \odot M_2,\qquad
\delta = \Delta_{\max}\tanh(\gamma),
\]

where \(\gamma\) is a learnable scalar initialized to zero and
\(\Delta_{\max}=0.5\) in the current configuration. Therefore,
\(\delta=0\) at initialization and \(\hat{F}_2=F_2\). The module starts from
the static P2 model and learns only a bounded deviation from it.

## Insertion Point

The module is inserted after the P2 feature-fusion block in
`configs/models/yolo11n_p2_scalegate.yaml`. The resulting model keeps the
four-scale detection structure \(P2/P3/P4/P5\), with the Detect head receiving
features from layers `[20, 23, 26, 29]` in the current YAML graph.

## Completed Evidence Boundary

The completed ScaleGate evidence may be discussed only as mixed or negative
adaptive-gate evidence. Do not write any of the following statements:

- ScaleAwareP2Gate improves VisDrone detection.
- ScaleAwareP2Gate repairs the UAVDT degradation of static P2.
- ScaleAwareP2Gate improves cross-dataset robustness.
- ScaleAwareP2Gate is the final proposed method.

The allowed post-result statement is:

> ScaleAwareP2Gate is an identity-initialized, bounded adaptive gate inserted
> after the P2 feature-fusion block. In the completed audit it remains
> mixed/negative evidence and motivates a stronger cross-scale candidate rather
> than becoming the main method.

## Evidence Sources

| Evidence | Required source |
| --- | --- |
| Model builds | `configs/models/yolo11n_p2_scalegate.yaml`; `tools/check_ieee_phase1_artifacts.py` |
| VisDrone accuracy | `runs/detect/yolo11n_p2_scalegate_960_visdrone/results.csv` after 100 epochs |
| UAVDT accuracy | `runs/detect/yolo11n_p2_scalegate_960_uavdt/results.csv` after 100 epochs |
| Complexity | `paper/tables/model_complexity.csv` after `tools/export_paper_tables.py` |
| Speed | `paper/tables/speed_results.csv` after `tools/benchmark_speed.py` |
| Scale diagnostics | `paper/tables/ieee_scale_results_visdrone.csv`; `paper/tables/ieee_scale_ap_results_visdrone.csv` |
| Method decision | `paper/ieee_scalegate_method_decision_audit.md` |

This draft should not be moved into a final IEEE manuscript as the proposed
method section. It can be summarized as an ablation or failure-mode analysis
only if the surrounding text preserves the audit decision.

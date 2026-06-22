# IEEE Transactions Method Redesign Plan

Status: active design document for the new IEEE route. This document replaces
the "package the current P2 result" mindset with a new method-and-evidence
route. It must not be cited as an experimental result source.

Current execution status: the ScaleGate VisDrone and UAVDT runs are complete,
synced, and audited. The predeclared method-decision audit reports
`DO_NOT_USE_SCALEGATE_AS_MAIN_METHOD`, so ScaleGate must remain a mixed or
negative adaptive-gate ablation. The active second-cycle method route is
`CrossScaleP2P3ConsistencyGate` (CSGate), which has code/config evidence only
and must not receive performance claims until complete real runs exist.

## 1. Evidence Diagnosis

The completed VisDrone and UAVDT evidence does not support a universal
"P2 is better" claim.

- On VisDrone, higher input resolution is the dominant source of the gain, and
  a P2 branch gives a modest additional benefit under the matched 960 setting.
- Scale diagnostics on VisDrone show that shallow high-resolution prediction
  is useful for small-object recall and local small-bin AP.
- On UAVDT, the completed YOLO11n-P2-960 run is weaker than YOLO11n-960,
  YOLOv8n-960, and YOLO11s-960.
- UAVDT contains only vehicle categories in the current project setting, while
  VisDrone contains more classes and more severe pedestrian/non-motor/tiny
  object cases. This makes P2 benefit dataset- and scale-distribution-dependent.

Conclusion: the next paper-worthy direction is not another static P2 head, but
an adaptive high-resolution mechanism that can preserve small-object detail
when it is useful and avoid over-amplifying shallow noise when it is not.

## 2. New Research Thesis

Working thesis:

> Lightweight UAV detectors need high-resolution detail for tiny objects, but
> static shallow prediction can be brittle across datasets. A scale-aware
> high-resolution gate can make the P2 branch adaptive while keeping the model
> in the nano-scale efficiency regime.

The paper should be rewritten around this question:

> Can a lightweight YOLO detector use high-resolution P2 features adaptively,
> improving VisDrone small-object evidence without reproducing the UAVDT
> degradation observed for a static P2 branch?

## 3. Candidate Methods

Completed first-cycle candidate:

- Name: `ScaleAwareP2Gate`
- Model config: `configs/models/yolo11n_p2_scalegate.yaml`
- VisDrone train config: `configs/train/yolo11n_p2_scalegate_960.yaml`
- UAVDT train config: `configs/train/yolo11n_p2_scalegate_960_uavdt.yaml`
- Source module: `src/models/attention/scale_aware_p2_gate.py`
- Decision: rejected as the main method by
  `paper/ieee_scalegate_method_decision_audit.md`

Design:

- Insert a lightweight gate after the P2 feature-fusion block.
- Use local depthwise context, channel context, and spatial saliency to modulate
  high-resolution P2 features.
- Initialize the learnable gain to zero, making the block identity at epoch 0.
- Bound the modulation strength so the block cannot immediately destabilize
  the P2 branch.

Observed decision evidence:

- VisDrone best mAP50-95 improves slightly over static P2, but small-object
  diagnostic preservation fails under the fixed rule.
- UAVDT best mAP50-95 does not repair the static-P2-to-YOLO11n gap.
- Therefore, ScaleGate can motivate the next design but cannot be placed in
  the title, abstract, contribution list, or conclusion as the proposed method.

Active second-cycle candidate:

- Name: `CrossScaleP2P3ConsistencyGate`
- Model config: `configs/models/yolo11n_p2_csgate.yaml`
- VisDrone train config: `configs/train/yolo11n_p2_csgate_960.yaml`
- UAVDT train config: `configs/train/yolo11n_p2_csgate_960_uavdt.yaml`
- Source module: `src/models/attention/cross_scale_p2_p3_gate.py`
- Server launcher: `tools/start_ieee_csgate_queue.sh`

Design:

- Use neighboring P3 semantic context to condition the shallow P2 response.
- Insert the module after P2/P3 alignment rather than applying a purely
  self-conditioned P2 gate.
- Initialize the learnable gain to zero, keeping the branch identity-like at
  epoch 0.
- Keep CSGate result-locked until complete 100-epoch VisDrone and UAVDT runs,
  refreshed speed/complexity, and scale diagnostics exist.

## 4. Required Experiment Matrix

Core matched experiments:

| ID | Dataset | Model | Input | Purpose | Status |
| --- | --- | --- | ---: | --- | --- |
| vis_yolo11n_960 | VisDrone | YOLO11n | 960 | matched baseline | complete |
| vis_yolo11n_p2_960 | VisDrone | YOLO11n-P2 | 960 | static P2 baseline | complete |
| vis_yolo11n_p2_scalegate_960 | VisDrone | YOLO11n-P2-ScaleGate | 960 | first adaptive candidate | complete, rejected as main method |
| vis_yolo11n_p2_csgate_960 | VisDrone | YOLO11n-P2-CSGate | 960 | second-cycle method candidate | pending real run |
| uavdt_yolo11n_960 | UAVDT | YOLO11n | 960 | matched baseline | complete |
| uavdt_yolo11n_p2_960 | UAVDT | YOLO11n-P2 | 960 | static P2 boundary | complete |
| uavdt_yolo11n_p2_scalegate_960 | UAVDT | YOLO11n-P2-ScaleGate | 960 | first adaptive cross-dataset test | complete, rejected as main method |
| uavdt_yolo11n_p2_csgate_960 | UAVDT | YOLO11n-P2-CSGate | 960 | second-cycle cross-dataset test | pending real run |

Secondary experiments after the first two runs:

| Experiment | Purpose | Launch condition |
| --- | --- | --- |
| CSGate speed benchmark | deployment and efficiency table | after CSGate best weights are synced |
| CSGate scale-bin AP/recall | small-object mechanism evidence | after CSGate best weights are synced |
| CSGate qualitative cases | show where cross-scale adaptation helps/fails | after CSGate best weights are synced |
| CSGate 3 seeds | stability check for the final claim | only if single-seed result is competitive |

## 5. Claim Gates

No claim is allowed until all required evidence exists.

Allowed now:

- The completed evidence shows a dataset boundary for static P2.
- `ScaleAwareP2Gate` is a completed mixed/negative ablation motivated by that
  boundary.
- `CrossScaleP2P3ConsistencyGate` is a second-cycle candidate motivated by the
  ScaleGate failure mode.
- CSGate builds locally and remains result-locked.

Locked:

- Do not claim ScaleGate is the proposed method.
- Do not claim CSGate improves VisDrone.
- Do not claim CSGate fixes UAVDT.
- Do not claim cross-dataset robustness.
- Do not claim IEEE Transactions readiness.
- Do not claim SOTA.

## 6. Paper Rewrite Direction

Current ScaleGate decision:

- ScaleGate cannot support the main method claim because it fails the
  predeclared acceptance routes.
- It can remain in the manuscript only as a completed ablation that motivates
  stronger cross-scale adaptation.
- The next paper rewrite should center on CSGate only if complete CSGate
  evidence supports it. Otherwise, the honest route is a mechanism/boundary
  study or a lower-risk venue.

## 7. Second-Cycle Design Rules

ScaleGate is the first adaptive-P2 candidate, not the final paper claim. Its
completed evidence is weak or mixed under the predeclared routes, so the next
method design is chosen from the observed failure mode rather than from a
desire to preserve the current module.

| Failure mode after complete runs | Interpretation | Next design direction |
| --- | --- | --- |
| VisDrone improves but UAVDT remains worse than YOLO11n-960 | the gate helps tiny-object-heavy scenes but does not repair transfer brittleness | add stronger cross-scale consistency between P2 and P3/P4, or add a dataset-agnostic regularizer that suppresses noisy P2 activation |
| VisDrone does not improve over YOLO11n-P2-960 | the gate is too weak, misplaced, or unnecessary for the completed setting | redesign the insertion point or add explicit scale-conditioned feature selection instead of only post-P2 modulation |
| Aggregate mAP improves but small-bin AP/recall does not | the module is optimizing non-target scales | keep it as an aggregate ablation and design a small-object-specific supervision or assignment experiment |
| UAVDT improves but VisDrone degrades | the gate may suppress useful tiny-object details | tune the gate strength, test 640/960 sensitivity, or redesign around adaptive rather than suppressive P2 fusion |
| Both datasets improve but speed cost is too high | evidence supports the mechanism but not deployment | prune the gate, benchmark fused/exported models, and report the cost honestly before final claims |

The selected second-cycle direction is CSGate, because ScaleGate did not repair
the UAVDT boundary and weakened the VisDrone small-object diagnostics relative
to static P2. The goal is an IEEE-level method supported by evidence, not a
sequence of unconnected module trials.

## 8. Immediate Commands

Local build check:

```powershell
@'
from src.models.register import register_custom_modules
register_custom_modules()
from ultralytics.nn.tasks import DetectionModel
m = DetectionModel("configs/models/yolo11n_p2_csgate.yaml", nc=10)
print(sum(p.numel() for p in m.parameters()))
'@ | python -
```

Training commands for the server, wrapped by `tools/start_ieee_csgate_queue.sh`:

```bash
cd /root/autodl-tmp/yolo-visdrone-project
python tools/train_baseline.py --config configs/train/yolo11n_p2_csgate_960.yaml
python tools/train_baseline.py --config configs/train/yolo11n_p2_csgate_960_uavdt.yaml
```

These commands should be run only through the guarded queue after the server
has the current code, datasets, and dependencies.

## 9. Next Engineering Tasks

1. Sync CSGate code/config/scripts to the server.
2. Run a remote CSGate build smoke test.
3. Launch `tools/start_ieee_csgate_queue.sh` only after the smoke test passes.
4. Monitor with `tools/check_ieee_server_status.ps1`.
5. Sync only complete CSGate runs with `tools/sync_ieee_server_results.ps1`.
6. Refresh speed, complexity, scale-wise recall/precision, and local scale-bin
   AP before writing any CSGate manuscript text.
7. Apply a CSGate-specific method decision before editing the title, abstract,
   contribution list, or conclusion.

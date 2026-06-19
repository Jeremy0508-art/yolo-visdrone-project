# IEEE Transactions Experiment Gap Matrix

## Purpose

This document converts the IEEE Transactions upgrade plan into concrete experiments and evidence gates. It is intentionally stricter than the previous CEA route because IEEE Transactions reviewers will expect stronger novelty, broader validation, and cleaner separation between method effects.

No experiment result should enter the English manuscript until its run directory, command, configuration, log, weights, and metrics are available locally.

## Current Completed Evidence

| Evidence | Status | Source |
| --- | --- | --- |
| VisDrone YOLO-format dataset | Complete | `configs/dataset/visdrone.yaml` |
| YOLO11n baseline 640 | Complete | `runs/detect/baseline_yolo11n_visdrone` |
| YOLO11n baseline 960 | Complete | `runs/detect/baseline_yolo11n_960_visdrone` |
| YOLO11n-P2 640 | Complete | `runs/detect/yolo11n_p2_pretrained_visdrone` |
| YOLO11n-P2 960 | Complete | `runs/detect/yolo11n_p2_960_visdrone` |
| YOLO11n-P2-CA 640 | Complete | `runs/detect/yolo11n_p2_coordatt_visdrone` |
| YOLO11n-P2-CA 960 | Complete | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full` |
| SmallObjAug ablation | Complete | `runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone` |
| YOLOv5n / YOLOv8n / YOLO11s reference baselines | Complete | `paper/tables/main_comparison_for_paper.csv` |
| Speed and complexity tables | Complete | `paper/tables/speed_results.csv`, `paper/tables/model_complexity.csv` |
| Visual examples and failure cases | Complete for current manuscript | `paper/figures/` |

## Critical Gaps

| Priority | Gap | Why It Matters for IEEE Transactions | Required Output |
| ---: | --- | --- | --- |
| P0 | Target journal not finalized | Determines framing, datasets, and required comparisons | `paper/ieee_target_journal_analysis.md` |
| P0 | No second dataset | Single-dataset VisDrone validation is weak for Transactions-level generalization | UAVDT dataset config, converted labels, baseline/main results |
| P0 | No strong new method beyond P2/CA/960 | Current method may look like module stacking and input-size tuning | New module proposal or a more modest paper target |
| P0 | No scale-wise AP/Recall audit suitable for IEEE claims | Small-object paper must prove small-object improvement directly | `paper/tables/ieee_scale_results.csv` |
| P1 | No multi-seed stability | Single-run improvements can be dismissed as variance | 3-seed results for key baseline and main model |
| P1 | Limited SOTA comparison | Current comparisons are mostly local YOLO baselines | Related work matrix and reproducible/quoted SOTA table |
| P1 | No UAVDT speed/complexity comparison | Deployment claim should hold outside VisDrone | Cross-dataset speed/accuracy matrix |
| P2 | No official VisDrone test-dev result | Official benchmark would strengthen the paper | Optional official submission if account works |
| P2 | No IEEEtran English manuscript | Chinese/CEA manuscript cannot be submitted directly | `paper/ieee_trans/main.tex` |

## Minimum Experiment Set for a Serious IEEE Attempt

### Dataset Preparation

| ID | Task | Command/Implementation Needed | Paper Use | Status |
| --- | --- | --- | --- | --- |
| D1 | Add UAVDT dataset download/placement instructions | `paper/datasets/uavdt_setup.md` or README section | Cross-dataset validation | Pending |
| D2 | Convert UAVDT annotations to YOLO format | New script under `tools/` | Reproducible second dataset | Pending |
| D3 | Add UAVDT data config | `configs/dataset/uavdt.yaml` | Training and validation | Pending |
| D4 | Verify class mapping and split integrity | Audit script | Avoid invalid comparison | Pending |

### Core VisDrone Experiments

| ID | Experiment | Input | Epochs | Seeds | Required Evidence | Status |
| --- | --- | ---: | ---: | ---: | --- | --- |
| V1 | YOLO11n baseline | 960 | 100 | 3 total if feasible | Existing + repeat seeds | One seed complete |
| V2 | YOLO11n-P2 | 960 | 100 | 3 total if feasible | Existing + repeat seeds | One seed complete |
| V3 | YOLO11n-P2-CA | 960 | 100 | Optional repeat | Existing + maybe repeat | One seed complete |
| V4 | New method candidate | 960 | 100 | 3 total if feasible | Full run evidence | Not designed |
| V5 | YOLOv8n baseline | 960 | 100 | 1-3 | Existing + optional repeat | One seed complete |
| V6 | YOLO11s baseline | 960 | 100 | 1 | Existing is enough for capacity reference | Complete |

### UAVDT Cross-Dataset Experiments

| ID | Experiment | Input | Epochs | Purpose | Status |
| --- | --- | ---: | ---: | --- | --- |
| U1 | YOLO11n baseline | 960 | 100 | Cross-dataset lightweight baseline | Pending |
| U2 | YOLO11n-P2 | 960 | 100 | Cross-dataset P2 validation | Pending |
| U3 | New method candidate | 960 | 100 | Cross-dataset method validation | Pending |
| U4 | YOLOv8n baseline | 960 | 100 | External lightweight reference | Pending |
| U5 | YOLO11s baseline | 960 | 100 | Capacity reference | Pending |

### SOTA / Literature Comparison

| ID | Item | Use Rule | Status |
| --- | --- | --- | --- |
| S1 | TPH-YOLOv5 | Prefer reproducible run if code/data compatible; otherwise cite reported results separately and mark as literature-only | Pending |
| S2 | SOD-YOLO / SOD-YOLOv8 | Same as above | Pending |
| S3 | Recent YOLO11 UAV methods | Use as literature context; do not compare numbers unless dataset/evaluation match | Pending |
| S4 | RT-DETR or lightweight DETR reference | Run only if cost is acceptable and implementation is stable | Optional |

### Analysis and Metrics

| ID | Analysis | Implementation Needed | Required for IEEE? | Status |
| --- | --- | --- | --- | --- |
| A1 | COCO-style AP-small/AP-medium/AP-large or VisDrone-specific scale AP/Recall | `tools/evaluate_scale_groups.py` now supports `--targets-csv`; full validation run still pending | Yes |
| A2 | Density-wise performance | Count objects per image and group validation images | Recommended |
| A3 | Per-class AP table | Existing partial material can be reused | Yes |
| A4 | Speed/latency/FPS | Existing benchmark script; repeat for new models | Yes |
| A5 | Params/GFLOPs/weight size | Existing exporter; repeat for new models | Yes |
| A6 | GPU memory | Add measurement if feasible | Recommended |
| A7 | Qualitative cases | Rebuild English-labeled figures | Yes |
| A8 | Failure-case taxonomy | Convert current Chinese analysis into English categories | Recommended |

## Claim Rules

| Claim Type | Allowed Only If |
| --- | --- |
| "improves small-object detection" | Scale-wise small-object AP/Recall improves, not only total mAP |
| "lightweight" | Params/FLOPs/FPS are reported and remain meaningfully below YOLO11s-like models |
| "generalizes" | At least one additional dataset shows consistent trend |
| "outperforms SOTA" | Same dataset, same metric, comparable split, and either reproduced or directly comparable official result |
| "real-time" | FPS/latency measured on declared hardware and preprocessing/postprocessing protocol is clear |
| "attention improves performance" | Attention ablation improves over the corresponding non-attention baseline under the same input size |

## Initial Server Queue Proposal

The following queue is intentionally conservative. It avoids launching expensive experiments until dataset conversion and method design are settled.

1. Prepare UAVDT dataset and run integrity checks.
2. Run UAVDT YOLO11n-960 baseline.
3. Run UAVDT YOLO11n-P2-960.
4. Run UAVDT YOLOv8n-960 reference.
5. If the new module is designed, run VisDrone new-method quick check.
6. If quick check is promising, run full VisDrone new-method 960.
7. Repeat key VisDrone runs for seeds 43 and 44 if budget allows.
8. Run UAVDT new-method 960 if VisDrone result is promising.

## Stop / Pivot Conditions

| Condition | Action |
| --- | --- |
| New method does not beat YOLO11n-P2-960 or does not improve small-scale metrics | Do not build IEEE paper around the new module; pivot to lower-risk journal or stronger systematic analysis |
| UAVDT results do not show consistent trend | Avoid generalization claims; use UAVDT as negative/limitation analysis only |
| FPS drops below practical lightweight range | Remove real-time/lightweight deployment claim |
| YOLO11s remains much better and main method has no efficiency advantage | Reframe as diagnostic study or choose a less competitive venue |

## Immediate Next Actions

1. Build `paper/ieee_related_work_matrix.csv`.
2. Design UAVDT conversion and dataset config.
3. Draft `paper/ieee_method_design_notes.md` with 1-2 candidate modules.
4. Decide with advisor whether to invest in route B new-module experiments.

## Scale Evaluation Command

The current IEEE target list is recorded at:

```text
paper/tables/ieee_scale_eval_targets.csv
```

Full VisDrone scale-wise evaluation command:

```powershell
python tools/evaluate_scale_groups.py `
  --dataset-root data/processed/visdrone_yolo `
  --dataset-name VisDrone2019-DET `
  --split val `
  --targets-csv paper/tables/ieee_scale_eval_targets.csv `
  --output paper/tables/ieee_scale_results_visdrone.csv `
  --plot-output paper/figures/scale_analysis/ieee_scale_recall_visdrone.png `
  --device 0
```

A one-image CPU smoke check has passed and wrote ignored files under `runs/scale_group_smoke/`. Those smoke values are not valid paper results.

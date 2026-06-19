# IEEE Transactions Route Advisor Brief

## Background

The project was previously prepared for a Chinese journal route targeting 《计算机工程与应用》. That route is now paused based on the advisor's suggestion to consider an IEEE Transactions English journal.

The existing Chinese-journal work is not discarded. It provides:

- verified VisDrone training logs,
- baseline and ablation results,
- speed and complexity tables,
- qualitative figures,
- reproducibility commands,
- evidence-audit infrastructure.

However, IEEE Transactions requires a stronger contribution and broader validation than the current Chinese-journal manuscript.

## Current Technical Status

Completed evidence:

- YOLO11n / YOLO11n-960.
- YOLO11n-P2 / YOLO11n-P2-960.
- YOLO11n-P2-CA / YOLO11n-P2-CA-960.
- YOLO11n-P2-CA-SmallObjAug.
- YOLOv5n, YOLOv8n, YOLOv8n-960, YOLO11s, YOLO11s-960 reference baselines.
- Speed, complexity, per-class, scale-distribution, and qualitative analysis materials.

Important interpretation:

- YOLO11n-P2-960 is currently the best nano-scale trade-off model.
- YOLO11s-960 is much stronger in absolute accuracy.
- CoordAttention does not currently improve the 960-input P2 model.
- The IEEE paper must not claim that the lightweight method generally beats larger-capacity models.

## Recommended IEEE Target Direction

Primary candidate:

> IEEE Transactions on Intelligent Transportation Systems

Reason:

- VisDrone and UAVDT contain UAV traffic scenes.
- The project can be framed as UAV-assisted traffic perception.
- Lightweight inference and small-object detection are relevant for real-time transportation monitoring.

Secondary candidate:

> IEEE Transactions on Geoscience and Remote Sensing

Reason:

- UAV aerial imagery and remote-sensing interpretation are relevant.

Risk:

- TGRS likely needs stronger remote-sensing-specific datasets and methodological novelty.

## New Work Completed After Route Switch

| Item | Artifact |
| --- | --- |
| IEEE master plan | `paper/IEEE_TRANS_SUBMISSION_PLAN.md` |
| Target journal analysis | `paper/ieee_target_journal_analysis.md` |
| Experiment gap matrix | `paper/ieee_required_experiment_gap.md` |
| Related-work seed table | `paper/ieee_related_work_matrix.csv` |
| UAVDT dataset config | `configs/dataset/uavdt.yaml` |
| UAVDT conversion notes | `paper/datasets/uavdt_setup.md` |
| UAVDT conversion script | `scripts/convert_uavdt_to_yolo.py` |
| Generic dataset checker update | `scripts/check_dataset.py` |
| TOFC candidate module | `src/models/attention/tiny_object_feature_calibration.py` |
| TOFC model/training config | `configs/models/yolo11n_p2_tofc.yaml`, `configs/train/yolo11n_p2_tofc_960.yaml` |
| Scale-evaluation target list | `paper/tables/ieee_scale_eval_targets.csv` |
| Guarded server queue | `tools/run_ieee_server_queue.sh` |

## Proposed New Method Direction

Tentative method candidate:

> Tiny Object Feature Calibration (TOFC)

Motivation:

- P2 introduces high-resolution shallow features.
- Shallow features preserve detail but also contain background noise.
- TOFC adds lightweight local feature calibration on the P2 branch.

Structural check:

| Model | Parameters |
| --- | ---: |
| YOLO11n-P2 | 2,893,672 |
| YOLO11n-P2-TOFC | 2,895,762 |
| YOLO11n-P2-CA | 2,903,704 |

TOFC adds only about 2,090 parameters over YOLO11n-P2. This is a structural fact only; no accuracy claim is allowed until training is completed.

## Required Next Experiments

Minimum next queue:

1. Train YOLO11n-P2-TOFC-960 on VisDrone.
2. Run full VisDrone scale-wise evaluation for completed models.
3. Download and convert UAVDT.
4. Train UAVDT YOLO11n-960 baseline.
5. Train UAVDT YOLO11n-P2-960.
6. Train UAVDT YOLOv8n-960 reference.
7. If TOFC works on VisDrone, train TOFC on UAVDT.

The guarded queue script is:

```bash
RUN_TRAINING=1 RUN_SCALE=1 ./tools/run_ieee_server_queue.sh
```

UAVDT jobs require:

```bash
RUN_TRAINING=1 RUN_UAVDT=1 RUN_SCALE=1 ./tools/run_ieee_server_queue.sh
```

The script is dry-run by default to prevent accidental GPU spending.

## Advisor Decisions Needed

1. Confirm the preferred target: T-ITS, TGRS, or another IEEE Transactions journal.
2. Confirm whether a new module such as TOFC is acceptable as the method direction.
3. Confirm whether UAVDT is an acceptable second dataset.
4. Confirm whether the project can spend GPU time on multi-seed experiments.
5. Confirm author order, affiliation, funding, and code/data release policy later.

## Current Recommendation

Do not start writing the final IEEE manuscript yet. First obtain:

- TOFC VisDrone result,
- full scale-wise results,
- UAVDT conversion and at least two UAVDT baseline runs.

After that, decide whether the project is strong enough for IEEE Transactions or should target a slightly less competitive English journal.

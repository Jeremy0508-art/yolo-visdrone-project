# IEEE Phase 1 Next Actions

## Current Status

The project has switched from the CEA route to the IEEE Transactions route. Phase 1 is about narrowing the target journal, preparing a second dataset, and deciding whether a new method module is worth implementing.

## Completed in Phase 1 So Far

| Item | Status | Artifact |
| --- | --- | --- |
| IEEE master plan | Done | `paper/IEEE_TRANS_SUBMISSION_PLAN.md` |
| Target journal analysis | Done | `paper/ieee_target_journal_analysis.md` |
| Experiment gap matrix | Done | `paper/ieee_required_experiment_gap.md` |
| Related work seed matrix | Done | `paper/ieee_related_work_matrix.csv` |
| UAVDT data config | Done | `configs/dataset/uavdt.yaml` |
| UAVDT setup notes | Done | `paper/datasets/uavdt_setup.md` |
| UAVDT conversion script | Done, untested without raw data | `scripts/convert_uavdt_to_yolo.py` |
| Dataset checker generalized for YAML class names | Done | `scripts/check_dataset.py` |
| Method design notes | Done | `paper/ieee_method_design_notes.md` |
| TOFC candidate module | Structure implemented; not trained | `src/models/attention/tiny_object_feature_calibration.py`, `configs/models/yolo11n_p2_tofc.yaml` |
| TOFC structure audit | Done | `paper/ieee_phase1_artifact_audit.md` |
| IEEE scale-evaluation target list | Done | `paper/tables/ieee_scale_eval_targets.csv` |
| Scale evaluation target-CSV support | Done | `tools/evaluate_scale_groups.py` |

## Immediate Technical Tasks

1. Obtain the raw UAVDT dataset and place it under `data/raw/UAVDT/`.
2. Run `scripts/convert_uavdt_to_yolo.py` and inspect conversion statistics.
3. Run `scripts/check_dataset.py --data-yaml configs/dataset/uavdt.yaml` with preview images.
4. Fix any raw-layout assumptions in the converter after seeing the actual downloaded structure.
5. Run the first TOFC full training only after GPU/server availability is confirmed.
6. Run the full scale-wise evaluation on completed VisDrone models when compute time is available.

## Immediate Research Tasks

1. Expand `paper/ieee_related_work_matrix.csv` with 20-30 recent papers.
2. Separate papers into:
   - directly reproducible comparisons,
   - literature-only comparisons,
   - method-background citations.
3. Check whether T-ITS recent papers emphasize traffic UAV datasets such as UAVDT or AU-AIR.
4. Check whether TGRS recent papers require remote-sensing-specific datasets beyond VisDrone/UAVDT.

## Do Not Do Yet

- Do not launch a long training queue before UAVDT conversion is verified.
- Do not start writing final IEEE claims before scale-wise metrics exist.
- Do not claim CoordAttention as a primary improvement unless new evidence supports it.
- Do not claim official VisDrone test-dev results unless the platform returns real metrics.

## Next Recommended Step

Prepare the UAVDT raw dataset and run conversion/integrity checks. In parallel, queue a VisDrone TOFC training experiment for the next available GPU window, but do not use TOFC in the manuscript until real training metrics exist.

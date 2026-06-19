# IEEE Phase 1 Artifact Audit

## Summary

This audit records the first set of local artifacts created for the IEEE Transactions route. It does not certify manuscript readiness and does not contain new training results.

| Check | Status | Evidence |
| --- | --- | --- |
| IEEE master plan exists | READY | `paper/IEEE_TRANS_SUBMISSION_PLAN.md` |
| Target journal analysis exists | READY | `paper/ieee_target_journal_analysis.md` |
| Experiment gap matrix exists | READY | `paper/ieee_required_experiment_gap.md` |
| Related-work seed matrix exists | READY | `paper/ieee_related_work_matrix.csv` |
| UAVDT dataset YAML exists | READY | `configs/dataset/uavdt.yaml` |
| UAVDT setup notes exist | READY | `paper/datasets/uavdt_setup.md` |
| UAVDT converter exists | READY | `scripts/convert_uavdt_to_yolo.py` |
| Dataset checker supports YAML names | READY | `scripts/check_dataset.py --data-yaml ...` |
| TOFC module exists | READY | `src/models/attention/tiny_object_feature_calibration.py` |
| TOFC model config builds | READY | `configs/models/yolo11n_p2_tofc.yaml` instantiated as a DetectionModel |
| TOFC training config exists | READY | `configs/train/yolo11n_p2_tofc_960.yaml` |
| TOFC training result exists | MISSING | No training has been launched yet |
| UAVDT converted dataset exists | MISSING | Raw UAVDT has not been placed under `data/raw/UAVDT/` yet |

## Structural Model Check

The following local construction check was run without training:

```text
configs/models/yolo11n_p2.yaml,30,2893672
configs/models/yolo11n_p2_tofc.yaml,31,2895762
configs/models/yolo11n_p2_coordatt.yaml,32,2903704
```

Interpretation:

- TOFC adds about 2,090 parameters over YOLO11n-P2.
- TOFC remains lighter than the existing CoordAttention variant.
- These are structural facts only, not detection-performance results.

## Remaining Phase 1 Gates

1. Download/place UAVDT raw files.
2. Run and visually validate UAVDT conversion.
3. Run a VisDrone TOFC training experiment only when GPU/server availability is confirmed.
4. Build scale-wise AP/Recall tooling before writing small-object claims.

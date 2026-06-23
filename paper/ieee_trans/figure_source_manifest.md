# IEEE Figure Source Manifest

Status: planning draft. This manifest records figure candidates for the IEEE Transactions route and their evidence boundaries.

## Ready or Usable With Current Evidence

| ID | Figure | Status | Source | Intended Use | Boundary |
| --- | --- | --- | --- | --- | --- |
| F-scale-1 | `paper/figures/scale_analysis/ieee_scale_recall_visdrone.png` | Ready | User-provided fixed final PNG; `paper/tables/ieee_scale_results_visdrone.csv`; `tools/evaluate_scale_groups.py` | Scale-wise recall comparison | Recall/precision only, not AP-small |
| F-scale-ap-1 | `paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png` | Ready | `paper/tables/ieee_scale_ap_results_visdrone.csv`; `tools/evaluate_scale_ap.py` | Local scale-bin AP50 comparison | Diagnostic only, not official AP-small |
| F-scale-2 | `paper/figures/scale_analysis/object_scale_distribution.png` | Ready | `paper/tables/object_scale_distribution.csv`; `tools/analyze_object_scales.py` | Dataset scale distribution | VisDrone only unless UAVDT stats are added |
| F-train-1 | `paper/figures/training_curves/p2_coordatt_960_results.png` | Ready | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png` | Training and validation curves | Existing P2-CA-960 run only |
| F-pr-1 | `paper/figures/training_curves/p2_coordatt_960_pr_curve.png` | Ready | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png` | PR curve | Existing P2-CA-960 run only |
| F-conf-1 | `paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png` | Ready | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png` | Class-level qualitative diagnostic | Optional; may be too dense for main paper |
| F-qual-1 | `paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg` | Ready | `runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg` | Representative detection visualization | Must not imply official test-dev result |
| F-fail-1 | `paper/figures/failure_cases/p2_case_contact_sheet.jpg` | Usable with caution | Existing curated failure-case visual asset | Failure-case discussion | Qualitative only; not a metric |
| F-trade-1 | `paper/figures/tradeoff/accuracy_speed_tradeoff.png` | Usable with caution | `paper/tables/accuracy_speed_tradeoff.csv`; `tools/plot_accuracy_speed_tradeoff.py` | Accuracy-speed trade-off | Refresh if final TOFC/UAVDT model is added |
| F-scalegate-design | `paper/figures/method/scalegate_schematic.png` | Ready as negative/mixed ablation | User-provided fixed v2 PNG; `src/models/attention/scale_aware_p2_gate.py`; `paper/ieee_trans/scalegate_method_section_draft.md`; `paper/ieee_scalegate_method_decision_audit.md` | Method explanation and mixed/negative ScaleGate evidence discussion | Structural figure only; do not promote ScaleGate as final method |

## Pending or Locked Figures

| ID | Figure | Status | Required Evidence |
| --- | --- | --- | --- |
| F-method-final | Bounded CSGate method overview | Ready for advisor draft | Completed CSGate VisDrone/UAVDT runs and `paper/ieee_csgate_method_decision_audit.md` |
| F-uavdt-qual | UAVDT qualitative detection results | Locked | Converted UAVDT dataset and completed model weights |
| F-uavdt-scale | UAVDT scale or density analysis | Locked | Converted UAVDT labels and evaluation outputs |
| F-tofc-ablation | TOFC ablation visualization | Locked | Completed TOFC training and validation evidence |
| F-official-testdev | Official VisDrone test-dev visualization or table | Locked | Official returned metrics or platform output |

## Figures Not Recommended for IEEE Manuscript

| File/Folder | Reason |
| --- | --- |
| `paper/figures/pdf_review/` | PDF review contact sheets are layout-review artifacts, not manuscript figures |
| CEA Word screenshots | They are format/debug artifacts and should not enter IEEE figures |
| Smoke-test plots under `runs/scale_group_smoke/` | Smoke tests are not paper evidence |

## Caption Rules

- Captions must name the dataset and split when relevant.
- Scale-wise captions must say recall/precision, not AP-small.
- Qualitative figures should not use words such as "best", "superior", or "state-of-the-art" unless supported by tables.
- Any figure generated from a pending run must remain out of final `main.tex`.
- Update this manifest after any new final-facing figure is selected or regenerated.

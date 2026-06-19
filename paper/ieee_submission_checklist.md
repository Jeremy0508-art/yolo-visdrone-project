# IEEE Transactions Submission Checklist

## Scope and Ethics

| Item | Status | Evidence / Action |
| --- | --- | --- |
| Target IEEE journal selected | Pending | Compare T-ITS and TGRS after advisor input |
| Duplicate-submission risk checked | Pending | CEA route is paused; do not submit both versions simultaneously |
| Original contribution defined | Pending | TOFC or another stronger method must be validated |
| All claims evidence-backed | Pending | Future `paper/ieee_claim_audit.md` |

## Experiments

| Item | Status | Evidence / Action |
| --- | --- | --- |
| VisDrone baseline and ablations | Ready | Existing `runs/` and `paper/tables/` artifacts |
| UAVDT dataset converted | Missing | `data/raw/UAVDT/` not available yet |
| UAVDT baseline experiments | Missing | Required for cross-dataset validation |
| New method experiment | Missing | TOFC structure exists but no training result |
| Scale-wise results | Partial | Tooling ready; full IEEE table pending |
| Multi-seed stability | Missing | Needed for strong Transactions claims |
| Speed/complexity | Ready for existing models | Must repeat for new models |

## Manuscript

| Item | Status | Evidence / Action |
| --- | --- | --- |
| IEEEtran template | Pending | Use IEEE Template Selector after target journal selection |
| English abstract | Pending | Write after final results |
| Related work | Partial | Seed matrix exists |
| Method section | Pending | Depends on selected final method |
| Results section | Pending | Depends on missing experiments |
| Discussion and limitations | Pending | Must include YOLO11s capacity comparison and failure cases |

## Submission Package

| Item | Status | Evidence / Action |
| --- | --- | --- |
| Main PDF | Pending | Build after IEEEtran manuscript exists |
| Source package | Pending | Include `.tex`, `.bib`, figures, generated tables |
| Cover letter | Pending | Write after target journal and contribution are fixed |
| Author metadata | Pending | Advisor/user confirmation required |
| Data/code availability statement | Pending | Decide GitHub release and dataset instructions |
| Suggested reviewers | Pending | Only if target journal requires |

## Current Gate

The project is in IEEE Phase 1. It is not ready for IEEE Transactions submission yet. The next gate is UAVDT dataset conversion plus the first real TOFC or alternative-method experiment.

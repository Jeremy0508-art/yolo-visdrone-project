# IEEE Dataset Strategy

This document decides which datasets should support the IEEE Transactions route. It separates required evidence from optional expansion so the project does not become too wide to finish.

## Recommendation

| Priority | Dataset | Decision | Reason |
| ---: | --- | --- | --- |
| P0 | VisDrone2019-DET | Keep as the primary dataset | It is already converted, trained, validated, and aligned with UAV aerial small-object detection. |
| P0 | UAVDT | Use as the required second dataset | It is UAV-based, traffic/vehicle-oriented, and fits a T-ITS framing better than a generic aerial dataset. |
| P1 | AU-AIR | Optional third dataset if UAVDT conversion or results are insufficient | It is traffic-related and UAV-based, but has a different annotation format and may require additional conversion work. |
| P1/P2 | AI-TOD-v2 | Optional tiny-object stress test | It is highly relevant to tiny-object detection, but setup and domain alignment are riskier than UAVDT. |
| P2 | TinyPerson | Literature/background only unless the paper pivots to tiny-person detection | Its category scope is much narrower than the current multi-class UAV detection task. |
| P2 | HIT-UAV | Not recommended for the first IEEE submission attempt | It is infrared/thermal, so domain shift would require a separate narrative and experiments. |

## Why UAVDT Is the Next Dataset

UAVDT should be the immediate cross-dataset target because it provides UAV traffic scenes, vehicle categories, multiple viewpoints, weather/illumination conditions, altitude attributes, occlusion attributes, and small dense targets. These properties align with the current project's strongest defensible narrative: lightweight UAV traffic perception under scale variation and crowding.

For IEEE-level evidence, UAVDT should not be used merely as a citation. It should be converted, integrity-checked, trained, validated, and audited with the same result traceability rules as VisDrone.

Required UAVDT outputs:

| Output | File/Command |
| --- | --- |
| Dataset setup record | `paper/datasets/uavdt_setup.md` |
| Dataset config | `configs/dataset/uavdt.yaml` |
| Conversion script | `scripts/convert_uavdt_to_yolo.py` |
| Integrity check | `python scripts/check_dataset.py --data-yaml configs/dataset/uavdt.yaml` |
| Baseline result | `runs/detect/baseline_yolo11n_960_uavdt` |
| P2 result | `runs/detect/yolo11n_p2_960_uavdt` |
| If TOFC works on VisDrone: TOFC result | `runs/detect/yolo11n_p2_tofc_960_uavdt` |

## Dataset-Specific Risks

| Dataset | Main Risk | Mitigation |
| --- | --- | --- |
| VisDrone2019-DET | Single-dataset evidence is not enough for IEEE Transactions | Add UAVDT, scale-wise metrics, and cautious claims. |
| UAVDT | Raw file layout and split conventions may differ across mirrors | Treat the current converter as provisional until raw files are inspected; record conversion statistics. |
| AU-AIR | JSON annotations and sensor metadata add conversion cost | Use only if T-ITS framing needs another traffic-oriented UAV dataset and time permits. |
| AI-TOD-v2 | Tiny-object strength is high, but the dataset construction/evaluation path is more complex | Use as optional stress test after VisDrone+UAVDT are complete. |
| TinyPerson | Single-category focus does not match VisDrone classes | Use for related work on tiny-object scale mismatch, not core experiments. |
| HIT-UAV | Infrared imagery differs from RGB VisDrone/UAVDT | Mention as adjacent UAV detection work only unless the paper pivots to multispectral/thermal. |

## Claim Mapping

| Desired Claim | Minimum Dataset Evidence |
| --- | --- |
| "The method improves VisDrone validation performance" | Completed VisDrone run, metric table, and log evidence for the exact method. |
| "The method improves small-object detection" | VisDrone scale-wise AP/Recall or equivalent size-bin analysis. |
| "The method generalizes to another UAV dataset" | UAVDT baseline and method results with identical or clearly documented protocol. |
| "The method is suitable for traffic UAV perception" | VisDrone traffic categories plus UAVDT or AU-AIR traffic-oriented validation. |
| "The method is robust for tiny aerial objects" | Scale-wise metrics plus optional AI-TOD-v2 or a clearly justified tiny-object benchmark. |

## Source Notes

Primary and near-primary sources checked on 2026-06-19:

- VisDrone official dataset repository: `https://github.com/VisDrone/VisDrone-Dataset`
- UAVDT official project page: `https://sites.google.com/view/grli-uavdt`
- AI-TOD official repository: `https://github.com/jwwangchn/AI-TOD`
- AI-TOD-v2 project page: `https://chasel-tsui.github.io/AI-TOD-v2/`
- AU-AIR data index: `https://fmi-data-index.github.io/au_air.html`
- AU-AIR API repository: `https://github.com/sunw71/auairdataset`
- HIT-UAV paper page: `https://arxiv.org/abs/2204.03245`

These notes are for planning. They do not replace formal BibTeX entries for the IEEE manuscript.

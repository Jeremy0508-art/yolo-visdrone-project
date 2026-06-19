# IEEE Reference Gap Report

Status: planning report, not a final bibliography audit.

This report compares the current related-work matrix with the seed BibTeX file and identifies which references are already usable as core background and which recent UAV/YOLO small-object papers still need verified BibTeX metadata before the final IEEE manuscript.

## Current Source Files

| Item | Source |
| --- | --- |
| Related-work matrix | `paper/ieee_related_work_matrix.csv` |
| Seed BibTeX | `paper/ieee_trans/references_seed.bib` |
| Reference audit | `paper/ieee_reference_audit.md` |

## Current Coverage Summary

| Category | Status | Notes |
| --- | --- | --- |
| Dataset and benchmark foundations | Mostly covered | VisDrone, UAVDT, AI-TOD, AU-AIR, TinyPerson, and HIT-UAV are represented in the seed bibliography. |
| Feature pyramid and fusion background | Covered | FPN, PANet, and EfficientDet are represented. |
| Attention background | Covered | Coordinate Attention is represented. |
| Drone-specific high-resolution YOLO prior | Covered at seed level | TPH-YOLOv5 is represented and should be used carefully as a close prior. |
| Recent 2024-2025 UAV/YOLO small-object papers | Pending metadata verification | Several rows exist in the related-work matrix, but their BibTeX entries are not yet verified. |
| Target-journal official pages | Not final bibliography items by default | These are planning sources and should usually remain in planning documents, not the manuscript references. |

## Seed Bibliography Items Already Available

| Topic | BibTeX Key | Role |
| --- | --- | --- |
| VisDrone benchmark | `du2019visdrone_det` | Primary dataset citation |
| VisDrone dataset repository | `visdrone_dataset_repo` | Dataset provenance / optional repository note |
| UAVDT benchmark | `du2018uavdt` | Planned second dataset citation |
| UAVDT project page | `uavdt_project_page` | Dataset access / optional repository note |
| TPH-YOLOv5 | `zhu2021tph_yolov5` | Drone small-object high-resolution head prior |
| CoordAttention | `hou2021coordinate_attention` | Attention-module background |
| FPN | `lin2017fpn` | Multi-scale feature-pyramid background |
| PANet | `liu2018panet` | Path aggregation / feature-fusion background |
| EfficientDet | `tan2020efficientdet` | Efficient feature-fusion and scaling background |
| AI-TOD | `wang2021aitod` | Tiny aerial-object benchmark background |
| AI-TOD-v2 / NWD | `xu2022aitodv2_nwd` | Tiny-object assignment/evaluation background |
| AU-AIR | `bozcan2020auair` | Traffic UAV dataset background |
| TinyPerson / Scale Match | `yu2020tinyperson` | Tiny-person scale mismatch background |
| HIT-UAV | `suo2023hituav` | Adjacent UAV detection dataset background |

## Pending Recent-Method References

The following related-work matrix rows should be converted to verified BibTeX entries only after checking publisher metadata, DOI, page/article number, and official title spelling.

| Paper / Resource | Year | Current Source URL | Planned Use | Needed Action |
| --- | ---: | --- | --- | --- |
| SOD-YOLO | 2024 | `https://www.mdpi.com/2072-4292/16/16/3057` | Recent UAV small-object YOLO prior | Verify title, authors, DOI, article number, and add BibTeX if used. |
| SMA-YOLO | 2025 | `https://www.mdpi.com/2072-4292/17/14/2421` | Recent multi-scale UAV small-object method | Verify publisher metadata and decide whether it is central enough to cite. |
| MASF-YOLO | 2025 | `https://arxiv.org/abs/2504.18136` | Very close YOLO11-based prior / novelty risk | Treat as preprint unless a peer-reviewed version exists; cite only with clear status. |
| SRTSOD-YOLO | 2025 | `https://www.mdpi.com/2072-4292/17/20/3414` | Recent real-time UAV small-object method | Verify publication metadata before final bibliography. |
| SOD-YOLOv8 | 2024 | `https://pmc.ncbi.nlm.nih.gov/articles/PMC11478522/` | Aerial/traffic small-object YOLOv8 prior | Verify original journal citation and DOI, not only PMC page. |

## Citation Strategy for the IEEE Manuscript

Use the references in three clearly separated roles:

1. **Dataset and problem motivation**: VisDrone, UAVDT, AI-TOD, AU-AIR, TinyPerson, HIT-UAV.
2. **Architectural background**: FPN, PANet, EfficientDet, TPH-YOLOv5, CoordAttention.
3. **Recent UAV/YOLO small-object context**: SOD-YOLO, SMA-YOLO, MASF-YOLO, SRTSOD-YOLO, SOD-YOLOv8 after metadata verification.

Do not use recent-method papers as direct numerical comparisons unless the dataset, split, metric definition, input size, and reproduction status are clearly aligned.

## Next Actions

1. Verify the five pending recent-method references from publisher or official paper pages.
2. Add BibTeX entries only after metadata is confirmed.
3. Update `paper/ieee_trans/citation_plan.md` with citation roles after new entries are added.
4. Re-run `python tools/check_ieee_references.py` and `python tools/run_ieee_audits.py`.

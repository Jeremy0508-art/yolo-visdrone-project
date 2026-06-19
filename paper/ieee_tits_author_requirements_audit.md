# IEEE T-ITS Author Requirements Audit

Status: official-source checklist, checked on 2026-06-19.

Primary target: IEEE Transactions on Intelligent Transportation Systems (T-ITS).

This document records submission-facing requirements that affect manuscript assembly. It does not replace the official pages; re-check the sources before final submission.

## Official Sources Checked

| Source | URL | Use |
| --- | --- | --- |
| IEEE ITSS T-ITS page | `https://ieee-itss.org/pub/t-its/` | Scope, submission site, article types, page guidance, abstract and keyword rules |
| IEEE Article Templates | `https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/tools-for-ieee-authors/ieee-article-templates/` | Official template entry point |
| IEEE Template Selector | `https://template-selector.ieee.org/` | Template selection entry point |

## Scope Requirements

T-ITS requires a clear transportation-systems contribution. Computer vision and deep learning are acceptable methodologies only when the transportation application is explicit.

Implications for this project:

| Requirement | Project Action |
| --- | --- |
| Transportation focus must be visible | Frame the paper as UAV-assisted traffic perception, not generic object detection. |
| Road users and transportation operations matter | Emphasize vehicles, pedestrians, bicycles, and traffic-scene monitoring in VisDrone/UAVDT. |
| Method benefit to transportation systems must be addressed | Explain how lightweight UAV detection supports traffic monitoring, emergency response, and deployable aerial sensing. |
| Generic YOLO engineering is not enough | Method and experiments must be tied to dense traffic small-object sensing and deployment trade-offs. |

## Submission and Format Requirements

| Item | Official Requirement | Current Project Status |
| --- | --- | --- |
| Submission portal | Electronic submission through IEEE Author Portal for T-ITS: `https://ieee.atyponrex.com/journal/t-its` | Pending final manuscript. |
| Format | IEEE style, double-column, single-spaced | Future `paper/ieee_trans/main.tex`; not created yet. |
| Template | Use IEEE article templates / template selector | Pending final `main.tex`; use IEEEtran journal template. |
| Article types | Regular, Short, Practitioner, Survey | Regular Paper is the likely target. |
| Suggested length | Regular 10 pages; Short 6; Practitioner 6; Survey 18 | Keep target draft near 10 IEEE pages before overlength. |
| Extra pages | Papers may exceed suggested length by no more than 6 additional pages; overlength charge after acceptance | Avoid relying on extra pages for core evidence. |
| Author list | Author list can be modified until acceptance; no changes after acceptance | Confirm authors before submission. |

## Abstract and Index-Term Requirements

| Item | Requirement | Project Action |
| --- | --- | --- |
| Abstract length | 150-250 words | Final abstract must be rewritten after final evidence gates pass. |
| Abstract format | One paragraph; no references, footnotes, displayed equations, or tabular material | Keep numerical results concise and source-backed. |
| Abstract quality | Concise, comprehensive, grammatical | Avoid overclaiming and avoid unexplained abbreviations. |
| Keywords/index terms | Maximum six keywords | Use `paper/ieee_trans/title_abstract_index_terms_workbench.md`. |
| Methodology keywords | Minimum one and maximum two from official methodology list | Likely candidates: Computer vision; Artificial Intelligence; Data-based approaches. |
| Application keywords | Minimum one and maximum two from official application list | Likely candidates: Road transportation; Traffic networks; Pedestrian flows and crowds. |
| Optional free keywords | Maximum two optional free keywords | Candidate free terms: UAV object detection; small object detection. |

## Final-File Requirements After Acceptance

This affects figure/table preparation even before submission.

| Item | Requirement | Project Action |
| --- | --- | --- |
| Paper files | PDF and identical LaTeX or Word source | Keep generated tables and figures reproducible. |
| Figures/tables | High-definition original files if not embedded; accepted examples include PS, EPS, PDF, PNG, TIFF, DOC, PPT, XLS | Prefer vector/PDF where possible for plots; keep PNG only when raster visualization is necessary. |
| Bios/photos | Required for regular papers, not required for Short/Practitioner Papers | Prepare only after article type is fixed. |
| Copyright | IEEE copyright transfer occurs through submission workflow | Confirm with authors before final submission. |

## Project-Specific Gate Before T-ITS Submission

Do not assemble a final-looking T-ITS manuscript until these are resolved:

| Gate | Current Status | Evidence Needed |
| --- | --- | --- |
| Transportation framing | Ready as plan | Use `paper/ieee_tits_scope_fit_checklist.md` and this audit when drafting. |
| Regular-paper page plan | Pending | Estimate page budget after final tables/figures are selected. |
| Final method | Pending | TOFC result or explicit fallback route decision. |
| Cross-dataset validation | Pending | UAVDT conversion and completed runs, or a scope downgrade approved by advisor. |
| Abstract and keywords | Pending | Final evidence-backed abstract and official-category keyword selection. |
| Final references | Pending | Verified `paper/ieee_trans/references.bib`. |

## Recommended Manuscript Positioning

The safe T-ITS positioning is:

> This work studies lightweight UAV-based traffic-object detection for dense small road users, with an emphasis on high-resolution prediction, scale-aware diagnostics, and deployable accuracy-efficiency trade-offs.

Avoid:

- framing the work as generic YOLO model tuning;
- claiming state-of-the-art performance without official or directly reproduced evidence;
- implying TOFC or UAVDT conclusions before the corresponding runs are complete;
- placing transportation motivation only in the introduction while the method and experiments remain generic.

# IEEE Submission Metadata Workbench

Status: planning workbench. User/advisor confirmation required before submission.

This file records the non-experimental information that will be needed when preparing an IEEE Transactions submission package. It intentionally leaves personal, institutional, funding, and reviewer information blank until confirmed by the user and advisor.

## Target and Article Type

| Field | Current Value | Confirmation Needed |
| --- | --- | --- |
| Target journal | IEEE Transactions on Intelligent Transportation Systems is the leading working target | Advisor confirmation required |
| Backup journal | IEEE Transactions on Geoscience and Remote Sensing or another IEEE venue | Advisor confirmation required |
| Article type | Regular Paper, tentatively | Advisor confirmation required |
| Submission system | IEEE Author Portal for T-ITS: `https://ieee.atyponrex.com/journal/t-its` | Re-check before final submission |
| Official requirement audit | `paper/ieee_tits_author_requirements_audit.md` | Re-check official pages before final submission |
| Suggested length | Regular Paper: 10 IEEE-style pages; extra pages have limits/charges | Estimate after final figures/tables are selected |
| Open access choice | Undecided | User/advisor/budget confirmation required |

## Author Metadata

Fill only after advisor confirmation.

| Field | Value |
| --- | --- |
| Author 1 name |  |
| Author 1 affiliation |  |
| Author 1 ORCID |  |
| Author 1 email |  |
| Author 2 name |  |
| Author 2 affiliation |  |
| Author 2 ORCID |  |
| Author 2 email |  |
| Additional authors |  |
| Corresponding author |  |
| Author order confirmed by all authors | No |

## Funding and Acknowledgment

| Field | Value / Action |
| --- | --- |
| Funding agency | User/advisor confirmation required |
| Grant number | User/advisor confirmation required |
| Institutional support | User/advisor confirmation required |
| Acknowledgment text | Draft only after funding and contribution details are confirmed |

## Data, Code, and Reproducibility Statement

Current project status:

- Public repository: `https://github.com/Jeremy0508-art/yolo-visdrone-project`
- Primary dataset: VisDrone2019-DET, distributed by its original dataset providers.
- Second dataset: UAVDT, converted and audited for the current baseline/static-P2 boundary set; ScaleGate UAVDT remains queued until the running server sequence reaches it.
- Training/evaluation commands: `paper/commands.md`
- Evidence tables: `paper/tables/`
- Dataset license audit: `paper/ieee_dataset_license_audit.md`
- Dataset compliance audit: `paper/ieee_dataset_compliance_audit.md`

Possible final wording, to revise after advisor approval:

> The implementation code, configuration files, reproducibility commands, and result-summary scripts are maintained in a public repository. Dataset download and use follow the licenses and terms of the original dataset providers. Trained weights and additional artifacts will be released according to the authors' institutional and dataset-license constraints.

Safe repository boundary:

> Raw datasets, converted datasets, and trained weights are not redistributed in this repository. Dataset users should obtain VisDrone and UAVDT data from the original providers and follow the corresponding terms.

Do not promise release of weights or private server logs until the advisor approves.

## Ethics and Originality Checks

| Check | Current Status | Action |
| --- | --- | --- |
| Simultaneous submission | CEA route paused | Do not submit CEA and IEEE versions at the same time |
| Prior dissemination | Repository is public; CEA draft materials exist locally | Disclose any public preprint/report if created later |
| Overlap risk | Not yet checked on final IEEE text | Run overlap/plagiarism self-check after final manuscript is assembled |
| AI/tool assistance disclosure | User/advisor decision required | Follow target journal and institution policy |
| Dataset license compliance | Audit documents ready; final confirmation pending | Use `paper/ieee_dataset_license_audit.md` and `paper/ieee_dataset_compliance_audit.md`; re-check VisDrone/UAVDT terms before submission |

## Suggested Reviewers / Opposed Reviewers

Only fill with advisor approval and after checking conflict-of-interest rules.

| Role | Name | Institution | Email | Reason / Expertise | Conflict Checked |
| --- | --- | --- | --- | --- | --- |
| Suggested reviewer 1 |  |  |  |  | No |
| Suggested reviewer 2 |  |  |  |  | No |
| Suggested reviewer 3 |  |  |  |  | No |
| Opposed reviewer, if any |  |  |  |  | No |

## Files Expected in Final Submission Package

| File / Item | Source | Status |
| --- | --- | --- |
| Main PDF | Future IEEEtran build | Pending |
| `main.tex` | Future `paper/ieee_trans/main.tex` | Pending |
| `references.bib` | Verified entries from `references_seed.bib` | Pending |
| 150-250 word abstract and max-six index terms | `paper/ieee_trans/title_abstract_index_terms_workbench.md` | Pending final target-journal and metadata review |
| Figures | `paper/ieee_trans/figure_source_manifest.md` | Partially ready |
| Generated LaTeX tables | `paper/ieee_trans/tables/` | Ready for current evidence; refresh after final results |
| Cover letter | `paper/ieee_trans/cover_letter_workbench.md` -> final draft | Pending |
| Response-prep risk register | `paper/ieee_reviewer_risk_register.md` | Ready |
| Response-prep plan | `paper/ieee_trans_response_plan.md` | Ready |
| Code/data statement | This workbench | Pending advisor confirmation |
| Dataset compliance audit | `paper/ieee_dataset_compliance_audit.md` | Ready as repository-boundary check; final human confirmation pending |

## Manual Confirmation Checklist

Before final submission, the user/advisor must confirm:

1. Exact IEEE journal.
2. Article type.
3. Author list, order, affiliations, emails, and ORCID IDs.
4. Corresponding author.
5. Funding and acknowledgments.
6. Code/data/weights release policy.
7. Open access or traditional publication choice.
8. Suggested/opposed reviewers, if requested by the submission system.
9. Whether any public preprint, report, or repository material must be disclosed.

# IEEE Dataset License and Citation Audit

Status: planning and compliance audit, checked on 2026-06-19.

This document records dataset-use constraints for the IEEE Transactions route. It is not legal advice. Re-check the official dataset pages and obtain advisor/institutional confirmation before final submission or public artifact release.

## Official Sources Checked

| Dataset | Source | URL | Relevant Finding |
| --- | --- | --- | --- |
| VisDrone | Official dataset repository | `https://github.com/VisDrone/VisDrone-Dataset` | Provides dataset description, download links, and citation entry for VisDrone; test-dev annotations are listed as available for paper publication. |
| VisDrone | Official privacy/copyright page | `https://aiskyeye.com/data-protection/` | States academic-use framing and Creative Commons Attribution-NonCommercial-ShareAlike 3.0 terms on the official VisDrone page. |
| UAVDT | Official project page | `https://sites.google.com/view/grli-uavdt` | States the dataset is for research purpose only and asks users to cite the UAVDT paper. |

## Current Repository Safety

| Item | Current State | Action |
| --- | --- | --- |
| Raw datasets | `data/raw/` is gitignored | Do not commit raw VisDrone/UAVDT data. |
| Converted datasets | `data/processed/` is gitignored | Do not commit converted labels/images. |
| Weights | `*.pt` and `weights/*` are gitignored | Release trained weights only after advisor/license confirmation. |
| Archives | `*.zip`, `*.tar`, `*.tar.gz`, `*.7z` are gitignored | Avoid uploading dataset archives to GitHub. |
| Public repository | Code and paper materials are public | Keep dataset download instructions as links, not bundled files. |

## Dataset-Specific Compliance Notes

### VisDrone2019-DET

Current manuscript use:

- Primary completed dataset for validation and analysis.
- Used through locally converted YOLO-format images/labels.
- Raw and converted data should remain outside Git.

Required manuscript actions:

- Cite the VisDrone detection/challenge paper and official dataset repository.
- State that VisDrone is distributed by its original providers.
- Do not redistribute raw images, annotations, or challenge archives in the repository.
- Do not claim official test-dev results unless official metrics are returned by the platform.

Open caution:

- The official privacy/copyright page currently names VisDrone2021 while giving the VisDrone license terms. Because this project uses VisDrone2019-DET, the final submission should conservatively follow the official academic/noncommercial/attribution/share-alike restrictions unless a version-specific VisDrone2019 license page says otherwise.

### UAVDT

Current manuscript use:

- Planned second dataset for T-ITS cross-dataset validation.
- Raw data is not yet placed locally.
- No UAVDT result can support manuscript claims yet.

Required manuscript actions:

- Cite the UAVDT ECCV paper and official project page.
- Follow the official project page's research-purpose-only statement.
- Do not redistribute the UAVDT dataset or converted copies.
- Record the exact download source, raw layout, conversion statistics, and split mapping after acquisition.

Open caution:

- If UAVDT is obtained from a mirror, the mirror's license metadata must not override the official project page without manual review.

## Citation Coverage

Current seed BibTeX coverage in `paper/ieee_trans/references_seed.bib`:

| Required Citation | Current Key | Status |
| --- | --- | --- |
| VisDrone detection/challenge paper | `du2019visdrone_det` | Ready for planning |
| VisDrone official dataset repository | `visdrone_dataset_repo` | Ready for planning |
| UAVDT ECCV paper | `du2018uavdt` | Ready for planning |
| UAVDT official project page | `uavdt_project_page` | Ready for planning |

Before final `references.bib`, verify publisher metadata and formatting for all dataset citations.

## Allowed Repository Wording

Safe wording for README or manuscript data-availability notes:

> The project provides code, configuration files, result-summary scripts, and reproducibility commands. VisDrone and UAVDT data should be downloaded from their original providers and used according to the corresponding dataset terms. Raw datasets, converted datasets, and trained weights are not redistributed in this repository.

Do not write:

- "The dataset is included in this repository."
- "All data and weights are freely reusable for any purpose."
- "UAVDT results are available" before conversion and training evidence exist.

## Final Submission Checklist

Before submission:

1. Re-open the official VisDrone and UAVDT pages.
2. Confirm the final dataset list with the advisor.
3. Confirm whether trained weights can be released.
4. Ensure the paper cites dataset papers and official project pages.
5. Ensure no raw/converted dataset files are included in the submission package unless explicitly allowed and required.
6. Ensure the data/code availability statement does not promise artifacts that cannot be released.

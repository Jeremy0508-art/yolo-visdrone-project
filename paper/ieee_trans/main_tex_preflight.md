# IEEE `main.tex` Preflight Checklist

Status: preflight checklist. Do not create final-facing `main.tex` until the gates below pass.

This checklist defines the required conditions, source files, and validation steps before creating an IEEEtran manuscript source under `paper/ieee_trans/main.tex`.

## Creation Gate

Create `main.tex` only when these items are satisfied:

| Gate | Current Status | Required Evidence |
| --- | --- | --- |
| Exact IEEE Transactions target selected | Pending | Advisor confirms T-ITS, TGRS, or another exact journal |
| Final method route selected | Pending | `paper/ieee_method_selection_protocol.md` updated after TOFC or fallback decision |
| TOFC decision complete | Pending | Complete run or explicit decision not to use TOFC |
| Cross-dataset plan resolved | Pending | UAVDT results complete, or manuscript scope downgraded to VisDrone-only analysis |
| T-ITS front matter workbench ready | Ready | `paper/ieee_trans/title_abstract_index_terms_workbench.md` |
| Submission metadata workbench ready | Ready | `paper/ieee_trans/submission_metadata_workbench.md`; user/advisor fields remain manual |
| Main result tables ready | Ready for current evidence | `paper/ieee_trans/tables/*.tex` generated and audited |
| Scale diagnostics ready | Ready for current evidence | recall/precision and local scale-bin AP reports exist |
| Claim audit ready | Pending final-facing files | `tools/check_ieee_claims.py` passes after `main.tex` exists |
| Reference metadata verified | Pending | Final `references.bib` checked against publisher metadata |

## Intended File Layout

When the gate passes, create or finalize:

| File/Folder | Purpose |
| --- | --- |
| `paper/ieee_trans/main.tex` | IEEEtran manuscript source |
| `paper/ieee_trans/references.bib` | Verified BibTeX entries for final manuscript |
| `paper/ieee_trans/tables/*.tex` | Generated evidence-backed table drafts |
| `paper/ieee_trans/figures/` | Final English figures copied or generated for IEEE layout |
| `paper/ieee_trans/build/` | Optional build output directory, ignored if needed |
| `paper/ieee_trans/cover_letter_draft.md` | Cover letter after target and claims are fixed |
| `paper/ieee_trans/submission_metadata_workbench.md` | Manual submission metadata source; not compiled into the paper |

Do not use CEA Word screenshots or PDF review contact sheets as IEEE figures.

## Section Source Map

| IEEE Section | Source to Start From | Must Update Before Final |
| --- | --- | --- |
| Title | `manuscript_blueprint.md`, `title_abstract_index_terms_workbench.md` | Final method and target journal |
| Abstract | `abstract_contribution_workbench.md`, `title_abstract_index_terms_workbench.md` | Exact final metrics and limitations |
| Index Terms | `title_abstract_index_terms_workbench.md` | Target journal and contribution category |
| Introduction | `section_draft_pack.md` | Final contributions and target-specific framing |
| Related Work | `related_work_outline.md`, `references_seed.bib` | Verified citations and recent literature |
| Method | `section_draft_pack.md`, method YAMLs | Final method decision, TOFC only if validated |
| Experiments | `section_draft_pack.md`, generated tables | UAVDT/TOFC updates if available |
| Discussion | `section_draft_pack.md`, `ieee_reviewer_risk_register.md` | Risks, limitations, YOLO11s boundary |
| Conclusion | Write last | No unsupported generalization or best-performance claims |
| Cover Letter | `cover_letter_workbench.md` | Target, title, authors, and evidence confirmed |
| Submission Metadata | `submission_metadata_workbench.md` | Author/funding/code-data fields confirmed manually |

## Mandatory Checks After `main.tex` Exists

Run these before sharing with the advisor:

```powershell
python tools\run_ieee_audits.py
python tools\check_ieee_claims.py
python tools\check_ieee_tables.py
python tools\check_ieee_figures.py
```

If LaTeX tooling is installed, compile with the selected IEEE template workflow and inspect:

- table width and column overflow,
- figure readability,
- reference formatting,
- title/abstract/conclusion claim strength,
- exact metric consistency with source CSV files.

## Claim Safety Checklist

Before compiling a shareable PDF, verify:

| Claim Type | Requirement |
| --- | --- |
| Small-object improvement | Must cite scale-wise recall/precision or local scale-bin AP with exact metric name |
| Official AP-small | Must not appear unless official-compatible evaluator is added |
| TOFC improvement | Must not appear unless TOFC run is complete and audited |
| Cross-dataset generalization | Must not appear unless UAVDT results are complete |
| Larger-model comparison | Must acknowledge YOLO11s-960 as stronger in absolute accuracy |
| Real-time/lightweight | Must cite speed, params, FLOPs, and hardware/protocol |

## Source Package Notes

The eventual submission package should include:

- `main.tex`
- `references.bib`
- final figures in accepted formats,
- generated table `.tex` files or inlined tables,
- any IEEE class/template files required by the selected journal,
- no local run weights or dataset files unless explicitly requested.

## Current Decision

Do not create `main.tex` yet. The project has strong planning and VisDrone evidence artifacts, but the final IEEE method, cross-dataset validation, and target journal still need to be settled.

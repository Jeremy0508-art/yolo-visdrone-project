# IEEE `main.tex` Preflight Checklist

Status: preflight checklist. Do not create final-facing `main.tex` until the gates below pass.

This checklist defines the required conditions, source files, and validation steps before creating an IEEEtran manuscript source under `paper/ieee_trans/main.tex`.

## Creation Gate

Create `main.tex` only when these items are satisfied:

| Gate | Current Status | Required Evidence |
| --- | --- | --- |
| Exact IEEE Transactions target selected | Pending | Advisor confirms T-ITS, TGRS, or another exact journal |
| Target author requirements checked | Ready for T-ITS | `paper/ieee_tits_author_requirements_audit.md`; re-check before final submission |
| Page budget plan reviewed | Ready as planning | `paper/ieee_trans/page_budget_plan.md`; revise after final table/figure selection |
| Front matter audit ready | Ready as planning | `paper/ieee_front_matter_audit.md`; final abstract length remains pending until evidence is complete |
| Dataset compliance audit ready | Ready as planning | `paper/ieee_dataset_compliance_audit.md`; final human license confirmation remains pending |
| Final method route selected | Ready as bounded CSGate route | `paper/ieee_csgate_method_decision_audit.md`; CSGate can be used as a method candidate with explicit limitations |
| Major-revision core argument locked | Ready as design layer | `paper/reframed_core_argument.md`, `paper/MAJOR_REVISION_ROADMAP.md` |
| Evidence matrix aligned with claims | Needs post-CSGate wording review | `paper/tables/reframed_evidence_matrix.csv`; update to include bounded CSGate evidence |
| TOFC decision complete | Ready for current draft | TOFC is retained as a VisDrone calibration candidate/ablation, not as the final cross-dataset method |
| ScaleGate decision complete | Ready; rejected as main method | `paper/ieee_scalegate_method_decision_audit.md` reports `DO_NOT_USE_SCALEGATE_AS_MAIN_METHOD` |
| CSGate decision complete | Ready; bounded method candidate | `paper/ieee_csgate_result_gate_audit.md` is open and `paper/ieee_csgate_method_decision_audit.md` accepts routes B and C |
| ScaleGate post-result runbook ready | Ready as current-state gate | `paper/ieee_scalegate_post_result_runbook.md` identifies the next allowed command block |
| ScaleGate guarded intake script ready | Ready | `tools/intake_ieee_scalegate_results.ps1` used for completed ScaleGate integration |
| ScaleGate scale-target enabler ready | Ready | `tools/set_ieee_scalegate_scale_target.py` prevents manually enabling diagnostics before local complete sync |
| ScaleGate paper-use gate | Ready for mixed/negative evidence | `paper/ieee_scalegate_result_gate_audit.md` reports `OPEN_FOR_POST_RESULT_INTEGRATION` |
| ScaleGate method-decision audit | Ready; rejected as main method | ScaleGate cannot become the main proposed method under the current audit |
| Cross-dataset plan resolved | Ready as validity-boundary evidence | `paper/tables/ieee_uavdt_results_for_paper.csv`; UAVDT shows current P2 trend does not transfer |
| T-ITS front matter workbench ready | Ready | `paper/ieee_trans/title_abstract_index_terms_workbench.md` |
| Submission metadata workbench ready | Ready | `paper/ieee_trans/submission_metadata_workbench.md`; user/advisor fields remain manual |
| Main result tables ready | Ready for current evidence | `paper/ieee_trans/tables/*.tex` generated and audited |
| Scale diagnostics ready | Ready for current evidence | recall/precision and local scale-bin AP reports exist |
| Number trace audit ready | Ready for current draft pack | `paper/ieee_number_trace_audit.md` shows zero non-ready numeric claims |
| Main draft number audit ready | Ready for current advisor draft | `paper/ieee_main_draft_number_audit.md` shows zero missing decimal traces |
| Advisor-draft shareability ready | Ready with author placeholders pending | `paper/ieee_draft_shareability_audit.md`; no missing issues before advisor sharing |
| Non-result closure audit ready | Ready if zero missing | `paper/ieee_non_result_closure_audit.md`; confirms remaining blockers are result/manual gates |
| Goal readiness audit ready | Ready if zero missing | `paper/ieee_goal_readiness_audit.md`; confirms local rest readiness is not mistaken for submission readiness |
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
| `paper/ieee_trans/page_budget_plan.md` | Page budget and figure/table selection guardrail |
| `paper/ieee_trans/post_uavdt_rewrite_checklist.md` | Ordered manuscript rewrite gate after complete UAVDT evidence |
| `paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md` | Ordered post-result integration gate for ScaleGate |
| `paper/ieee_scalegate_result_gate_audit.md` | Generated lock that confirms whether ScaleGate can enter paper-facing result claims |
| `paper/ieee_scalegate_method_decision_audit.md` | Generated A/B/C acceptance-route decision before final method selection |
| `paper/ieee_trans/reproducibility_notes.md` | Build, table-generation, and audit commands for the IEEE draft |
| `paper/ieee_draft_shareability_audit.md` | Advisor-review draft shareability check |
| `paper/ieee_main_draft_number_audit.md` | Decimal-number trace check for advisor-review draft text |
| `paper/reframed_core_argument.md` | Shared core argument for paper-style rewriting |
| `paper/tables/reframed_evidence_matrix.csv` | Claim-support and claim-boundary matrix |
| `paper/ieee_trans/build/` | Optional build output directory, ignored if needed |
| `paper/ieee_trans/cover_letter_draft.md` | Cover letter after target and claims are fixed |
| `paper/ieee_trans/submission_metadata_workbench.md` | Manual submission metadata source; not compiled into the paper |
| `paper/ieee_dataset_compliance_audit.md` | Dataset/code-release boundary check for final package review |
| `paper/ieee_goal_readiness_audit.md` | High-level rest/submission readiness gate |

Do not use CEA Word screenshots or PDF review contact sheets as IEEE figures.

`paper/ieee_trans/main_draft.tex` is allowed as an advisor-review draft because it is explicitly marked as evidence-bounded and non-final. This does not open the gate for `paper/ieee_trans/main.tex`.

## Section Source Map

| IEEE Section | Source to Start From | Must Update Before Final |
| --- | --- | --- |
| Title | `manuscript_blueprint.md`, `title_abstract_index_terms_workbench.md` | Final method and target journal |
| Abstract | `abstract_contribution_workbench.md`, `title_abstract_index_terms_workbench.md` | Exact final metrics and limitations |
| Index Terms | `title_abstract_index_terms_workbench.md` | Target journal and contribution category |
| Introduction | `section_draft_pack.md` | Final contributions and target-specific framing |
| Core claim framing | `../reframed_core_argument.md`, `../MAJOR_REVISION_ROADMAP.md`, `../IEEE_TRANS_METHOD_REDESIGN_PLAN.md` | Update after ScaleGate and method-selection decision |
| Related Work | `related_work_outline.md`, `references_seed.bib` | Verified citations and recent literature |
| Method | `section_draft_pack.md`, `scalegate_method_section_draft.md`, `csgate_method_section_draft.md`, method YAMLs, `../ieee_scalegate_method_decision_audit.md`, `../ieee_csgate_method_decision_audit.md` | ScaleGate only as mixed/negative evidence; CSGate is the bounded method-candidate route |
| Experiments | `section_draft_pack.md`, generated tables, `post_uavdt_rewrite_checklist.md`, `../IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md`, `../ieee_scalegate_result_gate_audit.md`, `../ieee_csgate_result_gate_audit.md` | ScaleGate is integrated as mixed/negative evidence; CSGate rows are integrated as bounded method evidence |
| Discussion | `section_draft_pack.md`, `ieee_reviewer_risk_register.md` | Risks, limitations, YOLO11s boundary |
| Conclusion | Write last | No unsupported generalization or best-performance claims |
| Cover Letter | `cover_letter_workbench.md` | Target, title, authors, and evidence confirmed |
| Submission Metadata | `submission_metadata_workbench.md` | Author/funding/code-data fields confirmed manually |

## Mandatory Checks After `main.tex` Exists

Run these before sharing with the advisor:

```powershell
python tools\run_ieee_audits.py
python tools\check_ieee_claims.py
python tools\check_ieee_front_matter.py
python tools\build_ieee_number_trace_audit.py
python tools\check_ieee_main_draft_numbers.py
python tools\check_ieee_draft_shareability.py
python tools\check_ieee_non_result_closure.py
python tools\check_ieee_goal_readiness.py
python tools\check_ieee_dataset_compliance.py
python tools\check_ieee_tables.py
python tools\check_ieee_figures.py
```

If LaTeX tooling is installed, compile with the selected IEEE template workflow and inspect:

- table width and column overflow,
- figure readability,
- reference formatting,
- title/abstract/conclusion claim strength,
- exact metric consistency with source CSV files.
- zero non-ready numeric claims in `paper/ieee_number_trace_audit.md`.

## Claim Safety Checklist

Before compiling a shareable PDF, verify:

| Claim Type | Requirement |
| --- | --- |
| Small-object improvement | Must cite scale-wise recall/precision or local scale-bin AP with exact metric name |
| Official AP-small | Must not appear unless official-compatible evaluator is added |
| TOFC improvement | Must be framed as completed VisDrone ablation, not final cross-dataset method |
| ScaleGate improvement | Must not appear as a positive method claim; completed evidence is mixed/negative |
| CSGate improvement | May appear only as bounded partial-repair evidence from completed VisDrone/UAVDT, speed, and scale diagnostics |
| Cross-dataset generalization | Must not appear unless the final method has positive cross-dataset evidence |
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

Do not create `main.tex` yet. The project now has a bounded CSGate method route from completed VisDrone/UAVDT evidence, but the exact IEEE target, author/funding metadata, verified bibliography, page budget, and final submission package still need to be settled.

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = ROOT / "paper/ieee_submission_dashboard.md"


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def count_csv_rows(rel_path: str) -> int:
    path = ROOT / rel_path
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def parse_summary(text: str) -> dict[str, str]:
    summary: dict[str, str] = {}
    for key in [
        "Total checks",
        "Ready",
        "Pending",
        "Missing",
        "Connection failed",
        "Tracked runs",
        "Partial",
        "Total entries",
        "Complete",
        "Ready in draft",
        "Non-ready numeric claims",
        "Untracked decimal tokens",
        "Untracked decimal tokens in draft",
        "Total decimal tokens",
        "Ignored layout/design-free tokens",
        "Gate status",
        "Complete ScaleGate runs",
        "Required epochs per run",
        "Decision status",
        "Accepted routes",
        "Closure status",
        "Intake status",
        "Remote complete ScaleGate runs",
        "Total requirements",
        "Experiment blockers",
        "Manual/final blockers",
        "Local rest status",
        "Submission status",
    ]:
        match = re.search(rf"- {re.escape(key)}: ([^\n]+)", text)
        if match:
            summary[key] = match.group(1).strip()
    return summary


def extract_pending_rows(phase_audit: str) -> list[str]:
    rows: list[str] = []
    for line in phase_audit.splitlines():
        if "| " in line and "| PENDING |" in line:
            rows.append(line)
    return rows


def status_badge(value: str) -> str:
    if value in {"0", "0.0", "0 missing"}:
        return "OK"
    return value


def build_dashboard() -> str:
    phase_text = read_text("paper/ieee_phase1_artifact_audit.md")
    claim_text = read_text("paper/ieee_claim_audit.md")
    server_text = read_text("paper/ieee_server_progress_report.md")
    scale_text = read_text("paper/ieee_scale_output_audit.md")
    registry_text = read_text("paper/ieee_experiment_registry_audit.md")
    table_text = read_text("paper/ieee_table_audit.md")
    figure_text = read_text("paper/ieee_figure_audit.md")
    front_text = read_text("paper/ieee_front_matter_audit.md")
    number_text = read_text("paper/ieee_number_trace_audit.md")
    main_draft_number_text = read_text("paper/ieee_main_draft_number_audit.md")
    dataset_text = read_text("paper/ieee_dataset_compliance_audit.md")
    interpretation_text = read_text("paper/ieee_result_interpretation_matrix_audit.md")
    uavdt_text = read_text("paper/datasets/uavdt_conversion_readiness_audit.md")
    evidence_map_text = read_text("paper/ieee_evidence_map_audit.md")
    assembly_text = read_text("paper/ieee_manuscript_assembly_audit.md")
    shareability_text = read_text("paper/ieee_draft_shareability_audit.md")
    reference_meta_text = read_text("paper/ieee_reference_metadata_readiness_audit.md")
    scalegate_launch_text = read_text("paper/ieee_scalegate_server_launch_audit.md")
    scalegate_gate_text = read_text("paper/ieee_scalegate_result_gate_audit.md")
    scalegate_decision_text = read_text("paper/ieee_scalegate_method_decision_audit.md")
    csgate_gate_text = read_text("paper/ieee_csgate_result_gate_audit.md")
    csgate_decision_text = read_text("paper/ieee_csgate_method_decision_audit.md")
    scalegate_runbook_text = read_text("paper/ieee_scalegate_post_result_runbook.md")
    scalegate_runbook_audit_text = read_text("paper/ieee_scalegate_post_result_runbook_audit.md")
    non_result_text = read_text("paper/ieee_non_result_closure_audit.md")
    goal_text = read_text("paper/ieee_goal_readiness_audit.md")
    phase = parse_summary(phase_text)
    claim = parse_summary(claim_text)
    server = parse_summary(server_text)
    scale = parse_summary(scale_text)
    registry = parse_summary(registry_text)
    table = parse_summary(table_text)
    figure = parse_summary(figure_text)
    front = parse_summary(front_text)
    number = parse_summary(number_text)
    main_draft_number = parse_summary(main_draft_number_text)
    dataset = parse_summary(dataset_text)
    interpretation = parse_summary(interpretation_text)
    uavdt = parse_summary(uavdt_text)
    evidence_map = parse_summary(evidence_map_text)
    assembly = parse_summary(assembly_text)
    shareability = parse_summary(shareability_text)
    reference_meta = parse_summary(reference_meta_text)
    scalegate_gate = parse_summary(scalegate_gate_text)
    scalegate_decision = parse_summary(scalegate_decision_text)
    csgate_gate = parse_summary(csgate_gate_text)
    csgate_decision = parse_summary(csgate_decision_text)
    scalegate_runbook = parse_summary(scalegate_runbook_text)
    scalegate_runbook_audit = parse_summary(scalegate_runbook_audit_text)
    non_result = parse_summary(non_result_text)
    goal = parse_summary(goal_text)
    related_rows = count_csv_rows("paper/ieee_related_work_matrix.csv")
    section_rows = count_csv_rows("paper/ieee_trans/evidence_to_sections.csv")
    scalegate_launched = bool(scalegate_launch_text.strip())
    scalegate_decision_status = scalegate_decision.get("Decision status", "")
    scalegate_rejected = scalegate_decision_status == "DO_NOT_USE_SCALEGATE_AS_MAIN_METHOD"
    scalegate_status = (
        "COMPLETED / REJECTED AS MAIN METHOD"
        if scalegate_rejected
        else ("TRAINING / QUEUED" if scalegate_launched else "PENDING TRAINING")
    )
    scalegate_action = (
        "Use as mixed/negative adaptive-gate evidence; do not promote it in the title, abstract, contributions, or conclusion."
        if scalegate_rejected
        else (
            "Monitor the launched server queue; sync and audit only after both ScaleGate runs reach 100 epochs."
            if scalegate_launched
            else "Launch only after server authentication and code sync are confirmed."
        )
    )
    csgate_launch_text = read_text("paper/ieee_csgate_server_launch_audit.md")
    csgate_launched = bool(csgate_launch_text.strip())
    csgate_status = "RUNNING / RESULT-LOCKED" if csgate_launched else "PENDING REAL RUNS"
    csgate_action = (
        "Monitor the guarded server queue; sync and cite only complete 100-epoch runs."
        if csgate_launched
        else "Sync the CSGate code/configs to the server, run a smoke test, then launch VisDrone and UAVDT only through the guarded queue."
    )

    pending_rows = extract_pending_rows(phase_text)

    lines = [
        "# IEEE Submission Dashboard",
        "",
        "This dashboard is generated by `tools/build_ieee_submission_dashboard.py`. It summarizes the current IEEE Transactions route without treating planned or pending work as completed evidence.",
        "",
        "## Current Route",
        "",
        "- Active route: IEEE Transactions preparation.",
        "- Primary target framing: UAV-assisted traffic small-object detection, with T-ITS as the leading target direction.",
        "- Parallel route: the CEA Chinese-journal package remains active and should not be treated as an abandoned or historical project.",
        "- Method direction: the route has moved beyond packaging the static P2 result; completed `ScaleAwareP2Gate` evidence did not pass the predeclared main-method gate, so the active method route is the second-cycle `CrossScaleP2P3ConsistencyGate` candidate.",
        "- Manuscript status: `paper/ieee_trans/main_draft.tex` is a compiled evidence-bounded draft after the major-revision reframing and UAVDT integration; final IEEE `main.tex` is intentionally not created yet.",
        f"- Local rest status: {goal.get('Local rest status', 'not audited yet')}; submission status: {goal.get('Submission status', 'not audited yet')}.",
        "",
        "## Major-Revision And UAVDT Status",
        "",
        "The English route has been reframed from a progress-report manuscript into a paper-style study of high-resolution prediction for lightweight UAV small-object detection. The current shared argument is:",
        "",
        "```text",
        "High-resolution input and shallow P2 prediction can improve lightweight YOLO small-object diagnostics, but the benefit must be discussed together with computational cost, object scale, model capacity, and cross-dataset validity boundaries.",
        "```",
        "",
        "The four required UAVDT runs have been synced and exported into manuscript-safe tables. The current UAVDT result narrows the claim: YOLO11n-P2-960 is weaker than YOLO11n-960, YOLOv8n-960, and YOLO11s-960 on UAVDT, so the IEEE draft should be framed as mechanism analysis and validity-boundary evidence rather than a transferable P2 superiority claim.",
        "",
        "The first adaptive P2 route, `ScaleAwareP2Gate`, is complete on VisDrone and UAVDT, but the method-decision audit rejects it as the main method. It may be used only as mixed/negative ablation evidence. The second-cycle route, `CrossScaleP2P3ConsistencyGate`, now has complete VisDrone/UAVDT runs, refreshed diagnostics, speed/complexity rows, and a method-decision audit that permits only a bounded partial-repair claim.",
        "",
        "## Readiness Snapshot",
        "",
        "| Area | Ready | Pending | Missing | Notes |",
        "| --- | ---: | ---: | ---: | --- |",
        (
            f"| Phase 1 artifacts | {phase.get('Ready', 'n/a')} | {phase.get('Pending', 'n/a')} | "
            f"{status_badge(phase.get('Missing', 'n/a'))} | `paper/ieee_phase1_artifact_audit.md` |"
        ),
        (
            f"| Claim audit | {claim.get('Ready', 'n/a')} | {claim.get('Pending', 'n/a')} | "
            f"{status_badge(claim.get('Missing', 'n/a'))} | `paper/ieee_claim_audit.md` |"
        ),
        (
            f"| Server progress | {server.get('Ready', 'n/a')} | {server.get('Partial', 'n/a')} partial / "
            f"{server.get('Connection failed', '0')} connection failed | "
            f"{server.get('Missing', 'n/a')} | `paper/ieee_server_progress_report.md` |"
        ),
        (
            f"| Scale-wise outputs | {scale.get('Ready', 'n/a')} | {scale.get('Pending', 'n/a')} | "
            f"{status_badge(scale.get('Missing', 'n/a'))} | `paper/ieee_scale_output_audit.md` |"
        ),
        (
            f"| Experiment registry | {registry.get('Complete', 'n/a')} complete | {registry.get('Pending', 'n/a')} | "
            f"{registry.get('Partial', '0')} partial | `paper/ieee_experiment_registry_audit.md` |"
        ),
        (
            f"| IEEE table drafts | {table.get('Ready', 'n/a')} | {table.get('Pending', 'n/a')} | "
            f"{status_badge(table.get('Missing', 'n/a'))} | `paper/ieee_table_audit.md` |"
        ),
        (
            f"| IEEE figure manifest | {figure.get('Ready', 'n/a')} | {figure.get('Pending', 'n/a')} | "
            f"{status_badge(figure.get('Missing', 'n/a'))} | `paper/ieee_figure_audit.md` |"
        ),
        (
            f"| Front matter audit | {front.get('Ready', 'n/a')} | {front.get('Pending', 'n/a')} | "
            f"{status_badge(front.get('Missing', 'n/a'))} | `paper/ieee_front_matter_audit.md` |"
        ),
        (
            f"| Number trace audit | {number.get('Ready in draft', 'n/a')} | "
            f"{number.get('Non-ready numeric claims', 'n/a')} | "
            f"{number.get('Untracked decimal tokens in draft', number.get('Untracked decimal tokens', 'n/a'))} untracked | `paper/ieee_number_trace_audit.md` |"
        ),
        (
            f"| Main draft number audit | {main_draft_number.get('Ready', 'n/a')} | "
            f"{main_draft_number.get('Ignored layout/design-free tokens', 'n/a')} ignored | "
            f"{status_badge(main_draft_number.get('Missing', 'n/a'))} | `paper/ieee_main_draft_number_audit.md` |"
        ),
        (
            f"| Dataset compliance audit | {dataset.get('Ready', 'n/a')} | {dataset.get('Pending', 'n/a')} | "
            f"{status_badge(dataset.get('Missing', 'n/a'))} | `paper/ieee_dataset_compliance_audit.md` |"
        ),
        (
            f"| UAVDT conversion readiness | {uavdt.get('Ready', 'n/a')} | {uavdt.get('Pending', 'n/a')} | "
            f"{status_badge(uavdt.get('Missing', 'n/a'))} | `paper/datasets/uavdt_conversion_readiness_audit.md` |"
        ),
        (
            f"| Result interpretation matrix | {interpretation.get('Ready', 'n/a')} | n/a | "
            f"{status_badge(interpretation.get('Missing', 'n/a'))} | `paper/ieee_result_interpretation_matrix_audit.md` |"
        ),
        (
            f"| Evidence-to-section map | {evidence_map.get('Ready', 'n/a')} | n/a | "
            f"{status_badge(evidence_map.get('Missing', 'n/a'))} | `paper/ieee_evidence_map_audit.md` |"
        ),
        (
            f"| Manuscript assembly audit | {assembly.get('Ready', 'n/a')} | {assembly.get('Pending', 'n/a')} | "
            f"{status_badge(assembly.get('Missing', 'n/a'))} | `paper/ieee_manuscript_assembly_audit.md` |"
        ),
        (
            f"| Advisor-draft shareability | {shareability.get('Ready', 'n/a')} | {shareability.get('Pending', 'n/a')} | "
            f"{status_badge(shareability.get('Missing', 'n/a'))} | `paper/ieee_draft_shareability_audit.md` |"
        ),
        (
            f"| Reference metadata readiness | {reference_meta.get('Ready', 'n/a')} | {reference_meta.get('Pending', 'n/a')} | "
            f"{status_badge(reference_meta.get('Missing', 'n/a'))} | `paper/ieee_reference_metadata_readiness_audit.md` |"
        ),
        (
            f"| ScaleGate result gate | {scalegate_gate.get('Ready', 'n/a')} | {scalegate_gate.get('Pending', 'n/a')} | "
            f"{status_badge(scalegate_gate.get('Missing', 'n/a'))} | "
            f"{scalegate_gate.get('Gate status', 'n/a')}; complete runs {scalegate_gate.get('Complete ScaleGate runs', 'n/a')} |"
        ),
        (
            f"| ScaleGate method decision | {scalegate_decision.get('Ready', 'n/a')} | {scalegate_decision.get('Pending', 'n/a')} | "
            f"{status_badge(scalegate_decision.get('Missing', 'n/a'))} | "
            f"{scalegate_decision.get('Decision status', 'n/a')}; accepted routes {scalegate_decision.get('Accepted routes', 'n/a')} |"
        ),
        (
            f"| CSGate result gate | {csgate_gate.get('Ready', 'n/a')} | {csgate_gate.get('Pending', 'n/a')} | "
            f"{status_badge(csgate_gate.get('Missing', 'n/a'))} | "
            f"{csgate_gate.get('Gate status', 'n/a')}; complete runs {csgate_gate.get('Complete CSGate runs', 'n/a')} |"
        ),
        (
            f"| CSGate method decision | {csgate_decision.get('Ready', 'n/a')} | {csgate_decision.get('Pending', 'n/a')} | "
            f"{status_badge(csgate_decision.get('Missing', 'n/a'))} | "
            f"{csgate_decision.get('Decision status', 'n/a')}; accepted routes {csgate_decision.get('Accepted routes', 'n/a')} |"
        ),
        (
            f"| ScaleGate post-result runbook | {scalegate_runbook.get('Remote complete ScaleGate runs', 'n/a')} remote complete | n/a | "
            f"n/a | {scalegate_runbook.get('Intake status', 'n/a')}; `paper/ieee_scalegate_post_result_runbook.md` |"
        ),
        (
            f"| ScaleGate runbook audit | {scalegate_runbook_audit.get('Ready', 'n/a')} | n/a | "
            f"{status_badge(scalegate_runbook_audit.get('Missing', 'n/a'))} | `paper/ieee_scalegate_post_result_runbook_audit.md` |"
        ),
        (
            f"| Non-result task closure | {non_result.get('Ready', 'n/a')} | {non_result.get('Pending', 'n/a')} | "
            f"{status_badge(non_result.get('Missing', 'n/a'))} | "
            f"{non_result.get('Closure status', 'n/a')}; `paper/ieee_non_result_closure_audit.md` |"
        ),
        (
            f"| IEEE goal readiness | {goal.get('Ready', 'n/a')} | {goal.get('Pending', 'n/a')} | "
            f"{status_badge(goal.get('Missing', 'n/a'))} | "
            f"{goal.get('Local rest status', 'n/a')}; {goal.get('Submission status', 'n/a')}; `paper/ieee_goal_readiness_audit.md` |"
        ),
        f"| Related-work matrix | {related_rows} rows | n/a | n/a | `paper/ieee_related_work_matrix.csv` |",
        f"| Evidence-to-section CSV | {section_rows} rows | n/a | n/a | `paper/ieee_trans/evidence_to_sections.csv` |",
        "",
        "## Ready Assets",
        "",
        "- IEEE route master plan: `paper/IEEE_TRANS_SUBMISSION_PLAN.md`",
        "- Target journal analysis: `paper/ieee_target_journal_analysis.md`",
        "- T-ITS scope-fit checklist: `paper/ieee_tits_scope_fit_checklist.md`",
        "- T-ITS author requirements audit: `paper/ieee_tits_author_requirements_audit.md`",
        "- Experiment gap matrix: `paper/ieee_required_experiment_gap.md`",
        "- Experiment registry: `paper/tables/ieee_experiment_registry.csv`, `paper/ieee_experiment_registry_audit.md`",
        "- Dataset strategy: `paper/ieee_dataset_strategy.md`",
        "- UAVDT setup, operational checklist, and conversion readiness audit: `paper/datasets/uavdt_setup.md`, `paper/datasets/uavdt_operational_checklist.md`, `paper/datasets/uavdt_conversion_readiness_audit.md`",
        "- Method design, selection protocol, and second-cycle backlog: `paper/ieee_method_design_notes.md`, `paper/ieee_method_selection_protocol.md`, `paper/IEEE_SECOND_CYCLE_METHOD_BACKLOG.md`",
        "- Claim boundary rules: `paper/ieee_claim_boundary.md`",
        "- Reviewer risk register and response-prep plan: `paper/ieee_reviewer_risk_register.md`, `paper/ieee_trans_response_plan.md`",
        "- Manuscript blueprint, front-matter/submission workbenches, section draft pack, assembly checklist, page budget plan, and main.tex preflight: `paper/ieee_trans/manuscript_blueprint.md`, `paper/ieee_trans/abstract_contribution_workbench.md`, `paper/ieee_trans/title_abstract_index_terms_workbench.md`, `paper/ieee_trans/submission_metadata_workbench.md`, `paper/ieee_trans/cover_letter_workbench.md`, `paper/ieee_trans/section_draft_pack.md`, `paper/ieee_trans/manuscript_assembly_checklist.md`, `paper/ieee_trans/page_budget_plan.md`, `paper/ieee_trans/main_tex_preflight.md`",
        "- ScaleGate method-section draft: `paper/ieee_trans/scalegate_method_section_draft.md`",
        "- CSGate method-section draft: `paper/ieee_trans/csgate_method_section_draft.md`",
        "- Manuscript assembly audit: `paper/ieee_manuscript_assembly_audit.md`",
        "- Advisor-draft shareability audit: `paper/ieee_draft_shareability_audit.md`",
        "- Related-work outline and literature comparison protocol: `paper/ieee_trans/related_work_outline.md`, `paper/ieee_literature_comparison_protocol.md`, `paper/tables/ieee_literature_context.csv`",
        "- Novelty positioning workbench: `paper/ieee_trans/novelty_positioning_workbench.md`",
        "- Seed bibliography, citation plan, and reference-gap report: `paper/ieee_trans/references_seed.bib`, `paper/ieee_trans/citation_plan.md`, `paper/ieee_reference_gap_report.md`",
        "- Reference metadata readiness audit: `paper/ieee_reference_metadata_readiness_audit.md`",
        "- ScaleGate result gate audit: `paper/ieee_scalegate_result_gate_audit.md`",
        "- ScaleGate method decision audit: `paper/ieee_scalegate_method_decision_audit.md`",
        "- CSGate result gate audit: `paper/ieee_csgate_result_gate_audit.md`",
        "- CSGate method decision audit: `paper/ieee_csgate_method_decision_audit.md`",
        "- ScaleGate post-result dynamic runbook: `paper/ieee_scalegate_post_result_runbook.md`",
        "- ScaleGate post-result runbook audit: `paper/ieee_scalegate_post_result_runbook_audit.md`",
        "- Non-result task closure audit: `paper/ieee_non_result_closure_audit.md`",
        "- IEEE goal readiness audit: `paper/ieee_goal_readiness_audit.md`",
        "- Table/figure plan: `paper/ieee_trans/table_figure_plan.md`",
        "- Generated IEEE table drafts and audit: `paper/ieee_trans/tables/`, `paper/ieee_table_audit.md`",
        "- Figure source manifest and audit: `paper/ieee_trans/figure_source_manifest.md`, `paper/ieee_figure_audit.md`",
        "- Front-matter audit for T-ITS title, abstract, index terms, and metadata: `paper/ieee_front_matter_audit.md`",
        "- Number trace audit for draft paragraphs: `paper/ieee_number_trace_audit.md`",
        "- Main draft number audit: `paper/ieee_main_draft_number_audit.md`",
        "- Result interpretation matrix and audit: `paper/ieee_result_interpretation_matrix.md`, `paper/ieee_result_interpretation_matrix_audit.md`",
        "- Evidence-to-section map and audit: `paper/ieee_trans/evidence_to_sections.csv`, `paper/ieee_evidence_map_audit.md`",
        "- Major-revision roadmap and shared argument: `paper/MAJOR_REVISION_ROADMAP.md`, `paper/reframed_core_argument.md`",
        "- New method redesign plan: `paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md`",
        "- Dual-route narrative strategy and evidence matrix: `paper/dual_track_reframed_manuscript_strategy.md`, `paper/tables/reframed_evidence_matrix.csv`",
        "- Compiled evidence-bounded IEEE draft: `paper/ieee_trans/main_draft.tex`, `paper/ieee_trans/main_draft.pdf`",
        "- UAVDT manuscript-safe results: `paper/tables/ieee_uavdt_results_for_paper.csv`, `paper/ieee_trans/tables/uavdt_results.tex`",
        "- UAVDT integration audit: `paper/ieee_uavdt_integration_audit.md`",
        "- Dataset license and compliance audits: `paper/ieee_dataset_license_audit.md`, `paper/ieee_dataset_compliance_audit.md`",
        "- Server resume runbook: `paper/ieee_server_resume_runbook.md`",
        "- ScaleGate server launch audit: `paper/ieee_scalegate_server_launch_audit.md`",
        "- CSGate server launch audit: `paper/ieee_csgate_server_launch_audit.md`",
        "- ScaleGate post-result integration protocol: `paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md`",
        "- CSGate post-result integration protocol: `paper/IEEE_CSGATE_POST_RESULT_PROTOCOL.md`",
        "- Server integration protocol: `paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md`",
        "- Scale-wise evaluation protocol, local AP protocol, audits, and interpretations: `paper/ieee_scale_evaluation_protocol.md`, `paper/ieee_scale_ap_protocol.md`, `paper/ieee_scale_output_audit.md`, `paper/ieee_scale_result_interpretation.md`, `paper/ieee_scale_ap_interpretation.md`",
        "- Guarded server queue: `tools/run_ieee_server_queue.sh`",
        "- ScaleGate server queue: `tools/start_ieee_scalegate_queue.sh`",
        "- CSGate server queue and intake tools: `tools/start_ieee_csgate_queue.sh`, `tools/intake_ieee_csgate_results.ps1`, `tools/set_ieee_scale_target.py`",
        "- Guarded server sync/status tools: `tools/check_ieee_server_status.ps1`, `tools/sync_ieee_server_results.ps1`",
        "",
        "## Current Pending Gates",
        "",
    ]

    lines.extend(
        [
            "| Area | Item | Status | Evidence | Action |",
            "| --- | --- | --- | --- | --- |",
            "| Final source | `paper/ieee_trans/main.tex` | NOT CREATED | `paper/ieee_trans/main_tex_preflight.md` | Create only after advisor confirms target journal, author metadata, and final manuscript route. |",
            f"| Advisor-review draft | `paper/ieee_trans/main_draft.pdf` | {shareability.get('Missing', 'n/a')} missing / {shareability.get('Pending', 'n/a')} pending | `paper/ieee_draft_shareability_audit.md` | Share only as a non-final advisor-review draft; author placeholders remain pending. |",
            "| Target journal | Exact IEEE Transactions venue | PENDING ADVISOR CONFIRMATION | `paper/ieee_target_journal_analysis.md` | Confirm T-ITS, TGRS, or another exact journal before final packaging. |",
            "| Final claims | Cross-dataset robustness / superiority | BLOCKED BY EVIDENCE | `paper/tables/ieee_uavdt_results_for_paper.csv` | Keep validity-boundary wording; do not claim transferable P2 improvement. |",
            f"| New method evidence | YOLO11n-P2-ScaleGate on VisDrone and UAVDT | {scalegate_status} | `paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md` | {scalegate_action} |",
            f"| Second-cycle method evidence | YOLO11n-P2-CSGate on VisDrone and UAVDT | {csgate_status} | `configs/models/yolo11n_p2_csgate.yaml` | {csgate_action} |",
            f"| ScaleGate paper-use gate | ScaleGate rows, diagnostics, speed, and manuscript claims | {scalegate_gate.get('Gate status', 'PENDING AUDIT')} | `paper/ieee_scalegate_result_gate_audit.md` | Use ScaleGate only after this gate opens and the post-result protocol is executed. |",
            f"| ScaleGate method decision | Acceptance routes A/B/C | {scalegate_decision.get('Decision status', 'PENDING AUDIT')} | `paper/ieee_scalegate_method_decision_audit.md` | Do not promote ScaleGate to the title, abstract, or contribution list unless an acceptance route passes. |",
            f"| CSGate paper-use gate | CSGate rows, diagnostics, speed, and manuscript claims | {csgate_gate.get('Gate status', 'PENDING AUDIT')} | `paper/ieee_csgate_result_gate_audit.md` | Do not sync or cite partial CSGate metrics. |",
            f"| CSGate method decision | Acceptance routes A/B/C | {csgate_decision.get('Decision status', 'PENDING AUDIT')} | `paper/ieee_csgate_method_decision_audit.md` | Do not promote CSGate unless an acceptance route passes after complete results. |",
            "| Submission metadata | Authors, affiliations, funding, code/data statements | MANUAL | `paper/ieee_trans/submission_metadata_workbench.md` | Fill after advisor confirmation. |",
        ]
    )

    lines.extend(
        [
            "",
            "## Next Execution Order",
            "",
            "1. Keep `main_draft.tex` as the advisor-review draft and do not rename it to `main.tex` yet.",
            "2. Treat completed UAVDT results as the reason for redesigning the method, not as a result to hide.",
            "3. Treat completed ScaleGate as a failed main-method candidate and use it only to motivate second-cycle design.",
            "4. Monitor the guarded CSGate VisDrone/UAVDT queue without using partial metrics.",
            "5. After CSGate completes, sync only complete runs and regenerate speed, complexity, scale recall/precision, and local scale-bin AP.",
            "6. Re-check target-journal fit, author metadata, funding, and code/data statements before final packaging.",
            "7. Run `python tools/run_ieee_audits.py` after every table, figure, or manuscript update.",
            "8. Compile and visually inspect `paper/ieee_trans/main_draft.pdf` before sharing.",
            "9. Create final IEEE `main.tex` only after the gates in `paper/ieee_trans/main_tex_preflight.md` pass.",
            "",
            "## Claim Discipline",
            "",
            "- TOFC is a VisDrone calibration candidate/ablation, not a validated cross-dataset final method.",
            "- ScaleGate is completed but failed the predeclared main-method acceptance routes; it must not be promoted as the proposed method.",
            "- CSGate has code/config evidence only; it has no accuracy, robustness, or SOTA claim until complete real runs are synced and audited.",
            "- UAVDT is complete and shows a validity boundary: the current P2 trend does not transfer under the audited setting.",
            "- Existing VisDrone results can be discussed only with exact values from audited tables.",
            "- Larger YOLO11s accuracy must be acknowledged; the safe current narrative is lightweight trade-off, not universal superiority.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    DASHBOARD_PATH.write_text(build_dashboard(), encoding="utf-8")
    print(f"Wrote {DASHBOARD_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

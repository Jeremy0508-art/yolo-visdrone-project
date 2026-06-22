from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_non_result_closure_audit.md"


@dataclass
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


REQUIRED_FILES = [
    ("Planning", "IEEE master plan", "paper/IEEE_TRANS_SUBMISSION_PLAN.md"),
    ("Planning", "Major-revision roadmap", "paper/MAJOR_REVISION_ROADMAP.md"),
    ("Planning", "Reframed core argument", "paper/reframed_core_argument.md"),
    ("Planning", "Method redesign plan", "paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md"),
    ("Planning", "Method selection protocol", "paper/ieee_method_selection_protocol.md"),
    ("Planning", "ScaleGate post-result protocol", "paper/IEEE_SCALEGATE_POST_RESULT_PROTOCOL.md"),
    ("Planning", "CSGate post-result protocol", "paper/IEEE_CSGATE_POST_RESULT_PROTOCOL.md"),
    ("Planning", "Second-cycle method backlog", "paper/IEEE_SECOND_CYCLE_METHOD_BACKLOG.md"),
    ("Manuscript", "Advisor-review IEEE draft source", "paper/ieee_trans/main_draft.tex"),
    ("Manuscript", "Advisor-review IEEE draft PDF", "paper/ieee_trans/main_draft.pdf"),
    ("Manuscript", "Manuscript blueprint", "paper/ieee_trans/manuscript_blueprint.md"),
    ("Manuscript", "Assembly checklist", "paper/ieee_trans/manuscript_assembly_checklist.md"),
    ("Evidence", "Reframed evidence matrix", "paper/tables/reframed_evidence_matrix.csv"),
    ("Evidence", "Result interpretation matrix", "paper/ieee_result_interpretation_matrix.md"),
    ("Evidence", "Evidence-to-section map", "paper/ieee_trans/evidence_to_sections.csv"),
    ("Evidence", "UAVDT paper-safe results", "paper/tables/ieee_uavdt_results_for_paper.csv"),
    ("Evidence", "Main draft number audit", "paper/ieee_main_draft_number_audit.md"),
    ("Guardrail", "ScaleGate result gate audit", "paper/ieee_scalegate_result_gate_audit.md"),
    ("Guardrail", "ScaleGate method decision audit", "paper/ieee_scalegate_method_decision_audit.md"),
    ("Guardrail", "CSGate result gate audit", "paper/ieee_csgate_result_gate_audit.md"),
    ("Guardrail", "CSGate method decision audit", "paper/ieee_csgate_method_decision_audit.md"),
    ("Guardrail", "ScaleGate post-result dynamic runbook", "paper/ieee_scalegate_post_result_runbook.md"),
    ("Guardrail", "ScaleGate post-result runbook audit", "paper/ieee_scalegate_post_result_runbook_audit.md"),
    ("Guardrail", "CSGate server launch audit", "paper/ieee_csgate_server_launch_audit.md"),
    ("Guardrail", "Draft shareability audit", "paper/ieee_draft_shareability_audit.md"),
    ("Guardrail", "Dataset compliance audit", "paper/ieee_dataset_compliance_audit.md"),
    ("Guardrail", "Reference metadata readiness audit", "paper/ieee_reference_metadata_readiness_audit.md"),
    ("Guardrail", "IEEE goal readiness audit", "paper/ieee_goal_readiness_audit.md"),
    ("Guardrail", "Submission dashboard", "paper/ieee_submission_dashboard.md"),
    ("Execution", "Guarded CSGate intake script", "tools/intake_ieee_csgate_results.ps1"),
    ("Execution", "Generic scale target enabler", "tools/set_ieee_scale_target.py"),
    ("Advisor", "Advisor progress brief", "paper/ieee_advisor_progress_brief.md"),
]


AUDIT_ZERO_MISSING = [
    ("paper/ieee_phase1_artifact_audit.md", "Phase 1 artifact audit"),
    ("paper/ieee_manuscript_assembly_audit.md", "Manuscript assembly audit"),
    ("paper/ieee_draft_shareability_audit.md", "Draft shareability audit"),
    ("paper/ieee_main_draft_number_audit.md", "Main draft number audit"),
    ("paper/ieee_claim_audit.md", "Claim audit"),
    ("paper/ieee_dataset_compliance_audit.md", "Dataset compliance audit"),
    ("paper/ieee_reference_metadata_readiness_audit.md", "Reference metadata readiness audit"),
    ("paper/ieee_table_audit.md", "IEEE table audit"),
    ("paper/ieee_figure_audit.md", "IEEE figure audit"),
    ("paper/ieee_evidence_map_audit.md", "Evidence map audit"),
    ("paper/ieee_csgate_result_gate_audit.md", "CSGate result gate audit"),
    ("paper/ieee_csgate_method_decision_audit.md", "CSGate method decision audit"),
]


EXPECTED_PENDING_MARKERS = [
    ("ScaleGate result gate", "OPEN_FOR_POST_RESULT_INTEGRATION"),
    ("ScaleGate method decision", "DO_NOT_USE_SCALEGATE_AS_MAIN_METHOD"),
    ("CSGate second-cycle evidence", "YOLO11n-P2-CSGate"),
    ("CSGate result gate", "WAITING_FOR_COMPLETE_CSGATE_RESULTS"),
    ("CSGate method decision", "LOCKED_WAITING_FOR_COMPLETE_CSGATE_RESULTS"),
    ("Advisor authors", "First/Second/Third Author placeholders found"),
    ("Final target journal", "Exact IEEE Transactions target selected"),
    ("Final method route", "CSGate"),
    ("Final dataset release boundary", "final dataset-license confirmation"),
    ("Final abstract", "final requirement is 150-250"),
]


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def summary_value(text: str, key: str) -> str | None:
    match = re.search(rf"- {re.escape(key)}: ([^\n]+)", text)
    if not match:
        return None
    return match.group(1).strip()


def file_check(area: str, item: str, rel_path: str) -> Check:
    path = ROOT / rel_path
    return Check(
        area=area,
        item=item,
        status="READY" if path.exists() else "MISSING",
        evidence=rel_path,
        action="" if path.exists() else "Regenerate or restore this result-independent artifact.",
    )


def missing_check(rel_path: str, label: str) -> Check:
    text = read_text(rel_path)
    if not text:
        return Check("Audit health", label, "MISSING", rel_path, "Run python tools/run_ieee_audits.py.")
    missing = summary_value(text, "Missing")
    if missing in {"0", "0.0"}:
        return Check("Audit health", label, "READY", f"{rel_path}; Missing={missing}")
    return Check(
        "Audit health",
        label,
        "MISSING",
        f"{rel_path}; Missing={missing if missing is not None else 'not reported'}",
        "Resolve missing entries before considering non-result tasks closed.",
    )


def marker_check(label: str, marker: str) -> Check:
    haystack = "\n".join(
        [
            read_text("paper/ieee_submission_dashboard.md"),
            read_text("paper/ieee_manuscript_assembly_audit.md"),
            read_text("paper/ieee_draft_shareability_audit.md"),
            read_text("paper/ieee_front_matter_audit.md"),
            read_text("paper/ieee_dataset_compliance_audit.md"),
            read_text("paper/ieee_scalegate_result_gate_audit.md"),
            read_text("paper/ieee_scalegate_method_decision_audit.md"),
            read_text("paper/ieee_csgate_result_gate_audit.md"),
            read_text("paper/ieee_csgate_method_decision_audit.md"),
        ]
    )
    if marker in haystack:
        return Check("Allowed pending gate", label, "READY", marker)
    return Check(
        "Allowed pending gate",
        label,
        "MISSING",
        marker,
        "Restore this explicit pending boundary so unfinished work is not mistaken for completed evidence.",
    )


def build_checks() -> list[Check]:
    checks: list[Check] = []
    checks.extend(file_check(area, item, rel_path) for area, item, rel_path in REQUIRED_FILES)
    checks.extend(missing_check(rel_path, label) for rel_path, label in AUDIT_ZERO_MISSING)
    checks.extend(marker_check(label, marker) for label, marker in EXPECTED_PENDING_MARKERS)

    main_tex = ROOT / "paper/ieee_trans/main.tex"
    checks.append(
        Check(
            "Final assembly boundary",
            "Final IEEE main.tex remains intentionally absent",
            "READY" if not main_tex.exists() else "PENDING",
            "paper/ieee_trans/main.tex",
            "" if not main_tex.exists() else "Keep this file out of final use until result, target-journal, and metadata gates close.",
        )
    )

    draft = read_text("paper/ieee_trans/main_draft.tex")
    forbidden = [
        "ScaleGate improves",
        "state-of-the-art performance",
        "outperforms larger",
        "generalizes to UAVDT",
    ]
    hits: list[str] = []
    for line in draft.splitlines():
        for token in forbidden:
            if token not in line:
                continue
            lowered = line.lower()
            if (
                "may not claim" in lowered
                or "do not claim" in lowered
                or "must not" in lowered
                or "do not support" in lowered
                or "does not support" in lowered
            ):
                continue
            hits.append(token)
    checks.append(
        Check(
            "Claim boundary",
            "Advisor draft avoids forbidden positive performance claims",
            "READY" if not hits else "MISSING",
            "hits: " + (", ".join(hits) if hits else "none"),
            "" if not hits else "Revise main_draft.tex before sharing.",
        )
    )
    return checks


def render_report(checks: list[Check]) -> str:
    ready = sum(1 for check in checks if check.status == "READY")
    pending = sum(1 for check in checks if check.status == "PENDING")
    missing = sum(1 for check in checks if check.status == "MISSING")
    closure_status = (
        "CLOSED_EXCEPT_RESULT_AND_MANUAL_GATES"
        if missing == 0
        else "OPEN_MISSING_NON_RESULT_ITEMS"
    )

    lines = [
        "# IEEE Non-Result Task Closure Audit",
        "",
        "This report is generated by `tools/check_ieee_non_result_closure.py`. It verifies that result-independent IEEE-route materials are in place while keeping experiment-dependent and human-confirmation gates explicit.",
        "",
        "It does not launch training, does not sync partial server runs, and does not promote ScaleGate into a main-method claim.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(checks)}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        f"- Closure status: {closure_status}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.area} | {check.item} | {check.status} | `{check.evidence}` | {check.action} |"
        )

    lines.extend(
        [
            "",
            "## Remaining Locked Items",
            "",
            "| Gate | Why it remains locked | Next action |",
            "| --- | --- | --- |",
            "| CSGate VisDrone/UAVDT evidence | The second-cycle route has code/config evidence but no completed metrics yet. | Launch and sync only through the guarded queue after remote smoke test. |",
            "| Final method route | ScaleGate has been rejected as the main method, and CSGate still needs complete evidence. | Keep ScaleGate as mixed/negative evidence; evaluate CSGate only after complete results are synced. |",
            "| Final IEEE `main.tex` | The final manuscript should not be assembled before the method route, target journal, author metadata, references, and release boundary are fixed. | Keep using `main_draft.tex` for advisor review. |",
            "| Author and submission metadata | Author order, affiliations, funding, OA choice, and release policy require advisor/institution confirmation. | Fill `paper/ieee_trans/submission_metadata_workbench.md` after confirmation. |",
            "",
            "## Interpretation",
            "",
            "- `READY` means the local non-result artifact or guardrail is present.",
            "- `PENDING` means the item is intentionally blocked by final manuscript assembly policy, not forgotten.",
            "- `MISSING` means a local non-result item still needs repair before resting this phase.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    checks = build_checks()
    REPORT_PATH.write_text(render_report(checks), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

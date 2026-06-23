from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_goal_readiness_audit.md"
SERVER_HISTORY_PATH = ROOT / "paper/tables/ieee_server_status_history.csv"


@dataclass
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


READY_FILES = [
    ("Route", "IEEE master route plan", "paper/IEEE_TRANS_SUBMISSION_PLAN.md"),
    ("Route", "Major-revision roadmap", "paper/MAJOR_REVISION_ROADMAP.md"),
    ("Route", "Reframed core argument", "paper/reframed_core_argument.md"),
    ("Route", "Adaptive method redesign plan", "paper/IEEE_TRANS_METHOD_REDESIGN_PLAN.md"),
    ("Route", "Second-cycle method backlog", "paper/IEEE_SECOND_CYCLE_METHOD_BACKLOG.md"),
    ("Route", "CSGate post-result protocol", "paper/IEEE_CSGATE_POST_RESULT_PROTOCOL.md"),
    ("Method", "ScaleAwareP2Gate source", "src/models/attention/scale_aware_p2_gate.py"),
    ("Method", "ScaleAwareP2Gate model config", "configs/models/yolo11n_p2_scalegate.yaml"),
    ("Method", "ScaleGate VisDrone train config", "configs/train/yolo11n_p2_scalegate_960.yaml"),
    ("Method", "ScaleGate UAVDT train config", "configs/train/yolo11n_p2_scalegate_960_uavdt.yaml"),
    ("Method", "CrossScaleP2P3ConsistencyGate source", "src/models/attention/cross_scale_p2_p3_gate.py"),
    ("Method", "CSGate model config", "configs/models/yolo11n_p2_csgate.yaml"),
    ("Method", "CSGate VisDrone train config", "configs/train/yolo11n_p2_csgate_960.yaml"),
    ("Method", "CSGate UAVDT train config", "configs/train/yolo11n_p2_csgate_960_uavdt.yaml"),
    ("Evidence", "VisDrone paper table", "paper/tables/main_comparison_for_paper.csv"),
    ("Evidence", "UAVDT paper-safe table", "paper/tables/ieee_uavdt_results_for_paper.csv"),
    ("Evidence", "Reframed evidence matrix", "paper/tables/reframed_evidence_matrix.csv"),
    ("Evidence", "Evidence-to-section map", "paper/ieee_trans/evidence_to_sections.csv"),
    ("Evidence", "Result interpretation matrix", "paper/ieee_result_interpretation_matrix.md"),
    ("Manuscript", "Advisor-review IEEE source", "paper/ieee_trans/main_draft.tex"),
    ("Manuscript", "Advisor-review IEEE PDF", "paper/ieee_trans/main_draft.pdf"),
    ("Manuscript", "IEEE section draft pack", "paper/ieee_trans/section_draft_pack.md"),
    ("Manuscript", "ScaleGate method section draft", "paper/ieee_trans/scalegate_method_section_draft.md"),
    ("Manuscript", "CSGate method section draft", "paper/ieee_trans/csgate_method_section_draft.md"),
    ("Manuscript", "IEEE manuscript assembly checklist", "paper/ieee_trans/manuscript_assembly_checklist.md"),
    ("Guardrail", "ScaleGate result gate audit", "paper/ieee_scalegate_result_gate_audit.md"),
    ("Guardrail", "ScaleGate method decision audit", "paper/ieee_scalegate_method_decision_audit.md"),
    ("Guardrail", "CSGate result gate audit", "paper/ieee_csgate_result_gate_audit.md"),
    ("Guardrail", "CSGate method decision audit", "paper/ieee_csgate_method_decision_audit.md"),
    ("Guardrail", "ScaleGate post-result runbook", "paper/ieee_scalegate_post_result_runbook.md"),
    ("Guardrail", "ScaleGate runbook audit", "paper/ieee_scalegate_post_result_runbook_audit.md"),
    ("Guardrail", "CSGate server launch audit", "paper/ieee_csgate_server_launch_audit.md"),
    ("Guardrail", "Non-result closure audit", "paper/ieee_non_result_closure_audit.md"),
    ("Guardrail", "Submission dashboard", "paper/ieee_submission_dashboard.md"),
    ("Execution", "ScaleGate server queue", "tools/start_ieee_scalegate_queue.sh"),
    ("Execution", "CSGate server queue", "tools/start_ieee_csgate_queue.sh"),
    ("Execution", "Guarded ScaleGate intake script", "tools/intake_ieee_scalegate_results.ps1"),
    ("Execution", "Guarded CSGate intake script", "tools/intake_ieee_csgate_results.ps1"),
    ("Execution", "ScaleGate scale target enabler", "tools/set_ieee_scalegate_scale_target.py"),
    ("Execution", "Generic scale target enabler", "tools/set_ieee_scale_target.py"),
    ("Execution", "IEEE audit runner", "tools/run_ieee_audits.py"),
]


ZERO_MISSING_AUDITS = [
    ("paper/ieee_phase1_artifact_audit.md", "Phase 1 artifact audit"),
    ("paper/ieee_non_result_closure_audit.md", "Non-result closure audit"),
    ("paper/ieee_scalegate_result_gate_audit.md", "ScaleGate result gate audit"),
    ("paper/ieee_scalegate_method_decision_audit.md", "ScaleGate method decision audit"),
    ("paper/ieee_csgate_result_gate_audit.md", "CSGate result gate audit"),
    ("paper/ieee_csgate_method_decision_audit.md", "CSGate method decision audit"),
    ("paper/ieee_scalegate_post_result_runbook_audit.md", "ScaleGate runbook audit"),
    ("paper/ieee_manuscript_assembly_audit.md", "Manuscript assembly audit"),
    ("paper/ieee_draft_shareability_audit.md", "Advisor-draft shareability audit"),
    ("paper/ieee_main_draft_number_audit.md", "Main draft number audit"),
    ("paper/ieee_dataset_compliance_audit.md", "Dataset compliance audit"),
    ("paper/ieee_reference_metadata_readiness_audit.md", "Reference metadata readiness audit"),
]


SCALEGATE_RUNS = [
    ("ScaleGate experiment", "VisDrone ScaleGate complete result", "yolo11n_p2_scalegate_960_visdrone"),
    ("ScaleGate experiment", "UAVDT ScaleGate complete result", "yolo11n_p2_scalegate_960_uavdt"),
]


CSGATE_RUNS = [
    ("CSGate experiment", "VisDrone CSGate complete result", "yolo11n_p2_csgate_960_visdrone"),
    ("CSGate experiment", "UAVDT CSGate strict 100-epoch complete result", "yolo11n_p2_csgate_960_uavdt_full100"),
]


FINAL_GATES = [
    (
        "Final assembly",
        "Final IEEE source package",
        "paper/ieee_trans/main.tex",
        "Create only after target journal, author metadata, release policy, and final references are confirmed.",
    ),
    (
        "Final assembly",
        "Final IEEE bibliography",
        "paper/ieee_trans/references.bib",
        "Create only after publisher metadata and final citation set are verified.",
    ),
    (
        "Manual confirmation",
        "Exact IEEE Transactions target",
        "paper/ieee_trans/submission_metadata_workbench.md",
        "Advisor must confirm T-ITS, TGRS, or another exact journal before final packaging.",
    ),
    (
        "Manual confirmation",
        "Author, affiliation, funding, and code/data release metadata",
        "paper/ieee_trans/submission_metadata_workbench.md",
        "Requires advisor/institution confirmation before submission.",
    ),
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
    if path.exists():
        return Check(area, item, "READY", rel_path)
    return Check(area, item, "MISSING", rel_path, "Restore or regenerate this local non-result artifact.")


def audit_zero_missing(rel_path: str, label: str) -> Check:
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
        "Resolve missing entries before resting the non-result phase.",
    )


def latest_server_rows() -> dict[str, dict[str, str]]:
    if not SERVER_HISTORY_PATH.exists():
        return {}
    rows: dict[str, dict[str, str]] = {}
    with SERVER_HISTORY_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            run = row.get("run", "")
            if run:
                rows[run] = row
    return rows


def server_run_check(area: str, item: str, run: str, rows: dict[str, dict[str, str]]) -> Check:
    row = rows.get(run)
    if not row:
        return Check(
            area,
            item,
            "PENDING",
            f"{run}; no server-history row",
            "Refresh server status, then sync only after a complete 100-epoch run exists.",
        )
    status = row.get("status", "")
    epochs = row.get("epochs", "")
    required = row.get("completion_gate_epochs", "100")
    timestamp = row.get("timestamp", "")
    metrics = []
    if row.get("last_map50"):
        metrics.append(f"mAP50={row['last_map50']}")
    if row.get("last_map50_95"):
        metrics.append(f"mAP50-95={row['last_map50_95']}")
    evidence = f"{run}; server={status}; epochs={epochs}/{required}; timestamp={timestamp}"
    if metrics:
        evidence += "; progress " + ", ".join(metrics)
    if status == "READY" and epochs == required:
        return Check(area, item, "READY", evidence)
    return Check(
        area,
        item,
        "PENDING",
        evidence,
        "Wait for full completion; do not use partial metrics in the manuscript.",
    )


def gate_status_check(label: str, rel_path: str, key: str, expected: str) -> Check:
    text = read_text(rel_path)
    if not text:
        return Check("Gate state", label, "MISSING", rel_path, "Run python tools/run_ieee_audits.py.")
    value = summary_value(text, key)
    if value == expected:
        return Check("Gate state", label, "READY", f"{rel_path}; {key}={value}")
    return Check(
        "Gate state",
        label,
        "PENDING",
        f"{rel_path}; {key}={value if value is not None else 'not reported'}",
        "This gate should remain locked until the completed results are synced and audited.",
    )


def final_gate_check(area: str, item: str, rel_path: str, action: str) -> Check:
    path = ROOT / rel_path
    if area == "Manual confirmation":
        if path.exists():
            return Check(area, item, "PENDING", rel_path, action)
        return Check(area, item, "MISSING", rel_path, "Restore the metadata workbench before final submission planning.")
    if path.exists():
        return Check(area, item, "PENDING", rel_path, "Review this final-facing artifact against the preflight gate.")
    return Check(area, item, "PENDING", f"{rel_path}; intentionally absent", action)


def build_checks() -> list[Check]:
    checks: list[Check] = []
    checks.extend(file_check(area, item, rel_path) for area, item, rel_path in READY_FILES)
    checks.extend(audit_zero_missing(rel_path, label) for rel_path, label in ZERO_MISSING_AUDITS)

    checks.append(
        gate_status_check(
            "ScaleGate result gate is open after complete synced runs",
            "paper/ieee_scalegate_result_gate_audit.md",
            "Gate status",
            "OPEN_FOR_POST_RESULT_INTEGRATION",
        )
    )
    checks.append(
        gate_status_check(
            "ScaleGate method decision rejects main-method promotion",
            "paper/ieee_scalegate_method_decision_audit.md",
            "Decision status",
            "DO_NOT_USE_SCALEGATE_AS_MAIN_METHOD",
        )
    )
    checks.append(
        gate_status_check(
            "ScaleGate intake runbook is ready for manuscript decision",
            "paper/ieee_scalegate_post_result_runbook.md",
            "Intake status",
            "READY_FOR_MANUSCRIPT_DECISION",
        )
    )

    server_rows = latest_server_rows()
    checks.extend(server_run_check(area, item, run, server_rows) for area, item, run in SCALEGATE_RUNS)
    checks.extend(server_run_check(area, item, run, server_rows) for area, item, run in CSGATE_RUNS)
    checks.extend(final_gate_check(area, item, rel_path, action) for area, item, rel_path, action in FINAL_GATES)
    return checks


def render_server_snapshot(rows: dict[str, dict[str, str]]) -> list[str]:
    lines = [
        "## Latest Server Snapshot",
        "",
        "| Run | Status | Epochs | mAP50 | mAP50-95 | Timestamp |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    wanted = [
        "yolo11n_p2_tofc_960_visdrone",
        "baseline_yolo11n_960_uavdt",
        "yolo11n_p2_960_uavdt",
        "baseline_yolov8n_960_uavdt",
        "baseline_yolo11s_960_uavdt",
        "yolo11n_p2_scalegate_960_visdrone",
        "yolo11n_p2_scalegate_960_uavdt",
        "yolo11n_p2_csgate_960_visdrone",
        "yolo11n_p2_csgate_960_uavdt_full100",
    ]
    for run in wanted:
        row = rows.get(run, {})
        epochs = row.get("epochs") or "0"
        last_epoch = row.get("completion_gate_epochs") or "100"
        lines.append(
            "| "
            + " | ".join(
                [
                    run,
                    row.get("status", "MISSING"),
                    f"{epochs}/{last_epoch}",
                    row.get("last_map50", ""),
                    row.get("last_map50_95", ""),
                    row.get("timestamp", ""),
                ]
            )
            + " |"
        )
    return lines


def render_report(checks: list[Check]) -> str:
    ready = sum(1 for check in checks if check.status == "READY")
    pending = sum(1 for check in checks if check.status == "PENDING")
    missing = sum(1 for check in checks if check.status == "MISSING")
    experiment_blockers = sum(
        1 for check in checks if check.status == "PENDING" and check.area in {"ScaleGate experiment", "CSGate experiment"}
    )
    manual_or_final_blockers = sum(
        1 for check in checks if check.status == "PENDING" and check.area in {"Final assembly", "Manual confirmation"}
    )

    non_result_text = read_text("paper/ieee_non_result_closure_audit.md")
    non_result_status = summary_value(non_result_text, "Closure status")
    if missing == 0 and experiment_blockers == 0 and non_result_status == "CLOSED_EXCEPT_RESULT_AND_MANUAL_GATES":
        local_rest_status = "CLOSED_EXCEPT_MANUAL_FINAL_GATES"
    elif missing == 0 and non_result_status == "CLOSED_EXCEPT_RESULT_AND_MANUAL_GATES":
        local_rest_status = "OPEN_SECOND_CYCLE_EXPERIMENTS"
    else:
        local_rest_status = "OPEN_LOCAL_NON_RESULT_ITEMS"

    if missing:
        submission_status = "NOT_READY_LOCAL_MISSING_ITEMS"
    elif experiment_blockers:
        submission_status = "NOT_READY_WAITING_FOR_EXPERIMENT_AND_MANUAL_GATES"
    elif manual_or_final_blockers:
        submission_status = "NOT_READY_WAITING_FOR_MANUAL_FINAL_GATES"
    else:
        submission_status = "READY_FOR_FINAL_SUBMISSION_REVIEW"

    rows = latest_server_rows()
    lines = [
        "# IEEE Goal Readiness Audit",
        "",
        "This report is generated by `tools/check_ieee_goal_readiness.py`. It audits the current high-level objective after completed ScaleGate and CSGate evidence: keep the failed ScaleGate route bounded, keep CSGate as a partial-repair method candidate, and keep the actual submission gate locked until manual metadata and final package requirements are satisfied.",
        "",
        "The audit does not launch training, does not connect to the server, does not sync partial runs, and does not promote planned results into manuscript claims.",
        "",
        "## Summary",
        "",
        f"- Total requirements: {len(checks)}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        f"- Experiment blockers: {experiment_blockers}",
        f"- Manual/final blockers: {manual_or_final_blockers}",
        f"- Local rest status: {local_rest_status}",
        f"- Submission status: {submission_status}",
        "",
        "## Requirement Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        evidence = check.evidence.replace("\n", "<br>")
        lines.append(f"| {check.area} | {check.item} | {check.status} | `{evidence}` | {check.action} |")

    lines.extend(["", "## Remaining Blockers", ""])
    lines.extend(
        [
            "| Blocker | Why it remains open | Safe next action |",
            "| --- | --- | --- |",
            "| Exact IEEE Transactions venue | T-ITS is the leading route, but the advisor must confirm the final journal before final IEEE packaging. | Confirm T-ITS, TGRS, or another exact venue, then update `paper/ieee_trans/submission_metadata_workbench.md`. |",
            "| Reference metadata verification | `references_seed.bib` is ready, but final `references.bib` should only be created after publisher metadata is checked. | Verify DOI, title, venue, year, and page/article fields for the final citation set. |",
            "| Author, funding, and code/data release metadata | These require advisor/institution confirmation and should not be guessed. | Fill the metadata workbench, including affiliations, acknowledgments, funding, and release boundary. |",
            "| Final IEEE manuscript package | `main.tex`, final BibTeX, figures, cover letter, and metadata depend on the manual gates above. | Use `paper/ieee_trans/main_tex_preflight.md` after manual gates close. |",
        ]
    )
    lines.extend([""])
    lines.extend(render_server_snapshot(rows))
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `Local rest status` answers whether the current evidence, manuscript draft, and guardrail package are coherent before final manual packaging.",
            "- `Submission status` answers whether the paper can be submitted now; it must remain not ready while manual final gates are pending.",
            "- `READY` means the relevant artifact or guardrail exists and passed a zero-missing audit where applicable.",
            "- `PENDING` means the item is intentionally waiting for complete experiments or human confirmation.",
            "- `MISSING` means a local non-result item still needs repair before resting.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    checks = build_checks()
    REPORT_PATH.write_text(render_report(checks), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_scalegate_post_result_runbook_audit.md"
RUNBOOK_PATH = ROOT / "paper/ieee_scalegate_post_result_runbook.md"
SERVER_HISTORY_PATH = ROOT / "paper/tables/ieee_server_status_history.csv"
RESULT_GATE_PATH = ROOT / "paper/ieee_scalegate_result_gate_audit.md"
METHOD_DECISION_PATH = ROOT / "paper/ieee_scalegate_method_decision_audit.md"

MIN_EPOCHS = 100
SCALEGATE_RUNS = [
    "yolo11n_p2_scalegate_960_visdrone",
    "yolo11n_p2_scalegate_960_uavdt",
]


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


@dataclass(frozen=True)
class RunStatus:
    name: str
    status: str = "UNKNOWN"
    epochs: int = 0

    @property
    def is_remote_complete(self) -> bool:
        return self.status == "READY" and self.epochs >= MIN_EPOCHS


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_summary_value(text: str, key: str) -> str | None:
    match = re.search(rf"- {re.escape(key)}: ([^\n]+)", text)
    return match.group(1).strip() if match else None


def parse_int(value: str | None) -> int:
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def latest_server_rows() -> dict[str, RunStatus]:
    latest: dict[str, RunStatus] = {name: RunStatus(name=name) for name in SCALEGATE_RUNS}
    if not SERVER_HISTORY_PATH.exists():
        return latest
    with SERVER_HISTORY_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row.get("run", "")
            if name not in latest:
                continue
            latest[name] = RunStatus(
                name=name,
                status=row.get("status", "UNKNOWN"),
                epochs=parse_int(row.get("epochs")),
            )
    return latest


def gate_value(path: Path, key: str, default: str = "n/a") -> str:
    return parse_summary_value(read_text(path), key) or default


def expected_intake_status(remote_complete: int, result_gate: str, method_decision: str) -> str:
    if remote_complete < len(SCALEGATE_RUNS):
        return "WAITING_FOR_REMOTE_COMPLETION"
    if result_gate != "OPEN_FOR_POST_RESULT_INTEGRATION":
        return "REMOTE_COMPLETE_READY_TO_SYNC"
    if method_decision.startswith("LOCKED") or method_decision.startswith("PENDING"):
        return "LOCAL_RESULTS_READY_FOR_DIAGNOSTICS"
    return "READY_FOR_MANUSCRIPT_DECISION"


def contains_check(text: str, area: str, item: str, token: str, action: str) -> Check:
    return Check(
        area,
        item,
        "ready" if token in text else "missing",
        token if token in text else "token not found",
        "" if token in text else action,
    )


def audit() -> list[Check]:
    text = read_text(RUNBOOK_PATH)
    checks: list[Check] = [
        Check(
            "Source",
            "Dynamic runbook exists",
            "ready" if RUNBOOK_PATH.exists() else "missing",
            RUNBOOK_PATH.relative_to(ROOT).as_posix(),
            "" if RUNBOOK_PATH.exists() else "Run tools/build_ieee_scalegate_post_result_runbook.py.",
        )
    ]
    if not text:
        return checks

    runs = latest_server_rows()
    remote_complete = sum(1 for status in runs.values() if status.is_remote_complete)
    result_gate = gate_value(RESULT_GATE_PATH, "Gate status")
    method_decision = gate_value(METHOD_DECISION_PATH, "Decision status")
    expected_status = expected_intake_status(remote_complete, result_gate, method_decision)

    actual_status = parse_summary_value(text, "Intake status")
    actual_remote = parse_summary_value(text, "Remote complete ScaleGate runs")
    expected_remote = f"{remote_complete}/{len(SCALEGATE_RUNS)}"

    checks.append(
        Check(
            "State consistency",
            "Intake status matches gates",
            "ready" if actual_status == expected_status else "missing",
            f"actual={actual_status}; expected={expected_status}",
            "Regenerate the runbook after server status and gate audits.",
        )
    )
    checks.append(
        Check(
            "State consistency",
            "Remote completion count matches server history",
            "ready" if actual_remote == expected_remote else "missing",
            f"actual={actual_remote}; expected={expected_remote}",
            "Refresh server status, rebuild the progress report, and regenerate the runbook.",
        )
    )

    for run_name, status in runs.items():
        token = f"| {run_name} | {status.status} | {status.epochs}/{MIN_EPOCHS}"
        checks.append(
            Check(
                "State consistency",
                f"{run_name} row matches server history",
                "ready" if token in text else "missing",
                token if token in text else f"expected status={status.status}; epochs={status.epochs}",
                "Regenerate the runbook after refreshing server history.",
            )
        )

    required_command_tokens = [
        ("Command gate", "Status refresh command", r"tools\check_ieee_server_status.ps1"),
        ("Command gate", "Guarded intake check command", r"tools\intake_ieee_scalegate_results.ps1 -CheckOnly"),
        ("Command gate", "Guarded sync command", r"tools\intake_ieee_scalegate_results.ps1"),
        ("Command gate", "Guarded diagnostics command", r"tools\intake_ieee_scalegate_results.ps1 -RunDiagnostics"),
        ("Command gate", "Audit refresh command", r"tools\run_ieee_audits.py"),
    ]
    for area, item, token in required_command_tokens:
        checks.append(contains_check(text, area, item, token, "Restore the guarded command sequence."))

    claim_locks = [
        ("Claim lock", "No manual partial copy", "Do not manually copy partial ScaleGate run directories"),
        ("Claim lock", "No premature paper table rows", "Do not add ScaleGate rows to paper-facing tables before"),
        ("Claim lock", "No premature method promotion", "Do not promote ScaleGate in the title, abstract"),
        ("Claim lock", "Progress metrics are monitoring only", "progress mAP values in this file as monitoring only"),
    ]
    for area, item, token in claim_locks:
        checks.append(contains_check(text, area, item, token, "Restore this claim lock."))

    if remote_complete < len(SCALEGATE_RUNS):
        checks.append(
            contains_check(
                text,
                "Current-state lock",
                "Partial sync remains forbidden while remote incomplete",
                "do not sync partial ScaleGate runs",
                "Runbook must tell the reader not to sync partial runs.",
            )
        )

    return checks


def status_label(status: str) -> str:
    return {"ready": "READY", "missing": "MISSING"}[status]


def render(checks: list[Check]) -> str:
    ready = sum(1 for check in checks if check.status == "ready")
    missing = sum(1 for check in checks if check.status == "missing")
    lines = [
        "# IEEE ScaleGate Post-Result Runbook Audit",
        "",
        "This report is generated by `tools/check_ieee_scalegate_post_result_runbook.py`. It checks that the generated ScaleGate runbook matches the latest server history and preserves the paper-claim locks.",
        "",
        "It does not launch training, sync files, or edit result tables.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(checks)}",
        f"- Ready: {ready}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        evidence = check.evidence.replace("\n", "<br>")
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{evidence}` | {check.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the generated runbook is consistent with the latest local evidence.",
            "- `MISSING` means the runbook is stale or missing a required command/claim lock.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    checks = audit()
    REPORT_PATH.write_text(render(checks), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

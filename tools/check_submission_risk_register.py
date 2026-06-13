from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = ROOT / "paper/CEA_SUBMISSION_RISK_REGISTER.md"
REPORT_PATH = ROOT / "paper/submission_risk_register_audit.md"


VALID_STATUSES = {"Pending", "Active", "Accepted", "Resolved"}
VALID_SEVERITIES = {"High", "Medium", "Low"}
REQUIRED_RISKS = {f"R{i}" for i in range(1, 13)}


@dataclass
class RiskCheck:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
        "partial": "PARTIAL",
    }[status]


def parse_table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("| R"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 7:
            rows.append(cells[:7])
    return rows


def extract_paths(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


def audit() -> list[RiskCheck]:
    if not REGISTER_PATH.exists():
        return [
            RiskCheck(
                "Risk register exists",
                "missing",
                str(REGISTER_PATH.relative_to(ROOT)),
                "Create the CEA submission risk register.",
            )
        ]

    text = REGISTER_PATH.read_text(encoding="utf-8")
    rows = parse_table_rows(text)
    checks: list[RiskCheck] = [
        RiskCheck(
            "Risk register exists",
            "ready",
            str(REGISTER_PATH.relative_to(ROOT)),
        ),
        RiskCheck(
            "Risk row count",
            "ready" if len(rows) >= len(REQUIRED_RISKS) else "missing",
            f"{len(rows)} risk rows",
            "" if len(rows) >= len(REQUIRED_RISKS) else "Add all required risk rows R1-R12.",
        ),
    ]

    seen_ids = {row[0] for row in rows}
    missing_ids = sorted(REQUIRED_RISKS - seen_ids)
    checks.append(
        RiskCheck(
            "Required risk IDs",
            "ready" if not missing_ids else "missing",
            "all R1-R12 present" if not missing_ids else ", ".join(missing_ids),
            "" if not missing_ids else "Add missing risk IDs to the register.",
        )
    )

    duplicate_ids = sorted({risk_id for risk_id in seen_ids if [row[0] for row in rows].count(risk_id) > 1})
    checks.append(
        RiskCheck(
            "Unique risk IDs",
            "ready" if not duplicate_ids else "missing",
            "no duplicate risk IDs" if not duplicate_ids else ", ".join(duplicate_ids),
            "" if not duplicate_ids else "Merge or rename duplicate risk IDs.",
        )
    )

    invalid_severities = [f"{row[0]}={row[2]}" for row in rows if row[2] not in VALID_SEVERITIES]
    checks.append(
        RiskCheck(
            "Severity vocabulary",
            "ready" if not invalid_severities else "missing",
            "High/Medium/Low only" if not invalid_severities else "; ".join(invalid_severities),
            "" if not invalid_severities else "Use only High, Medium, or Low severity.",
        )
    )

    invalid_statuses = [f"{row[0]}={row[3]}" for row in rows if row[3] not in VALID_STATUSES]
    checks.append(
        RiskCheck(
            "Status vocabulary",
            "ready" if not invalid_statuses else "missing",
            "Pending/Active/Accepted/Resolved only" if not invalid_statuses else "; ".join(invalid_statuses),
            "" if not invalid_statuses else "Use the documented status vocabulary.",
        )
    )

    high_without_mitigation = [row[0] for row in rows if row[2] == "High" and len(row[6]) < 20]
    checks.append(
        RiskCheck(
            "High-risk mitigation coverage",
            "ready" if not high_without_mitigation else "missing",
            "all high risks include mitigation" if not high_without_mitigation else ", ".join(high_without_mitigation),
            "" if not high_without_mitigation else "Add concrete mitigation actions for high-risk items.",
        )
    )

    referenced_paths: list[tuple[str, str]] = []
    for row in rows:
        for rel_path in extract_paths(row[5]):
            referenced_paths.append((row[0], rel_path))

    missing_paths = [
        f"{risk_id}:{rel_path}"
        for risk_id, rel_path in referenced_paths
        if not (ROOT / rel_path).exists()
    ]
    checks.append(
        RiskCheck(
            "Referenced evidence files exist",
            "ready" if not missing_paths else "missing",
            f"{len(referenced_paths)} referenced paths checked" if not missing_paths else "; ".join(missing_paths[:8]),
            "" if not missing_paths else "Create missing evidence files or update the risk evidence path.",
        )
    )

    pending_high = [row[0] for row in rows if row[2] == "High" and row[3] == "Pending"]
    checks.append(
        RiskCheck(
            "High-risk unresolved gate",
            "partial" if pending_high else "ready",
            "pending high risks: " + ", ".join(pending_high) if pending_high else "no high-risk pending gates",
            "Resolve after fair-comparison experiments complete." if pending_high else "",
        )
    )

    return checks


def write_report(checks: list[RiskCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# Submission Risk Register Audit",
        "",
        "This report is generated by `tools/check_submission_risk_register.py`. It checks whether the CEA submission risk register has complete risk IDs, controlled severity/status values, mitigation coverage, and existing evidence paths. It does not validate or add experiment results.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Partial: {partial}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the risk-register structure or evidence path is complete.",
            "- `PARTIAL` means the register is structurally sound but still contains real unresolved submission risk.",
            "- `MISSING` means the register itself, an expected row, a required mitigation, or a referenced evidence file is absent.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

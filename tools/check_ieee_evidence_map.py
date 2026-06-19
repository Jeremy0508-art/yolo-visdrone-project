from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "paper/ieee_trans/evidence_to_sections.csv"
REPORT_PATH = ROOT / "paper/ieee_evidence_map_audit.md"


@dataclass(frozen=True)
class Check:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_label(status: str) -> str:
    return {"ready": "READY", "missing": "MISSING"}[status]


def read_rows() -> list[dict[str, str]]:
    if not MAP_PATH.exists():
        return []
    with MAP_PATH.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def split_sources(source: str) -> list[str]:
    return [part.strip() for part in source.split(";") if part.strip()]


def source_path_exists(source: str) -> bool:
    if source.endswith(" missing"):
        return True
    if source.startswith("Future ") or source.startswith("future "):
        return True
    if source.startswith("UAVDT results missing"):
        return True
    path = ROOT / source
    return path.exists()


def audit() -> list[Check]:
    rows = read_rows()
    if not rows:
        return [
            Check(
                "Evidence-to-section map exists",
                "missing",
                "paper/ieee_trans/evidence_to_sections.csv",
                "Restore the IEEE evidence-to-section map before manuscript assembly.",
            )
        ]

    checks: list[Check] = [
        Check("Evidence-to-section map exists", "ready", "paper/ieee_trans/evidence_to_sections.csv"),
        Check(
            "Evidence-to-section row count",
            "ready" if len(rows) >= 20 else "missing",
            f"{len(rows)} rows",
            "" if len(rows) >= 20 else "Expand the map so all IEEE sections and major claims are covered.",
        ),
    ]

    sections = {row.get("section", "") for row in rows}
    required_sections = [
        "Front Matter",
        "Cover Letter",
        "Introduction",
        "Related Work",
        "Method",
        "Experiments",
        "Discussion",
        "Conclusion",
    ]
    for section in required_sections:
        checks.append(
            Check(
                f"Section covered: {section}",
                "ready" if section in sections else "missing",
                section if section in sections else "not found",
                "" if section in sections else "Add at least one row for this IEEE manuscript section.",
            )
        )

    statuses = {row.get("status", "") for row in rows}
    for required_status in ["ready", "partially_ready", "locked"]:
        checks.append(
            Check(
                f"Status category present: {required_status}",
                "ready" if required_status in statuses else "missing",
                required_status if required_status in statuses else "not found",
                "" if required_status in statuses else "Use this status category to distinguish evidence readiness.",
            )
        )

    locked_expectations = [
        ("TOFC is the final proposed contribution", "TOFC final method claim"),
        ("UAVDT cross-dataset comparison", "UAVDT cross-dataset claim"),
        ("Generalization beyond VisDrone", "Generalization claim"),
    ]
    for phrase, item in locked_expectations:
        matches = [row for row in rows if phrase in row.get("claim_or_content", "")]
        locked = bool(matches) and all(row.get("status") == "locked" for row in matches)
        checks.append(
            Check(
                f"Locked evidence gate: {item}",
                "ready" if locked else "missing",
                phrase if matches else "not found",
                "" if locked else "Keep this claim locked until complete evidence exists.",
            )
        )

    boundary_expectations = [
        ("Scale-wise small-object recall/precision", "do not describe as AP-small"),
        ("Local scale-bin AP diagnostics", "do not describe as official"),
        ("Speed and complexity for existing models", "Update after any new final model"),
    ]
    for claim, action_token in boundary_expectations:
        matches = [row for row in rows if claim in row.get("claim_or_content", "")]
        ok = bool(matches) and any(action_token in row.get("next_action", "") for row in matches)
        checks.append(
            Check(
                f"Boundary action present: {claim}",
                "ready" if ok else "missing",
                action_token if ok else "not found",
                "" if ok else "Add a manuscript-use boundary for this evidence item.",
            )
        )

    missing_sources: list[str] = []
    for row in rows:
        if row.get("status") == "locked":
            continue
        for source in split_sources(row.get("current_source", "")):
            if not source_path_exists(source):
                missing_sources.append(source)
    checks.append(
        Check(
            "Ready/partial rows reference existing local sources",
            "ready" if not missing_sources else "missing",
            ", ".join(missing_sources[:8]) if missing_sources else "all checked sources exist",
            "" if not missing_sources else "Fix or qualify missing evidence sources before manuscript assembly.",
        )
    )

    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE Evidence-to-Section Map Audit",
        "",
        "This report is generated by `tools/check_ieee_evidence_map.py`. It checks whether `paper/ieee_trans/evidence_to_sections.csv` covers the planned IEEE manuscript sections, keeps locked claims locked, and points ready/partial rows to existing local evidence sources.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check.item} | {status_label(check.status)} | `{check.evidence}` | {check.action} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the mapped section, boundary, or local evidence source is covered.",
            "- `MISSING` means the evidence map should be corrected before final IEEE manuscript assembly.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

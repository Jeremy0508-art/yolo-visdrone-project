from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/claim_boundary_audit.md"
SERVER_SNAPSHOT = ROOT / "paper/cea_server_status_snapshot.md"


SCANNED_FILES = [
    "README.md",
    "paper/README.md",
    "paper/advisor_progress_brief.md",
    "paper/manuscript_submission_candidate.tex",
    "paper/manuscript_submission_candidate.md",
    "paper/manuscript_polished.md",
]


FORBIDDEN_CLAIMS = [
    ("universal superiority", re.compile("全面优于|显著优于主流|优于所有|全面超过")),
    ("unsupported official test-dev claim", re.compile("官方\\s*test-dev\\s*(AP|结果|成绩)|test-dev\\s*官方\\s*(AP|结果|成绩)", re.I)),
    ("all classes improve", re.compile("所有类别.*提升|各类别.*均.*提升")),
    ("no extra cost claim", re.compile("无额外计算成本|无需额外计算成本|不增加计算成本")),
    ("completed fair experiments claim", re.compile("公平对比实验.*全部完成|所有公平对比.*完成")),
    ("final submission ready claim", re.compile("已达到投稿状态|可以正式投稿|最终投稿稿件")),
]

NEGATING_CONTEXT = re.compile("不建议|避免|不能|不得|禁止|尚未|未.*完成|不要|当前不")


REQUIRED_BOUNDARY_PHRASES = [
    ("partial server results excluded", "未完成 100 epoch"),
    ("fair-comparison gate stated", "公平对比"),
    ("paper tables evidence boundary", "paper/tables"),
]


@dataclass
class ClaimCheck:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
    }[status]


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8-sig", errors="ignore")


def line_numbers(text: str, pattern: re.Pattern[str]) -> list[int]:
    hits: list[int] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line) and not NEGATING_CONTEXT.search(line):
            hits.append(number)
    return hits


def latest_partial_values() -> list[str]:
    if not SERVER_SNAPSHOT.exists():
        return []
    text = SERVER_SNAPSHOT.read_text(encoding="utf-8")
    values: list[str] = []
    row_match = re.search(
        r"\| baseline_yolo11n_960_visdrone \| PARTIAL \| [0-9]+ \| [0-9]+ \| ([0-9.]+) \| ([0-9.]+) \|",
        text,
    )
    if row_match:
        values.extend([row_match.group(1), row_match.group(2)])
    return values


def audit() -> list[ClaimCheck]:
    checks: list[ClaimCheck] = []

    for rel_path in SCANNED_FILES:
        path = ROOT / rel_path
        if not path.exists():
            checks.append(
                ClaimCheck(
                    f"Claim-boundary file exists: {rel_path}",
                    "missing",
                    rel_path,
                    "Restore or regenerate this paper-facing text file.",
                )
            )
            continue

        text = read_text(rel_path)
        hits: list[str] = []
        for label, pattern in FORBIDDEN_CLAIMS:
            lines = line_numbers(text, pattern)
            if lines:
                shown = ", ".join(str(n) for n in lines[:5])
                if len(lines) > 5:
                    shown += ", ..."
                hits.append(f"{label} at line {shown}")
        checks.append(
            ClaimCheck(
                f"Forbidden overclaim scan: {rel_path}",
                "ready" if not hits else "missing",
                "no forbidden claim patterns found" if not hits else "; ".join(hits),
                "" if not hits else "Revise the paper-facing text to use evidence-bounded wording.",
            )
        )

    partial_values = latest_partial_values()
    if partial_values:
        for rel_path in SCANNED_FILES:
            path = ROOT / rel_path
            if not path.exists():
                continue
            text = read_text(rel_path)
            found = [value for value in partial_values if value in text]
            checks.append(
                ClaimCheck(
                    f"Partial server metrics excluded: {rel_path}",
                    "ready" if not found else "missing",
                    "partial server mAP values not found" if not found else ", ".join(found),
                    "" if not found else "Remove partial server metrics from paper-facing text.",
                )
            )

    advisor_path = ROOT / "paper/advisor_progress_brief.md"
    if advisor_path.exists():
        advisor_text = advisor_path.read_text(encoding="utf-8-sig")
        for item, phrase in REQUIRED_BOUNDARY_PHRASES:
            checks.append(
                ClaimCheck(
                    f"Advisor brief boundary phrase: {item}",
                    "ready" if phrase in advisor_text else "missing",
                    phrase if phrase in advisor_text else "not found",
                    "" if phrase in advisor_text else "Regenerate or revise the advisor brief.",
                )
            )

    return checks


def write_report(checks: list[ClaimCheck]) -> None:
    total = len(checks)
    ready = sum(1 for check in checks if check.status == "ready")
    missing = sum(1 for check in checks if check.status == "missing")

    lines = [
        "# Claim Boundary Audit",
        "",
        "This report is generated by `tools/check_claim_boundaries.py`. It scans paper-facing text for unsupported overclaims that should not appear before fair-comparison experiments are complete and audited. It intentionally does not scan planning documents that list forbidden phrases as examples.",
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
        lines.append(f"| {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means no configured unsupported claim pattern was found, or a required boundary statement exists.",
            "- `MISSING` means paper-facing text should be revised before sharing or submission.",
            "- Partial server metrics remain progress information only and must not appear in manuscript claims.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

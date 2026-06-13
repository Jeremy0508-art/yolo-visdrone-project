from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "paper/CEA_REVIEWER_RESPONSE_PREP.md"
REPORT_PATH = ROOT / "paper/cea_reviewer_response_prep_audit.md"

REQUIRED_IDS = {f"Q{i}" for i in range(1, 11)}
REQUIRED_THEMES = {
    "Novelty",
    "Fair Comparison",
    "External Baselines",
    "Small Objects",
    "Negative Results",
    "Efficiency",
    "Reproducibility",
    "Dataset And Evaluation",
    "Failure Cases",
    "Journal Formatting",
}
REQUIRED_BOUNDARY_TOKENS = [
    "Do not claim",
    "Do not mix",
    "not official AP",
    "Do not hide",
    "Use measured",
    "official test-dev",
    "manual gates",
]


@dataclass
class MatrixCheck:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
    }[status]


def parse_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("| Q"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 6:
            rows.append(cells[:6])
    return rows


def extract_paths(text: str) -> list[str]:
    paths = re.findall(r"`([^`]+)`", text)
    return [
        path
        for path in paths
        if path.startswith(("paper/", "configs/", "tools/")) and " " not in path
    ]


def audit() -> list[MatrixCheck]:
    if not MATRIX_PATH.exists():
        return [
            MatrixCheck(
                "Reviewer response matrix exists",
                "missing",
                str(MATRIX_PATH.relative_to(ROOT)),
                "Run python tools/build_cea_reviewer_response_prep.py.",
            )
        ]

    text = MATRIX_PATH.read_text(encoding="utf-8-sig")
    rows = parse_rows(text)
    checks: list[MatrixCheck] = [
        MatrixCheck("Reviewer response matrix exists", "ready", str(MATRIX_PATH.relative_to(ROOT))),
        MatrixCheck(
            "Question row count",
            "ready" if len(rows) >= len(REQUIRED_IDS) else "missing",
            f"{len(rows)} question rows",
            "" if len(rows) >= len(REQUIRED_IDS) else "Add reviewer-question rows Q1-Q10.",
        ),
    ]

    seen_ids = {row[0] for row in rows}
    missing_ids = sorted(REQUIRED_IDS - seen_ids)
    checks.append(
        MatrixCheck(
            "Required question IDs",
            "ready" if not missing_ids else "missing",
            "all Q1-Q10 present" if not missing_ids else ", ".join(missing_ids),
            "" if not missing_ids else "Add missing question IDs.",
        )
    )

    themes = {row[1] for row in rows}
    missing_themes = sorted(REQUIRED_THEMES - themes)
    checks.append(
        MatrixCheck(
            "Required review themes",
            "ready" if not missing_themes else "missing",
            "all required themes present" if not missing_themes else ", ".join(missing_themes),
            "" if not missing_themes else "Add missing reviewer themes.",
        )
    )

    missing_boundary_tokens = [token for token in REQUIRED_BOUNDARY_TOKENS if token not in text]
    checks.append(
        MatrixCheck(
            "Response-boundary coverage",
            "ready" if not missing_boundary_tokens else "missing",
            "all boundary tokens present" if not missing_boundary_tokens else ", ".join(missing_boundary_tokens),
            "" if not missing_boundary_tokens else "Add explicit response-boundary statements.",
        )
    )

    paths = extract_paths(text)
    missing_paths = [path for path in paths if not (ROOT / path).exists()]
    checks.append(
        MatrixCheck(
            "Referenced evidence files exist",
            "ready" if not missing_paths else "missing",
            f"{len(paths)} evidence paths checked" if not missing_paths else "; ".join(missing_paths[:8]),
            "" if not missing_paths else "Create missing evidence files or update matrix paths.",
        )
    )

    required_commands = [
        "tools/sync_cea_server_results.ps1",
        "tools/run_paper_audits.py",
    ]
    missing_commands = [command for command in required_commands if command not in text]
    checks.append(
        MatrixCheck(
            "Post-result workflow commands",
            "ready" if not missing_commands else "missing",
            "sync and audit commands present" if not missing_commands else ", ".join(missing_commands),
            "" if not missing_commands else "Add the missing post-result workflow command references.",
        )
    )

    return checks


def write_report(checks: list[MatrixCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# CEA Reviewer Response Preparation Audit",
        "",
        "This report is generated by `tools/check_cea_reviewer_response_prep.py`. It checks whether the reviewer-response preparation matrix covers the expected CEA-facing review questions, response boundaries, evidence paths, and post-result workflow commands.",
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
            "- `READY` means the reviewer-response matrix has the expected structure, evidence links, and boundary statements.",
            "- `MISSING` means a required reviewer-question category, evidence file, or workflow command is absent.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

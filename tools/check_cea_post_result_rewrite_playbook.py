from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK_PATH = ROOT / "paper/CEA_POST_RESULT_REWRITE_PLAYBOOK.md"
REPORT_PATH = ROOT / "paper/cea_post_result_rewrite_playbook_audit.md"

REQUIRED_IDS = {f"W{i}" for i in range(1, 13)}
REQUIRED_SECTIONS = {
    "Abstract",
    "Introduction",
    "Related Work",
    "Method",
    "Experiment Setup",
    "Main Results",
    "Ablation Study",
    "Small-Object Analysis",
    "Efficiency Analysis",
    "Discussion And Limitations",
    "Conclusion",
    "Final PDF And GitHub",
}
REQUIRED_BOUNDARIES = [
    "partial server metrics",
    "unsupported superiority claims",
    "Do not invent",
    "Do not hide",
    "official AP",
    "real-time deployment",
    "manual journal-template",
]
REQUIRED_WORKFLOW_TOKENS = [
    "tools/sync_cea_server_results.ps1 -MinEpochs 100",
    "python tools/run_paper_audits.py",
    "Rebuild the PDF",
    "GitHub",
]


@dataclass
class PlaybookCheck:
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
        if not line.startswith("| W"):
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
        if path.startswith(("paper/", "configs/", "tools/")) and " " not in path and "**" not in path
    ]


def audit() -> list[PlaybookCheck]:
    if not PLAYBOOK_PATH.exists():
        return [
            PlaybookCheck(
                "Post-result rewrite playbook exists",
                "missing",
                str(PLAYBOOK_PATH.relative_to(ROOT)),
                "Run python tools/build_cea_post_result_rewrite_playbook.py.",
            )
        ]

    text = PLAYBOOK_PATH.read_text(encoding="utf-8-sig")
    rows = parse_rows(text)
    checks: list[PlaybookCheck] = [
        PlaybookCheck("Post-result rewrite playbook exists", "ready", str(PLAYBOOK_PATH.relative_to(ROOT))),
        PlaybookCheck(
            "Rewrite task row count",
            "ready" if len(rows) >= len(REQUIRED_IDS) else "missing",
            f"{len(rows)} rewrite task rows",
            "" if len(rows) >= len(REQUIRED_IDS) else "Add rewrite tasks W1-W12.",
        ),
    ]

    seen_ids = {row[0] for row in rows}
    missing_ids = sorted(REQUIRED_IDS - seen_ids)
    checks.append(
        PlaybookCheck(
            "Required rewrite IDs",
            "ready" if not missing_ids else "missing",
            "all W1-W12 present" if not missing_ids else ", ".join(missing_ids),
            "" if not missing_ids else "Add missing rewrite task IDs.",
        )
    )

    sections = {row[1] for row in rows}
    missing_sections = sorted(REQUIRED_SECTIONS - sections)
    checks.append(
        PlaybookCheck(
            "Required manuscript sections",
            "ready" if not missing_sections else "missing",
            "all required sections present" if not missing_sections else ", ".join(missing_sections),
            "" if not missing_sections else "Add missing manuscript-section rewrite tasks.",
        )
    )

    missing_boundaries = [token for token in REQUIRED_BOUNDARIES if token not in text]
    checks.append(
        PlaybookCheck(
            "Forbidden-claim boundaries",
            "ready" if not missing_boundaries else "missing",
            "all boundary tokens present" if not missing_boundaries else ", ".join(missing_boundaries),
            "" if not missing_boundaries else "Add explicit forbidden-claim boundaries.",
        )
    )

    paths = extract_paths(text)
    missing_paths = [path for path in paths if not (ROOT / path).exists()]
    checks.append(
        PlaybookCheck(
            "Referenced evidence files exist",
            "ready" if not missing_paths else "missing",
            f"{len(paths)} evidence paths checked" if not missing_paths else "; ".join(missing_paths[:8]),
            "" if not missing_paths else "Create missing evidence files or update playbook paths.",
        )
    )

    missing_workflow = [token for token in REQUIRED_WORKFLOW_TOKENS if token not in text]
    checks.append(
        PlaybookCheck(
            "Execution workflow coverage",
            "ready" if not missing_workflow else "missing",
            "sync, audit, PDF, and GitHub workflow present" if not missing_workflow else ", ".join(missing_workflow),
            "" if not missing_workflow else "Add missing execution-order workflow tokens.",
        )
    )

    return checks


def write_report(checks: list[PlaybookCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# CEA Post-Result Rewrite Playbook Audit",
        "",
        "This report is generated by `tools/check_cea_post_result_rewrite_playbook.py`. It checks whether the post-result rewrite playbook covers the expected manuscript sections, evidence paths, forbidden-claim boundaries, and final sync/audit/PDF/GitHub workflow.",
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
            "- `READY` means the rewrite playbook has the expected structure, evidence links, and claim boundaries.",
            "- `MISSING` means a required rewrite task, evidence file, claim boundary, or workflow step is absent.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

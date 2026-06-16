from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md"


@dataclass
class PreflightCheck:
    category: str
    item: str
    status: str
    evidence: str
    action: str


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def local_status(rel_path: str) -> str:
    return "ready" if exists(rel_path) else "missing"


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def build_checks() -> list[PreflightCheck]:
    checks: list[PreflightCheck] = []

    for item, path, action in [
        (
            "Current PDF preview",
            "paper/manuscript_submission_candidate.pdf",
            "Rebuild the PDF after the last manuscript edit.",
        ),
        (
            "Current LaTeX source",
            "paper/manuscript_submission_candidate.tex",
            "Restore the LaTeX source before final editing.",
        ),
        (
            "Submission audit dashboard",
            "paper/submission_audit_dashboard.md",
            "Run python tools/run_paper_audits.py.",
        ),
        (
            "Submission package checklist",
            "paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md",
            "Run python tools/build_cea_submission_package_checklist.py.",
        ),
        (
            "Evidence audit",
            "paper/evidence_audit.md",
            "Run python tools/build_evidence_audit.py.",
        ),
        (
            "Reproducibility commands",
            "paper/commands.md",
            "Restore the reproducibility command notes.",
        ),
        (
            "Submission metadata worksheet",
            "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md",
            "Create the worksheet for author, affiliation, funding, declaration, and upload metadata.",
        ),
    ]:
        status = local_status(path)
        checks.append(
            PreflightCheck(
                "Local Package",
                item,
                status,
                path,
                "" if status == "ready" else action,
            )
        )

    synced_text = read_text("paper/synced_fair_experiment_artifacts_audit.md")
    consistency_text = read_text("paper/paper_consistency_audit.md")
    fair_integration_ready = (
        "Pending: 0" in synced_text
        and "Missing: 0" in synced_text
        and "Completed comparison rows trace to local results and best weights" in consistency_text
    )

    manual_items = [
        (
            "Official CEA template",
            "pending",
            "manual verification required",
            "Download and compare against the current official template or upload instructions before final submission.",
        ),
        (
            "Submission file type",
            "pending",
            "manual verification required",
            "Confirm whether the journal system requires Word, PDF, LaTeX source, figures, or a combined package.",
        ),
        (
            "Title, authors, affiliations, and email",
            "pending",
            "manual verification required",
            "Verify final author order, corresponding author, institution names, and contact email in the submission system.",
        ),
        (
            "Funding and acknowledgement statements",
            "pending",
            "manual verification required",
            "Confirm whether funding, acknowledgement, conflict-of-interest, and data-availability statements are required.",
        ),
        (
            "Chinese and English abstracts and keywords",
            "pending",
            "manual verification required",
            "Manually check wording, length, and keyword consistency after the final result rewrite.",
        ),
        (
            "Final PDF page-by-page visual review",
            "pending",
            "manual verification required",
            "Inspect the compiled PDF for figure placement, table width, captions, references, blank pages, and unreadable labels.",
        ),
        (
            "Completed fair-comparison experiment integration",
            "ready" if fair_integration_ready else "pending",
            "synced artifacts and paper consistency audits" if fair_integration_ready else "manual verification required",
            "" if fair_integration_ready else "Only mark ready after all 100-epoch server runs are synced, audited, and reflected in tables and manuscript text.",
        ),
        (
            "GitHub public view",
            "pending",
            "manual verification required",
            "Open the repository page after the final push and verify that README, paper links, and command notes render cleanly.",
        ),
    ]
    for item, status, evidence, action in manual_items:
        checks.append(
            PreflightCheck(
                "Manual Submission Gate",
                item,
                status,
                evidence,
                action,
            )
        )

    return checks


def write_report(checks: list[PreflightCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# CEA Manual Submission Preflight",
        "",
        "This file is generated by `tools/build_cea_manual_submission_preflight.py`.",
        "",
        "It records the final manual checks that cannot be proven by local scripts. It is not an official instruction page for `Computer Engineering and Applications`; the current journal website and submission system must be checked before upload.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Category | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.category} | {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the local package item exists.",
            "- `PENDING` means a human must verify the item in the final manuscript, GitHub page, or journal-system login.",
            "- `MISSING` means a required local package file is absent.",
            "",
            "This report intentionally keeps manual journal-system checks as `PENDING` until the final upload preparation stage.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = build_checks()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md"


@dataclass
class PackageCheck:
    category: str
    item: str
    status: str
    evidence: str
    action: str = ""


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def status_from_file(rel_path: str) -> str:
    return "ready" if exists(rel_path) else "missing"


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def count_csv_rows(rel_path: str) -> int:
    path = ROOT / rel_path
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def fair_experiment_counts() -> tuple[int, int, str]:
    text = read_text("paper/post_sync_update_checklist.md")
    if "0/5 completed experiments" in text:
        return 0, 5, "post-sync checklist reports 0/5 completed experiments"
    status_path = ROOT / "paper/tables/cea_experiment_status.csv"
    if not status_path.exists():
        return 0, 5, "fair experiment status table missing"
    total = 0
    complete = 0
    with status_path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            total += 1
            state = " ".join(str(v).lower() for v in row.values())
            if "complete" in state or "ready" in state:
                complete += 1
    return complete, total or 5, f"{complete}/{total or 5} completed experiments"


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def build_checks() -> list[PackageCheck]:
    checks: list[PackageCheck] = []

    for item, path in [
        ("LaTeX candidate source", "paper/manuscript_submission_candidate.tex"),
        ("Compiled PDF preview", "paper/manuscript_submission_candidate.pdf"),
        ("Paper workspace README", "paper/README.md"),
        ("Project README", "README.md"),
    ]:
        checks.append(
            PackageCheck(
                "Manuscript",
                item,
                status_from_file(path),
                path,
                "" if exists(path) else "Generate or restore this manuscript-facing file.",
            )
        )

    for item, path in [
        ("Main result table", "paper/tables/main_comparison_for_paper.csv"),
        ("Ablation table", "paper/tables/ablation_results.csv"),
        ("Speed table", "paper/tables/speed_results.csv"),
        ("Complexity table", "paper/tables/model_complexity.csv"),
        ("Per-class table", "paper/tables/per_class_results.csv"),
        ("Scale-group table", "paper/tables/scale_group_results.csv"),
    ]:
        rows = count_csv_rows(path)
        checks.append(
            PackageCheck(
                "Tables",
                item,
                "ready" if rows > 0 else "missing",
                f"{path}; {rows} data rows",
                "" if rows > 0 else "Regenerate from audited experiment outputs.",
            )
        )

    figure_paths = [
        "paper/figures/method/hrpca_yolo11n_overview.png",
        "paper/figures/scale_analysis/object_scale_distribution.png",
        "paper/figures/scale_analysis/scale_group_recall.png",
        "paper/figures/tradeoff/accuracy_speed_tradeoff.png",
        "paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg",
        "paper/figures/failure_cases/p2_case_contact_sheet.jpg",
    ]
    missing_figures = [path for path in figure_paths if not exists(path)]
    checks.append(
        PackageCheck(
            "Figures",
            "Core manuscript figures",
            "ready" if not missing_figures else "missing",
            f"{len(figure_paths) - len(missing_figures)}/{len(figure_paths)} figures present",
            "" if not missing_figures else "Regenerate missing figure files before final PDF build.",
        )
    )

    for item, path in [
        ("Submission audit dashboard", "paper/submission_audit_dashboard.md"),
        ("Evidence audit", "paper/evidence_audit.md"),
        ("Number trace audit", "paper/manuscript_number_trace_audit.md"),
        ("Claim boundary audit", "paper/claim_boundary_audit.md"),
        ("Result interpretation matrix audit", "paper/result_interpretation_matrix_audit.md"),
        ("Reviewer response prep audit", "paper/cea_reviewer_response_prep_audit.md"),
        ("PDF readability audit", "paper/pdf_text_readability_audit.md"),
        ("PDF layout health audit", "paper/pdf_layout_health_audit.md"),
        ("Synced fair-experiment artifacts audit", "paper/synced_fair_experiment_artifacts_audit.md"),
        ("Reference verification audit", "paper/reference_verification_audit.md"),
        ("Manual submission preflight", "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md"),
    ]:
        checks.append(
            PackageCheck(
                "Evidence",
                item,
                status_from_file(path),
                path,
                "" if exists(path) else "Run python tools/run_paper_audits.py.",
            )
        )

    complete, total, evidence = fair_experiment_counts()
    checks.append(
        PackageCheck(
            "Experiment Gate",
            "Fair-comparison server experiments",
            "ready" if total > 0 and complete == total else "pending",
            evidence,
            "Wait for complete 100-epoch runs, then sync with tools/sync_cea_server_results.ps1 -MinEpochs 100.",
        )
    )

    checks.append(
        PackageCheck(
            "Experiment Gate",
            "Post-sync manuscript rewrite",
            "pending" if complete != total else "ready",
            "abstract, fair-resolution section, mainstream YOLO section, and conclusion depend on audited synced results",
            "Rewrite only after refreshed tables and audits are complete.",
        )
    )

    for item, path in [
        ("Reproducibility commands", "paper/commands.md"),
        ("Result integration protocol", "paper/CEA_RESULT_INTEGRATION_PROTOCOL.md"),
        ("Advisor progress brief", "paper/advisor_progress_brief.md"),
    ]:
        checks.append(
            PackageCheck(
                "Supporting Materials",
                item,
                status_from_file(path),
                path,
                "" if exists(path) else "Restore or regenerate supporting material.",
            )
        )

    checks.append(
        PackageCheck(
            "External Submission",
            "CEA official template and upload form",
            "pending",
            "manual verification required on the journal submission website before final upload",
            "Download the current official template and adapt this LaTeX/PDF package if the journal system requires Word or a specific format.",
        )
    )

    return checks


def write_report(checks: list[PackageCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# CEA Submission Package Checklist",
        "",
        "This checklist is generated by `tools/build_cea_submission_package_checklist.py`. It organizes the project-facing materials needed before preparing a submission package for `Computer Engineering and Applications`.",
        "",
        "It is not an official journal instruction page. Before final upload, manually verify the current journal template, file type, author information, and submission-system requirements on the journal website.",
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
            "- `READY` means the local package item exists or the local gate is satisfied.",
            "- `PENDING` means the item depends on completed server experiments or external journal-system verification.",
            "- `MISSING` means a local file is absent and should be regenerated before final submission preparation.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = build_checks()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

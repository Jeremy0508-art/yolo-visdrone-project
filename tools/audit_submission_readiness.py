from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Check:
    category: str
    item: str
    status: str
    evidence: str
    next_action: str = ""


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def count_csv_rows(path: str) -> int:
    p = ROOT / path
    if not p.exists():
        return 0
    with p.open(newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def read_csv(path: str) -> list[dict[str, str]]:
    p = ROOT / path
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "partial": "PARTIAL",
        "missing": "MISSING",
        "pending": "PENDING",
    }.get(status, status.upper())


def audit() -> list[Check]:
    checks: list[Check] = []

    required_docs = [
        ("Final CEA submission execution plan", "paper/CEA_FINAL_SUBMISSION_EXECUTION_PLAN.md"),
        ("CEA result interpretation matrix", "paper/CEA_RESULT_INTERPRETATION_MATRIX.md"),
        ("CEA section evidence map", "paper/CEA_SECTION_EVIDENCE_MAP.md"),
        ("CEA submission risk register", "paper/CEA_SUBMISSION_RISK_REGISTER.md"),
        ("CEA submission readiness 100 plan", "paper/CEA_SUBMISSION_READINESS_100_PLAN.md"),
        ("CEA full submission execution plan", "paper/CEA_FULL_SUBMISSION_EXECUTION_PLAN.md"),
        ("Master journal plan", "paper/CEA_JOURNAL_MASTER_PLAN.md"),
        ("CEA gap analysis", "paper/CEA_REVIEW_GAP_ANALYSIS.md"),
        ("CEA journal style benchmark", "paper/CEA_JOURNAL_STYLE_BENCHMARK.md"),
        ("Journal manuscript outline", "paper/CEA_JOURNAL_MANUSCRIPT_OUTLINE.md"),
        ("CEA execution log", "paper/CEA_EXECUTION_LOG.md"),
        ("CEA server status snapshot", "paper/cea_server_status_snapshot.md"),
        ("CEA server progress report", "paper/cea_server_progress_report.md"),
        ("CEA result integration protocol", "paper/CEA_RESULT_INTEGRATION_PROTOCOL.md"),
        ("CEA manuscript update queue", "paper/CEA_MANUSCRIPT_UPDATE_QUEUE.md"),
        ("Post-sync manuscript update checklist", "paper/post_sync_update_checklist.md"),
        ("CEA submission package checklist", "paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md"),
        ("CEA manual submission preflight", "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md"),
        ("Advisor progress brief audit", "paper/advisor_progress_brief_audit.md"),
        ("CEA manuscript rewrite blueprint", "paper/CEA_MANUSCRIPT_REWRITE_BLUEPRINT.md"),
        ("Journal manuscript gap audit", "paper/manuscript_journal_gap_audit.md"),
        ("Claim boundary audit", "paper/claim_boundary_audit.md"),
        ("Result interpretation matrix audit", "paper/result_interpretation_matrix_audit.md"),
        ("LaTeX reference audit", "paper/tex_reference_audit.md"),
        ("Reference verification audit", "paper/reference_verification_audit.md"),
        ("LaTeX figure audit", "paper/tex_figure_audit.md"),
        ("LaTeX cross-reference audit", "paper/tex_cross_reference_audit.md"),
        ("LaTeX table source audit", "paper/tex_table_source_audit.md"),
        ("Section evidence map audit", "paper/section_evidence_map_audit.md"),
        ("Submission risk register audit", "paper/submission_risk_register_audit.md"),
        ("Synced fair-experiment artifacts audit", "paper/synced_fair_experiment_artifacts_audit.md"),
        ("Reproducibility commands audit", "paper/repro_commands_audit.md"),
        ("Config inventory audit", "paper/config_inventory_audit.md"),
        ("Text hygiene audit", "paper/text_hygiene_audit.md"),
        ("Project README presentation audit", "paper/project_readme_presentation_audit.md"),
        ("PDF text readability audit", "paper/pdf_text_readability_audit.md"),
        ("PDF layout health audit", "paper/pdf_layout_health_audit.md"),
        ("Submission material manifest", "paper/submission_material_manifest.md"),
        ("Submission audit dashboard", "paper/submission_audit_dashboard.md"),
        ("Advisor progress brief", "paper/advisor_progress_brief.md"),
        ("Evidence audit", "paper/evidence_audit.md"),
        ("Manuscript number trace audit", "paper/manuscript_number_trace_audit.md"),
        ("Manuscript length audit", "paper/manuscript_length_audit.md"),
        ("Submission checklist", "paper/submission_checklist.md"),
        ("Reference verification matrix", "paper/reference_verification_matrix.md"),
        ("Failure case taxonomy", "paper/failure_case_taxonomy.md"),
        ("Reproducibility commands", "paper/commands.md"),
        ("Paper workspace README", "paper/README.md"),
    ]
    for item, path in required_docs:
        checks.append(
            Check(
                "Documents",
                item,
                "ready" if exists(path) else "missing",
                path,
                "" if exists(path) else f"Create {path}",
            )
        )

    manuscript_files = [
        ("LaTeX candidate source", "paper/manuscript_submission_candidate.tex"),
        ("LaTeX candidate PDF", "paper/manuscript_submission_candidate.pdf"),
        ("Markdown polished manuscript", "paper/manuscript_polished.md"),
    ]
    for item, path in manuscript_files:
        checks.append(
            Check(
                "Manuscript",
                item,
                "ready" if exists(path) else "missing",
                path,
                "" if exists(path) else f"Regenerate or restore {path}",
            )
        )

    table_expectations = [
        ("Main result table", "paper/tables/main_results.csv", 5),
        ("Paper comparison table", "paper/tables/main_comparison_for_paper.csv", 5),
        ("Ablation table", "paper/tables/ablation_results.csv", 5),
        ("Speed table", "paper/tables/speed_results.csv", 5),
        ("Complexity table", "paper/tables/model_complexity.csv", 5),
        ("Per-class table", "paper/tables/per_class_results.csv", 5),
        ("Object scale distribution", "paper/tables/object_scale_distribution.csv", 2),
        ("Scale-group matching", "paper/tables/scale_group_results.csv", 6),
        ("Accuracy-speed trade-off source", "paper/tables/accuracy_speed_tradeoff.csv", 5),
        ("Server status history", "paper/tables/cea_server_status_history.csv", 1),
    ]
    for item, path, min_rows in table_expectations:
        rows = count_csv_rows(path)
        checks.append(
            Check(
                "Tables",
                item,
                "ready" if rows >= min_rows else ("partial" if rows else "missing"),
                f"{path} ({rows} rows)",
                "" if rows >= min_rows else "Regenerate from audited results",
            )
        )

    figure_files = [
        ("Method overview", "paper/figures/method/hrpca_yolo11n_overview.png"),
        ("Scale distribution", "paper/figures/scale_analysis/object_scale_distribution.png"),
        ("Scale-group recall", "paper/figures/scale_analysis/scale_group_recall.png"),
        ("Accuracy-speed trade-off", "paper/figures/tradeoff/accuracy_speed_tradeoff.png"),
        ("Best model training curve", "paper/figures/training_curves/p2_coordatt_960_results.png"),
        ("Qualitative result sample", "paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg"),
        ("Failure case contact sheet", "paper/figures/failure_cases/p2_case_contact_sheet.jpg"),
    ]
    for item, path in figure_files:
        checks.append(
            Check(
                "Figures",
                item,
                "ready" if exists(path) else "missing",
                path,
                "" if exists(path) else f"Generate or collect {path}",
            )
        )

    tool_files = [
        ("Server status checker", "tools/check_cea_server_status.ps1"),
        ("Guarded server result sync", "tools/sync_cea_server_results.ps1"),
        ("Paper PDF build script", "tools/build_paper_pdf.ps1"),
        ("Paper table exporter", "tools/export_paper_tables.py"),
        ("Readiness audit script", "tools/audit_submission_readiness.py"),
        ("Paper consistency audit script", "tools/check_paper_consistency.py"),
        ("Claim boundary audit script", "tools/check_claim_boundaries.py"),
        ("Result interpretation matrix audit script", "tools/check_result_interpretation_matrix.py"),
        ("Journal manuscript gap audit script", "tools/check_journal_manuscript_gaps.py"),
        ("LaTeX reference audit script", "tools/check_tex_references.py"),
        ("Reference verification audit script", "tools/check_reference_verification_matrix.py"),
        ("LaTeX figure audit script", "tools/check_tex_figures.py"),
        ("LaTeX cross-reference audit script", "tools/check_tex_cross_references.py"),
        ("LaTeX table source audit script", "tools/check_tex_table_sources.py"),
        ("Reproducibility commands audit script", "tools/check_repro_commands.py"),
        ("Config inventory audit script", "tools/check_config_inventory.py"),
        ("Text hygiene audit script", "tools/check_text_hygiene.py"),
        ("Project README presentation audit script", "tools/check_project_readme_presentation.py"),
        ("PDF text readability audit script", "tools/check_pdf_text_readability.py"),
        ("PDF layout health audit script", "tools/check_pdf_layout_health.py"),
        ("Advisor progress brief builder", "tools/build_advisor_progress_brief.py"),
        ("Advisor progress brief audit script", "tools/check_advisor_progress_brief.py"),
        ("Section evidence map audit script", "tools/check_section_evidence_map.py"),
        ("Submission risk register audit script", "tools/check_submission_risk_register.py"),
        ("Synced fair-experiment artifacts audit script", "tools/check_synced_fair_experiment_artifacts.py"),
        ("CEA server progress report builder", "tools/build_cea_server_progress_report.py"),
        ("Post-sync update checklist builder", "tools/build_post_sync_update_checklist.py"),
        ("Evidence audit builder", "tools/build_evidence_audit.py"),
        ("Manuscript number trace audit script", "tools/check_manuscript_number_trace.py"),
        ("Manuscript length audit script", "tools/check_manuscript_length.py"),
        ("Submission material manifest builder", "tools/build_submission_material_manifest.py"),
        ("Paper audit runner", "tools/run_paper_audits.py"),
        ("Submission audit dashboard script", "tools/build_submission_audit_dashboard.py"),
        ("CEA submission package checklist builder", "tools/build_cea_submission_package_checklist.py"),
        ("CEA manual submission preflight builder", "tools/build_cea_manual_submission_preflight.py"),
    ]
    for item, path in tool_files:
        checks.append(
            Check(
                "Tools",
                item,
                "ready" if exists(path) else "missing",
                path,
                "" if exists(path) else f"Create {path}",
            )
        )

    exp_rows = read_csv("paper/tables/cea_experiment_status.csv")
    for row in exp_rows:
        status = row.get("status", "")
        normalized = "ready" if status == "completed" else ("pending" if status in {"queued", "running"} else "missing")
        checks.append(
            Check(
                "Fair Experiments",
                row.get("experiment", "unknown"),
                normalized,
                f"{row.get('status','')} | {row.get('run_dir','')} | {row.get('config','')}",
                "Sync only after complete 100-epoch run" if normalized == "pending" else "",
            )
        )

    completed_rows = [r for r in read_csv("paper/tables/main_comparison_for_paper.csv") if r.get("run_dir")]
    checks.append(
        Check(
            "Evidence",
            "Completed local paper-facing runs",
            "ready" if len(completed_rows) >= 5 else "partial",
            f"{len(completed_rows)} completed rows in paper/tables/main_comparison_for_paper.csv",
            "Add only completed and audited runs",
        )
    )

    return checks


def write_report(checks: list[Check], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# Submission Readiness Audit",
        "",
        "This report is generated by `tools/audit_submission_readiness.py`. It checks local paper-facing artifacts and records which items are ready, partial, pending, or missing. It does not treat partial server runs as paper evidence.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Partial: {partial}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Category | Item | Status | Evidence | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in checks:
        lines.append(
            f"| {c.category} | {c.item} | {status_symbol(c.status)} | `{c.evidence}` | {c.next_action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the local artifact exists or the table has enough audited rows for the current manuscript stage.",
            "- `PENDING` means the item depends on server experiments that are queued or still running.",
            "- `PARTIAL` means a local artifact exists but is not yet sufficient for final journal submission.",
            "- `MISSING` means the expected local artifact was not found.",
            "",
            "The project should not be considered journal-submission-ready until pending fair-comparison experiments are complete, synced, audited, and reflected in the manuscript.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    output = ROOT / "paper/submission_readiness_audit.md"
    write_report(checks, output)
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

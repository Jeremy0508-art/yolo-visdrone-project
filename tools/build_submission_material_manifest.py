from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/submission_material_manifest.md"


@dataclass
class Material:
    category: str
    item: str
    path: str
    status: str
    note: str = ""


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def count_csv_rows(rel_path: str) -> int:
    path = ROOT / rel_path
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def file_size_note(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return "missing"
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def add_file(materials: list[Material], category: str, item: str, rel_path: str, note: str = "") -> None:
    materials.append(
        Material(
            category=category,
            item=item,
            path=rel_path,
            status="READY" if exists(rel_path) else "MISSING",
            note=note or file_size_note(rel_path),
        )
    )


def build_materials() -> list[Material]:
    materials: list[Material] = []

    for item, path in [
        ("LaTeX source", "paper/manuscript_submission_candidate.tex"),
        ("Compiled PDF", "paper/manuscript_submission_candidate.pdf"),
        ("Paper workspace README", "paper/README.md"),
        ("Final CEA submission execution plan", "paper/CEA_FINAL_SUBMISSION_EXECUTION_PLAN.md"),
        ("CEA result interpretation matrix", "paper/CEA_RESULT_INTERPRETATION_MATRIX.md"),
        ("CEA section evidence map", "paper/CEA_SECTION_EVIDENCE_MAP.md"),
        ("Submission checklist", "paper/submission_checklist.md"),
        ("Reproducibility commands", "paper/commands.md"),
        ("Result integration protocol", "paper/CEA_RESULT_INTEGRATION_PROTOCOL.md"),
        ("Post-sync manuscript update checklist", "paper/post_sync_update_checklist.md"),
        ("Execution log", "paper/CEA_EXECUTION_LOG.md"),
        ("Server status snapshot", "paper/cea_server_status_snapshot.md"),
        ("Server progress report", "paper/cea_server_progress_report.md"),
    ]:
        add_file(materials, "Core Documents", item, path)

    for item, path in [
        ("Main comparison table", "paper/tables/main_comparison_for_paper.csv"),
        ("Ablation table", "paper/tables/ablation_results.csv"),
        ("Speed table", "paper/tables/speed_results.csv"),
        ("Complexity table", "paper/tables/model_complexity.csv"),
        ("Per-class table", "paper/tables/per_class_results.csv"),
        ("Object scale distribution table", "paper/tables/object_scale_distribution.csv"),
        ("Scale-group matching table", "paper/tables/scale_group_results.csv"),
        ("Accuracy-speed trade-off table", "paper/tables/accuracy_speed_tradeoff.csv"),
        ("Fair experiment status table", "paper/tables/cea_experiment_status.csv"),
        ("Server status history table", "paper/tables/cea_server_status_history.csv"),
    ]:
        rows = count_csv_rows(path)
        add_file(materials, "Tables", item, path, f"{rows} data rows")

    for item, path in [
        ("Method overview figure", "paper/figures/method/hrpca_yolo11n_overview.png"),
        ("Training curve figure", "paper/figures/training_curves/p2_coordatt_960_results.png"),
        ("PR curve figure", "paper/figures/training_curves/p2_coordatt_960_pr_curve.png"),
        ("Confusion matrix figure", "paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png"),
        ("Qualitative prediction figure", "paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg"),
        ("Failure-case figure", "paper/figures/failure_cases/p2_case_contact_sheet.jpg"),
        ("Object-scale distribution figure", "paper/figures/scale_analysis/object_scale_distribution.png"),
        ("Scale-group recall figure", "paper/figures/scale_analysis/scale_group_recall.png"),
        ("Accuracy-speed trade-off figure", "paper/figures/tradeoff/accuracy_speed_tradeoff.png"),
    ]:
        add_file(materials, "Figures", item, path)

    for item, path in [
        ("Submission audit dashboard", "paper/submission_audit_dashboard.md"),
        ("Submission readiness audit", "paper/submission_readiness_audit.md"),
        ("Evidence audit", "paper/evidence_audit.md"),
        ("Manuscript number trace audit", "paper/manuscript_number_trace_audit.md"),
        ("Journal manuscript gap audit", "paper/manuscript_journal_gap_audit.md"),
        ("Paper consistency audit", "paper/paper_consistency_audit.md"),
        ("LaTeX reference audit", "paper/tex_reference_audit.md"),
        ("LaTeX figure audit", "paper/tex_figure_audit.md"),
        ("LaTeX table-source audit", "paper/tex_table_source_audit.md"),
        ("Section evidence map audit", "paper/section_evidence_map_audit.md"),
        ("Reproducibility command audit", "paper/repro_commands_audit.md"),
        ("Config inventory audit", "paper/config_inventory_audit.md"),
        ("Text hygiene audit", "paper/text_hygiene_audit.md"),
    ]:
        add_file(materials, "Audits", item, path)

    return materials


def write_report(materials: list[Material]) -> None:
    total = len(materials)
    ready = sum(1 for item in materials if item.status == "READY")
    missing = sum(1 for item in materials if item.status == "MISSING")

    lines = [
        "# Submission Material Manifest",
        "",
        "This manifest is generated by `tools/build_submission_material_manifest.py`. It lists the paper-facing documents, tables, figures, and audit reports that form the current submission material package.",
        "",
        "It is a material index, not a claim that the manuscript is final-submission-ready. The current gate remains the completion and audited integration of the pending fair-comparison server experiments.",
        "",
        "## Summary",
        "",
        f"- Total materials: {total}",
        f"- Ready: {ready}",
        f"- Missing: {missing}",
        "",
        "## Materials",
        "",
        "| Category | Item | Status | Path | Note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for material in materials:
        lines.append(
            f"| {material.category} | {material.item} | {material.status} | `{material.path}` | {material.note} |"
        )

    lines.extend(
        [
            "",
            "## Use",
            "",
            "- Use `paper/manuscript_submission_candidate.pdf` as the current PDF preview.",
            "- Use `paper/submission_audit_dashboard.md` to inspect readiness gates.",
            "- Use `paper/evidence_audit.md` to trace paper-facing values back to tables and artifacts.",
            "- Use `paper/CEA_RESULT_INTEGRATION_PROTOCOL.md` before integrating server-side fair-comparison results.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    materials = build_materials()
    write_report(materials)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

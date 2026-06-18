from __future__ import annotations

import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ZIP = ROOT / "paper/advisor_review_package.zip"
MANIFEST = ROOT / "paper/advisor_review_package_manifest.md"


@dataclass(frozen=True)
class PackageItem:
    path: str
    note: str


PACKAGE_ITEMS = [
    PackageItem("README.md", "Repository-level project introduction."),
    PackageItem("paper/README.md", "Paper workspace navigation."),
    PackageItem("paper/manuscript_submission_candidate.pdf", "Current PDF manuscript preview."),
    PackageItem("paper/manuscript_submission_candidate.tex", "Current LaTeX source."),
    PackageItem("paper/cea_template_migration/manuscript_cea_template_draft.docx", "First-pass CEA Word-template migration draft."),
    PackageItem("paper/cea_template_migration/cea_word_migration_audit.md", "Audit report for the CEA Word migration draft."),
    PackageItem("paper/advisor_review_note.md", "Short cover note for advisor review."),
    PackageItem("paper/advisor_progress_brief.md", "Short advisor-facing progress brief."),
    PackageItem("paper/CEA_FINAL_HANDOFF_CHECKLIST.md", "Final handoff checklist and claim boundaries."),
    PackageItem("paper/CEA_PDF_VISUAL_REVIEW_FORM.md", "Manual page-by-page PDF review form."),
    PackageItem("paper/pdf_visual_contact_sheet.md", "Generated contact-sheet report for PDF visual review."),
    PackageItem("paper/figures/pdf_review/manuscript_pages_contact_sheet.jpg", "Contact sheet of all manuscript PDF pages."),
    PackageItem("paper/CEA_GITHUB_PUBLIC_VIEW_CHECKLIST.md", "Manual GitHub public rendering checklist."),
    PackageItem("paper/github_public_view_audit.md", "Automated public GitHub reachability and raw README audit."),
    PackageItem("paper/CEA_TEMPLATE_MIGRATION_RECORD.md", "Official template migration record sheet."),
    PackageItem("paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md", "Extracted CEA Word-template requirement summary."),
    PackageItem("paper/templates/计算机工程与应用论文模版.docx", "Local copy of the CEA Word manuscript template provided by the user."),
    PackageItem("paper/CEA_SUBMISSION_METADATA_WORKSHEET.md", "Worksheet for author, affiliation, funding, declaration, and upload metadata."),
    PackageItem("paper/CEA_COVER_LETTER_DRAFT.md", "Bounded draft for editor-facing submission notes."),
    PackageItem("paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md", "Manual submission preflight checklist."),
    PackageItem("paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md", "Local submission package checklist."),
    PackageItem("paper/GOAL_COMPLETION_AUDIT.md", "Requirement-to-evidence audit for the active project objective."),
    PackageItem("paper/submission_audit_dashboard.md", "Current audit dashboard."),
    PackageItem("paper/evidence_audit.md", "Paper-facing number provenance audit."),
    PackageItem("paper/manuscript_number_trace_audit.md", "Trace audit for manuscript numbers."),
    PackageItem("paper/commands.md", "Reproducibility commands."),
    PackageItem("paper/tables/main_comparison_for_paper.csv", "Main comparison table."),
    PackageItem("paper/tables/ablation_results.csv", "Ablation table."),
    PackageItem("paper/tables/speed_results.csv", "Speed benchmark table."),
    PackageItem("paper/tables/model_complexity.csv", "Model complexity table."),
    PackageItem("paper/tables/object_scale_distribution.csv", "Object scale distribution table."),
    PackageItem("paper/tables/scale_group_results.csv", "Scale-group matching table."),
    PackageItem("paper/tables/per_class_results.csv", "Per-class result table."),
    PackageItem("paper/figures/method/hrpca_yolo11n_overview.png", "Method overview figure."),
    PackageItem("paper/figures/tradeoff/accuracy_speed_tradeoff.png", "Accuracy-speed trade-off figure."),
    PackageItem("paper/figures/scale_analysis/object_scale_distribution.png", "Object scale distribution figure."),
    PackageItem("paper/figures/scale_analysis/scale_group_recall.png", "Scale-group recall figure."),
    PackageItem("paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg", "Qualitative prediction figure."),
    PackageItem("paper/figures/failure_cases/p2_case_contact_sheet.jpg", "Failure-case contact sheet."),
]


def file_size(path: Path) -> str:
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def build_package() -> tuple[list[PackageItem], list[PackageItem]]:
    ready: list[PackageItem] = []
    missing: list[PackageItem] = []
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in PACKAGE_ITEMS:
            path = ROOT / item.path
            if not path.exists():
                missing.append(item)
                continue
            archive.write(path, arcname=item.path)
            ready.append(item)
    return ready, missing


def write_manifest(ready: list[PackageItem], missing: list[PackageItem]) -> None:
    lines = [
        "# Advisor Review Package Manifest",
        "",
        "This file is generated by `tools/build_advisor_review_package.py`.",
        "",
        "The zip package is intended for advisor review only. It contains manuscript-facing documents, audits, key tables, and selected figures. It intentionally excludes model weights, full `runs/` directories, datasets, and server logs.",
        "",
        "## Package",
        "",
        f"- Zip file: `paper/advisor_review_package.zip`",
        f"- Ready files: {len(ready)}",
        f"- Missing files: {len(missing)}",
        f"- Zip size: {file_size(OUTPUT_ZIP) if OUTPUT_ZIP.exists() else 'missing'}",
        "",
        "## Included Files",
        "",
        "| Path | Size | Note |",
        "| --- | ---: | --- |",
    ]
    for item in ready:
        path = ROOT / item.path
        lines.append(f"| `{item.path}` | {file_size(path)} | {item.note} |")

    lines.extend(["", "## Missing Files", "", "| Path | Note |", "| --- | --- |"])
    if missing:
        for item in missing:
            lines.append(f"| `{item.path}` | {item.note} |")
    else:
        lines.append("| none |  |")

    lines.extend(
        [
            "",
            "## Use",
            "",
            "1. Share the zip file only for review of the current paper package.",
            "2. Use the included CEA Word template and template summary only as migration evidence; final upload requirements still need journal-system confirmation.",
            "3. Do not treat this package as an official submission archive; it is an advisor-review bundle.",
        ]
    )
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ready, missing = build_package()
    write_manifest(ready, missing)
    print(f"Wrote {OUTPUT_ZIP.relative_to(ROOT)}")
    print(f"Wrote {MANIFEST.relative_to(ROOT)}")
    if missing:
        print(f"Missing files: {len(missing)}")


if __name__ == "__main__":
    main()

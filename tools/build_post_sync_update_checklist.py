from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_STATUS = ROOT / "paper/tables/cea_experiment_status.csv"
REPORT_PATH = ROOT / "paper/post_sync_update_checklist.md"


@dataclass
class ChecklistItem:
    category: str
    item: str
    status: str
    evidence: str
    action: str


def read_experiments() -> list[dict[str, str]]:
    if not EXPERIMENT_STATUS.exists():
        return []
    with EXPERIMENT_STATUS.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def experiment_gate_items(experiments: list[dict[str, str]]) -> list[ChecklistItem]:
    items: list[ChecklistItem] = []
    for row in experiments:
        status = row.get("status", "")
        experiment = row.get("experiment", "unknown")
        run_dir = row.get("run_dir", "")
        if status == "completed":
            normalized = "ready"
            action = "Regenerate downstream tables and manuscript text if this result is newly integrated."
        elif status in {"running", "queued"}:
            normalized = "pending"
            action = "Wait for complete 100-epoch run, then sync with the guarded protocol."
        else:
            normalized = "missing"
            action = "Investigate why this planned experiment is absent from the status table."
        items.append(
            ChecklistItem(
                "Fair Experiments",
                experiment,
                normalized,
                f"{status} | {run_dir}",
                action,
            )
        )
    return items


def build_items() -> list[ChecklistItem]:
    experiments = read_experiments()
    incomplete = [row for row in experiments if row.get("status") != "completed"]
    gate_status = "ready" if not incomplete and experiments else "pending"

    items: list[ChecklistItem] = [
        ChecklistItem(
            "Gate",
            "Fair-comparison experiment gate",
            gate_status,
            f"{len(experiments) - len(incomplete)}/{len(experiments)} completed experiments",
            "Do not rewrite final abstract/conclusion until all included fair experiments are complete and audited.",
        ),
        ChecklistItem(
            "Gate",
            "Guarded server sync protocol",
            "ready" if exists("tools/sync_cea_server_results.ps1") else "missing",
            "tools/sync_cea_server_results.ps1",
            "Use `-MinEpochs 100`; do not copy partial results manually.",
        ),
        ChecklistItem(
            "Gate",
            "Full paper audit runner",
            "ready" if exists("tools/run_paper_audits.py") else "missing",
            "tools/run_paper_audits.py",
            "Run after table, figure, speed, per-class, or manuscript updates.",
        ),
    ]
    items.extend(experiment_gate_items(experiments))

    rewrite_actions = [
        ("Tables", "Regenerate paper result tables", "paper/tables/main_comparison_for_paper.csv", "Run `python tools/export_paper_tables.py` after completed runs are synced."),
        ("Tables", "Regenerate speed table if new weights are included", "paper/tables/speed_results.csv", "Run `python tools/benchmark_speed.py --warmup 10 --samples 100 --output paper/tables/speed_results.csv` on one consistent hardware setup."),
        ("Tables", "Regenerate per-class table if final model changes", "paper/tables/per_class_results.csv", "Run `python tools/collect_per_class_metrics.py` after validation logs are available."),
        ("Tables", "Regenerate scale-group table if compared models change", "paper/tables/scale_group_results.csv", "Run `python tools/evaluate_scale_groups.py --device 0 --output paper/tables/scale_group_results.csv`."),
        ("Figures", "Regenerate accuracy-speed trade-off figure", "paper/figures/tradeoff/accuracy_speed_tradeoff.png", "Run `python tools/plot_accuracy_speed_tradeoff.py` after speed/complexity tables change."),
        ("Manuscript", "Rewrite fair-resolution comparison section", "paper/manuscript_submission_candidate.tex", "Use only audited 960-input comparison rows."),
        ("Manuscript", "Rewrite mainstream YOLO comparison section", "paper/manuscript_submission_candidate.tex", "Separate same-resolution, model-capacity, and external-version comparisons."),
        ("Manuscript", "Rewrite abstract after result sections", "paper/manuscript_submission_candidate.tex", "Fill only values that appear in refreshed paper tables."),
        ("Manuscript", "Rewrite conclusion last", "paper/manuscript_submission_candidate.tex", "Avoid universal superiority claims unless supported by fair comparisons."),
        ("Audit", "Regenerate all paper-facing audits", "paper/submission_audit_dashboard.md", "Run `python tools/run_paper_audits.py`."),
        ("Audit", "Compile PDF after manuscript changes", "paper/manuscript_submission_candidate.pdf", "Run `./tools/build_paper_pdf.ps1` and inspect the PDF."),
    ]
    for category, item, evidence, action in rewrite_actions:
        items.append(
            ChecklistItem(
                category,
                item,
                "ready" if exists(evidence) and gate_status == "ready" else ("pending" if exists(evidence) else "missing"),
                evidence,
                action,
            )
        )
    return items


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def write_report(items: list[ChecklistItem]) -> None:
    total = len(items)
    ready = sum(1 for item in items if item.status == "ready")
    pending = sum(1 for item in items if item.status == "pending")
    missing = sum(1 for item in items if item.status == "missing")

    lines = [
        "# Post-Sync Manuscript Update Checklist",
        "",
        "This checklist is generated by `tools/build_post_sync_update_checklist.py`. It turns the post-server-result manuscript update plan into actionable gates. It does not add or infer any experiment result.",
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
    for item in items:
        lines.append(
            f"| {item.category} | {item.item} | {status_symbol(item.status)} | `{item.evidence}` | {item.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the prerequisite exists and, where applicable, the fair-experiment gate is satisfied.",
            "- `PENDING` means the action is blocked by incomplete fair-comparison experiments or should wait until synced results change paper-facing evidence.",
            "- `MISSING` means an expected local artifact or script is absent.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    items = build_items()
    write_report(items)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

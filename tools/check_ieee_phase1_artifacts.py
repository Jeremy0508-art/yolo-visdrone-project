from __future__ import annotations

import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_phase1_artifact_audit.md"


@dataclass
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


REQUIRED_FILES = [
    ("Planning", "IEEE master plan", "paper/IEEE_TRANS_SUBMISSION_PLAN.md"),
    ("Planning", "Target journal analysis", "paper/ieee_target_journal_analysis.md"),
    ("Planning", "T-ITS scope-fit checklist", "paper/ieee_tits_scope_fit_checklist.md"),
    ("Planning", "T-ITS author requirements audit", "paper/ieee_tits_author_requirements_audit.md"),
    ("Planning", "Experiment gap matrix", "paper/ieee_required_experiment_gap.md"),
    ("Planning", "IEEE experiment registry", "paper/tables/ieee_experiment_registry.csv"),
    ("Planning", "IEEE experiment registry audit", "paper/ieee_experiment_registry_audit.md"),
    ("Planning", "Related-work seed matrix", "paper/ieee_related_work_matrix.csv"),
    ("Planning", "IEEE literature comparison protocol", "paper/ieee_literature_comparison_protocol.md"),
    ("Planning", "IEEE literature context table", "paper/tables/ieee_literature_context.csv"),
    ("Planning", "Dataset strategy", "paper/ieee_dataset_strategy.md"),
    ("Planning", "IEEE dataset license audit", "paper/ieee_dataset_license_audit.md"),
    ("Planning", "IEEE dataset compliance audit", "paper/ieee_dataset_compliance_audit.md"),
    ("Planning", "IEEE server resume runbook", "paper/ieee_server_resume_runbook.md"),
    ("Planning", "Method design notes", "paper/ieee_method_design_notes.md"),
    ("Planning", "IEEE method selection protocol", "paper/ieee_method_selection_protocol.md"),
    ("Planning", "IEEE result interpretation matrix", "paper/ieee_result_interpretation_matrix.md"),
    ("Planning", "IEEE result interpretation matrix audit", "paper/ieee_result_interpretation_matrix_audit.md"),
    ("Planning", "Claim boundary rules", "paper/ieee_claim_boundary.md"),
    ("Planning", "IEEE reviewer risk register", "paper/ieee_reviewer_risk_register.md"),
    ("Planning", "IEEE reviewer response plan", "paper/ieee_trans_response_plan.md"),
    ("Planning", "IEEE result integration protocol", "paper/IEEE_RESULT_INTEGRATION_PROTOCOL.md"),
    ("Planning", "IEEE scale evaluation protocol", "paper/ieee_scale_evaluation_protocol.md"),
    ("Planning", "IEEE local scale-bin AP protocol", "paper/ieee_scale_ap_protocol.md"),
    ("Planning", "IEEE scale result interpretation", "paper/ieee_scale_result_interpretation.md"),
    ("Planning", "IEEE local scale-bin AP interpretation", "paper/ieee_scale_ap_interpretation.md"),
    ("Planning", "Next actions", "paper/ieee_phase1_next_actions.md"),
    ("Planning", "Submission checklist", "paper/ieee_submission_checklist.md"),
    ("Planning", "IEEE workspace README", "paper/ieee_trans/README.md"),
    ("Planning", "IEEE manuscript blueprint", "paper/ieee_trans/manuscript_blueprint.md"),
    ("Planning", "IEEE abstract/contribution workbench", "paper/ieee_trans/abstract_contribution_workbench.md"),
    ("Planning", "IEEE title/abstract/index terms workbench", "paper/ieee_trans/title_abstract_index_terms_workbench.md"),
    ("Planning", "IEEE submission metadata workbench", "paper/ieee_trans/submission_metadata_workbench.md"),
    ("Planning", "IEEE front matter audit", "paper/ieee_front_matter_audit.md"),
    ("Planning", "IEEE related-work outline", "paper/ieee_trans/related_work_outline.md"),
    ("Planning", "IEEE section draft pack", "paper/ieee_trans/section_draft_pack.md"),
    ("Planning", "IEEE manuscript assembly checklist", "paper/ieee_trans/manuscript_assembly_checklist.md"),
    ("Planning", "IEEE manuscript assembly audit", "paper/ieee_manuscript_assembly_audit.md"),
    ("Planning", "IEEE main.tex preflight checklist", "paper/ieee_trans/main_tex_preflight.md"),
    ("Planning", "IEEE page budget plan", "paper/ieee_trans/page_budget_plan.md"),
    ("Planning", "IEEE seed bibliography", "paper/ieee_trans/references_seed.bib"),
    ("Planning", "IEEE citation plan", "paper/ieee_trans/citation_plan.md"),
    ("Planning", "IEEE evidence-to-section map", "paper/ieee_trans/evidence_to_sections.csv"),
    ("Planning", "IEEE evidence-to-section map audit", "paper/ieee_evidence_map_audit.md"),
    ("Planning", "IEEE table and figure plan", "paper/ieee_trans/table_figure_plan.md"),
    ("Planning", "IEEE figure source manifest", "paper/ieee_trans/figure_source_manifest.md"),
    ("Planning", "IEEE cover letter workbench", "paper/ieee_trans/cover_letter_workbench.md"),
    ("Planning", "IEEE generated table directory", "paper/ieee_trans/tables/README.md"),
    ("Planning", "IEEE claim audit report", "paper/ieee_claim_audit.md"),
    ("Planning", "IEEE number trace audit", "paper/ieee_number_trace_audit.md"),
    ("Planning", "IEEE server progress report", "paper/ieee_server_progress_report.md"),
    ("Planning", "IEEE server status snapshot", "paper/ieee_server_status_snapshot.md"),
    ("Planning", "IEEE server status history", "paper/tables/ieee_server_status_history.csv"),
    ("Planning", "IEEE submission dashboard", "paper/ieee_submission_dashboard.md"),
    ("Planning", "IEEE reference audit", "paper/ieee_reference_audit.md"),
    ("Planning", "IEEE reference gap report", "paper/ieee_reference_gap_report.md"),
    ("Planning", "IEEE scale output audit", "paper/ieee_scale_output_audit.md"),
    ("Planning", "IEEE table audit", "paper/ieee_table_audit.md"),
    ("Planning", "IEEE figure audit", "paper/ieee_figure_audit.md"),
    ("Planning", "Advisor transition brief", "paper/ieee_advisor_transition_brief.md"),
    ("Dataset", "UAVDT data YAML", "configs/dataset/uavdt.yaml"),
    ("Dataset", "UAVDT setup notes", "paper/datasets/uavdt_setup.md"),
    ("Dataset", "UAVDT operational checklist", "paper/datasets/uavdt_operational_checklist.md"),
    ("Dataset", "UAVDT conversion readiness audit", "paper/datasets/uavdt_conversion_readiness_audit.md"),
    ("Dataset", "UAVDT converter", "scripts/convert_uavdt_to_yolo.py"),
    ("Method", "TOFC source module", "src/models/attention/tiny_object_feature_calibration.py"),
    ("Method", "TOFC model YAML", "configs/models/yolo11n_p2_tofc.yaml"),
    ("Method", "TOFC train config", "configs/train/yolo11n_p2_tofc_960.yaml"),
    ("Analysis", "Scale target list", "paper/tables/ieee_scale_eval_targets.csv"),
    ("Execution", "Guarded server queue", "tools/run_ieee_server_queue.sh"),
    ("Execution", "IEEE claim scanner", "tools/check_ieee_claims.py"),
    ("Execution", "IEEE front matter checker", "tools/check_ieee_front_matter.py"),
    ("Execution", "IEEE number trace audit builder", "tools/build_ieee_number_trace_audit.py"),
    ("Execution", "IEEE result interpretation checker", "tools/check_ieee_result_interpretation_matrix.py"),
    ("Execution", "IEEE evidence map checker", "tools/check_ieee_evidence_map.py"),
    ("Execution", "IEEE manuscript assembly checker", "tools/check_ieee_manuscript_assembly.py"),
    ("Execution", "IEEE reference checker", "tools/check_ieee_references.py"),
    ("Execution", "IEEE dataset compliance checker", "tools/check_ieee_dataset_compliance.py"),
    ("Execution", "IEEE scale output checker", "tools/check_ieee_scale_outputs.py"),
    ("Execution", "IEEE scale interpretation builder", "tools/build_ieee_scale_interpretation.py"),
    ("Execution", "IEEE scale AP interpretation builder", "tools/build_ieee_scale_ap_interpretation.py"),
    ("Execution", "IEEE local scale-bin AP evaluator", "tools/evaluate_scale_ap.py"),
    ("Execution", "IEEE table exporter", "tools/export_ieee_tables.py"),
    ("Execution", "IEEE table checker", "tools/check_ieee_tables.py"),
    ("Execution", "IEEE figure checker", "tools/check_ieee_figures.py"),
    ("Execution", "IEEE server status checker", "tools/check_ieee_server_status.ps1"),
    ("Execution", "IEEE server sync script", "tools/sync_ieee_server_results.ps1"),
    ("Execution", "IEEE server progress reporter", "tools/build_ieee_server_progress_report.py"),
    ("Execution", "IEEE dashboard builder", "tools/build_ieee_submission_dashboard.py"),
    ("Execution", "IEEE experiment registry builder", "tools/build_ieee_experiment_registry.py"),
    ("Execution", "IEEE audit runner", "tools/run_ieee_audits.py"),
    ("Execution", "UAVDT conversion readiness checker", "tools/check_uavdt_conversion_readiness.py"),
]


RESULT_GATES = [
    (
        "Training Evidence",
        "TOFC VisDrone result",
        "runs/detect/yolo11n_p2_tofc_960_visdrone/weights/best.pt",
        "Run the guarded server queue only after GPU availability is confirmed.",
    ),
    (
        "Training Evidence",
        "UAVDT YOLO11n baseline result",
        "runs/detect/baseline_yolo11n_960_uavdt/weights/best.pt",
        "Convert and validate UAVDT before launching this run.",
    ),
    (
        "Training Evidence",
        "UAVDT YOLO11n-P2 result",
        "runs/detect/yolo11n_p2_960_uavdt/weights/best.pt",
        "Convert and validate UAVDT before launching this run.",
    ),
    (
        "Training Evidence",
        "UAVDT YOLOv8n baseline result",
        "runs/detect/baseline_yolov8n_960_uavdt/weights/best.pt",
        "Convert and validate UAVDT before launching this run.",
    ),
    (
        "Training Evidence",
        "UAVDT YOLO11s capacity reference result",
        "runs/detect/baseline_yolo11s_960_uavdt/weights/best.pt",
        "Convert and validate UAVDT before launching this run.",
    ),
    (
        "Analysis",
        "Full VisDrone scale-wise results",
        "paper/tables/ieee_scale_results_visdrone.csv",
        "Run tools/evaluate_scale_groups.py on completed VisDrone models.",
    ),
    (
        "Analysis",
        "Full VisDrone scale-wise figure",
        "paper/figures/scale_analysis/ieee_scale_recall_visdrone.png",
        "Generate after full scale-wise evaluation.",
    ),
    (
        "Analysis",
        "Full VisDrone local scale-bin AP output",
        "paper/tables/ieee_scale_ap_results_visdrone.csv",
        "Run tools/evaluate_scale_ap.py on the full VisDrone validation split.",
    ),
    (
        "Analysis",
        "Full VisDrone local scale-bin AP figure",
        "paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png",
        "Generate with tools/evaluate_scale_ap.py --plot-output.",
    ),
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def exists_check(area: str, item: str, rel_path: str, missing_action: str) -> Check:
    path = ROOT / rel_path
    return Check(
        area=area,
        item=item,
        status="ready" if path.exists() else "missing",
        evidence=rel_path,
        action="" if path.exists() else missing_action,
    )


def count_csv_rows(rel_path: str) -> int:
    path = ROOT / rel_path
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


def check_required_files() -> list[Check]:
    return [
        exists_check(area, item, path, f"Create or restore `{path}`.")
        for area, item, path in REQUIRED_FILES
    ]


def check_related_work_matrix() -> list[Check]:
    rows = count_csv_rows("paper/ieee_related_work_matrix.csv")
    status = "ready" if rows >= 10 else "pending" if rows > 0 else "missing"
    action = ""
    if rows < 20:
        action = "Expand to 20-30 recent and directly relevant papers before drafting the IEEE related-work section."
    return [
        Check(
            "Literature",
            "Related-work seed coverage",
            status,
            f"{rows} rows in paper/ieee_related_work_matrix.csv",
            action,
        )
    ]


def check_uavdt_dataset() -> list[Check]:
    processed = ROOT / "data/processed/uavdt_yolo/images/train"
    raw = ROOT / "data/raw/UAVDT"
    checks = [
        Check(
            "Dataset",
            "Raw UAVDT dataset placement",
            "ready" if raw.exists() else "pending",
            rel(raw),
            "" if raw.exists() else "Place raw UAVDT files under data/raw/UAVDT/.",
        ),
        Check(
            "Dataset",
            "Converted UAVDT YOLO train images",
            "ready" if processed.exists() else "pending",
            rel(processed),
            "" if processed.exists() else "Run scripts/convert_uavdt_to_yolo.py after raw data is available.",
        ),
    ]
    return checks


def check_tofc_model_build() -> list[Check]:
    code = (
        "from src.models.register import register_custom_modules\n"
        "register_custom_modules()\n"
        "from ultralytics.nn.tasks import DetectionModel\n"
        "for p in ['configs/models/yolo11n_p2_tofc.yaml']:\n"
        "    m=DetectionModel(p, nc=10)\n"
        "    params=sum(x.numel() for x in m.parameters())\n"
        "    print(f'{p},{len(m.model)},{params}')\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive audit path
        return [
            Check(
                "Method",
                "TOFC model construction",
                "missing",
                f"{type(exc).__name__}: {exc}",
                "Fix the custom-module registration or model YAML before launching TOFC training.",
            )
        ]

    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode == 0:
        return [
            Check(
                "Method",
                "TOFC model construction",
                "ready",
                output.splitlines()[-1] if output else "DetectionModel construction succeeded",
            )
        ]

    return [
        Check(
            "Method",
            "TOFC model construction",
            "missing",
            output or f"python exited with status {result.returncode}",
            "Fix the custom-module registration or model YAML before launching TOFC training.",
        )
    ]


def check_server_queue_guard() -> list[Check]:
    path = ROOT / "tools/run_ieee_server_queue.sh"
    if not path.exists():
        return [
            Check(
                "Execution",
                "Server queue safety guard",
                "missing",
                "tools/run_ieee_server_queue.sh",
                "Restore the guarded server queue script.",
            )
        ]
    text = path.read_text(encoding="utf-8", errors="ignore")
    has_guard = "RUN_TRAINING" in text and "Dry-run only" in text
    has_uavdt_gate = "RUN_UAVDT" in text and "data/processed/uavdt_yolo/images/train" in text
    if has_guard and has_uavdt_gate:
        return [
            Check(
                "Execution",
                "Server queue safety guard",
                "ready",
                "RUN_TRAINING dry-run guard and RUN_UAVDT dataset gate found",
            )
        ]
    return [
        Check(
            "Execution",
            "Server queue safety guard",
            "missing",
            "guard text not fully found",
            "Keep training disabled by default and gate UAVDT jobs on converted data.",
        )
    ]


def check_result_gates() -> list[Check]:
    checks: list[Check] = []
    for area, item, path, action in RESULT_GATES:
        artifact = ROOT / path
        checks.append(
            Check(
                area,
                item,
                "ready" if artifact.exists() else "pending",
                path,
                "" if artifact.exists() else action,
            )
        )
    return checks


def check_text_boundaries() -> list[Check]:
    plan = ROOT / "paper/IEEE_TRANS_SUBMISSION_PLAN.md"
    gap = ROOT / "paper/ieee_required_experiment_gap.md"
    needed = [
        (plan, "Do not claim"),
        (gap, "Claim Rules"),
    ]
    checks: list[Check] = []
    for path, phrase in needed:
        if not path.exists():
            checks.append(
                Check(
                    "Claim Boundary",
                    f"Boundary text in {rel(path)}",
                    "missing",
                    rel(path),
                    "Restore the planning document.",
                )
            )
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        checks.append(
            Check(
                "Claim Boundary",
                f"Boundary text in {rel(path)}",
                "ready" if phrase in text else "pending",
                f"searched phrase: {phrase}",
                "" if phrase in text else "Add an explicit evidence boundary before drafting IEEE claims.",
            )
        )
    return checks


def audit() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_required_files())
    checks.extend(check_related_work_matrix())
    checks.extend(check_uavdt_dataset())
    checks.extend(check_tofc_model_build())
    checks.extend(check_server_queue_guard())
    checks.extend(check_result_gates())
    checks.extend(check_text_boundaries())
    return checks


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# IEEE Phase 1 Artifact Audit",
        "",
        "This report is generated by `tools/check_ieee_phase1_artifacts.py`. It checks whether the IEEE Transactions route has the planning, dataset, method, execution, and evidence artifacts needed before manuscript claims are expanded.",
        "",
        "The audit does not launch training. `PENDING` means a planned result or dataset gate is not available yet and must not be used as paper evidence.",
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
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        evidence = check.evidence.replace("\n", "<br>")
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{evidence}` | {check.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the artifact exists locally or the structural check passed.",
            "- `PENDING` means the work is planned but cannot support IEEE manuscript claims yet.",
            "- `MISSING` means a required planning or implementation artifact should be restored or fixed before proceeding.",
            "",
            "## Current Claim Gate",
            "",
            "At this stage, the TOFC module can only be described as a candidate design whose structure builds successfully. Existing VisDrone scale-wise recall/precision and local scale-bin AP evidence can be used for completed models, but TOFC accuracy and cross-dataset generalization remain locked until full training, validation, and synchronization are complete.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {rel(REPORT_PATH)}")


if __name__ == "__main__":
    main()

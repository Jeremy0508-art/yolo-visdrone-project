from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_manuscript_assembly_audit.md"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def parse_summary_value(text: str, key: str) -> int | None:
    match = re.search(rf"- {re.escape(key)}: ([0-9]+)", text)
    if not match:
        return None
    return int(match.group(1))


def file_check(area: str, item: str, rel_path: str) -> Check:
    path = ROOT / rel_path
    return Check(
        area,
        item,
        "ready" if path.exists() else "missing",
        rel_path,
        "" if path.exists() else f"Restore or create `{rel_path}` before manuscript assembly.",
    )


def token_check(area: str, item: str, rel_path: str, token: str, action: str) -> Check:
    text = read_text(rel_path)
    return Check(
        area,
        item,
        "ready" if token in text else "missing",
        token if token in text else "not found",
        "" if token in text else action,
    )


def check_required_inputs() -> list[Check]:
    required = [
        ("Planning input", "Manuscript blueprint", "paper/ieee_trans/manuscript_blueprint.md"),
        ("Planning input", "Section draft pack", "paper/ieee_trans/section_draft_pack.md"),
        ("Planning input", "Assembly checklist", "paper/ieee_trans/manuscript_assembly_checklist.md"),
        ("Planning input", "main.tex preflight checklist", "paper/ieee_trans/main_tex_preflight.md"),
        ("Planning input", "Page budget plan", "paper/ieee_trans/page_budget_plan.md"),
        ("Planning input", "Table and figure plan", "paper/ieee_trans/table_figure_plan.md"),
        ("Planning input", "Figure source manifest", "paper/ieee_trans/figure_source_manifest.md"),
        ("Planning input", "Title/abstract/index terms workbench", "paper/ieee_trans/title_abstract_index_terms_workbench.md"),
        ("Planning input", "Submission metadata workbench", "paper/ieee_trans/submission_metadata_workbench.md"),
        ("Planning input", "Cover letter workbench", "paper/ieee_trans/cover_letter_workbench.md"),
        ("Planning input", "Seed bibliography", "paper/ieee_trans/references_seed.bib"),
        ("Audit input", "Front matter audit", "paper/ieee_front_matter_audit.md"),
        ("Audit input", "Number trace audit", "paper/ieee_number_trace_audit.md"),
        ("Audit input", "Claim audit", "paper/ieee_claim_audit.md"),
        ("Audit input", "Evidence map audit", "paper/ieee_evidence_map_audit.md"),
        ("Audit input", "Result interpretation matrix audit", "paper/ieee_result_interpretation_matrix_audit.md"),
        ("Audit input", "Dataset compliance audit", "paper/ieee_dataset_compliance_audit.md"),
    ]
    return [file_check(area, item, rel_path) for area, item, rel_path in required]


def check_generated_tables() -> list[Check]:
    tables = [
        "paper/ieee_trans/tables/visdrone_main_results.tex",
        "paper/ieee_trans/tables/speed_complexity.tex",
        "paper/ieee_trans/tables/scale_recall_precision.tex",
        "paper/ieee_trans/tables/scale_bin_ap.tex",
        "paper/ieee_trans/tables/literature_context.tex",
        "paper/ieee_trans/tables/README.md",
    ]
    return [file_check("Generated tables", Path(path).name, path) for path in tables]


def check_guardrails() -> list[Check]:
    checks = [
        token_check(
            "Guardrail",
            "Abstract/title/conclusion written last",
            "paper/ieee_trans/manuscript_assembly_checklist.md",
            "The abstract, title, and conclusion must be written last",
            "Keep the assembly checklist explicit about high-risk sections.",
        ),
        token_check(
            "Guardrail",
            "TOFC remains locked",
            "paper/ieee_trans/manuscript_assembly_checklist.md",
            "TOFC Description | `section_draft_pack.md` | Locked",
            "Keep TOFC locked until complete training evidence exists.",
        ),
        token_check(
            "Guardrail",
            "UAVDT results remain locked",
            "paper/ieee_trans/manuscript_assembly_checklist.md",
            "UAVDT Results | none | Locked",
            "Keep UAVDT result claims locked until conversion and runs are complete.",
        ),
        token_check(
            "Guardrail",
            "YOLO11s boundary retained",
            "paper/ieee_trans/manuscript_assembly_checklist.md",
            "Both routes require honest comparison against YOLO11s-960",
            "Keep the larger-model accuracy boundary in the assembly checklist.",
        ),
        token_check(
            "Guardrail",
            "main.tex preflight says not to create final source yet",
            "paper/ieee_trans/main_tex_preflight.md",
            "Do not create `main.tex` yet",
            "Keep the final-source creation gate explicit.",
        ),
        token_check(
            "Guardrail",
            "Claim audit remains pending until final-facing files exist",
            "paper/ieee_trans/main_tex_preflight.md",
            "Claim audit ready | Pending final-facing files",
            "Keep claim audit expectations tied to final-facing files.",
        ),
    ]
    return checks


def check_final_files_guard() -> list[Check]:
    phase_text = read_text("paper/ieee_phase1_artifact_audit.md")
    pending = parse_summary_value(phase_text, "Pending")
    creation_locked = pending is None or pending > 0
    final_files = [
        "paper/ieee_trans/main.tex",
        "paper/ieee_trans/references.bib",
        "paper/ieee_trans/cover_letter_draft.md",
        "paper/ieee_trans/abstract.md",
    ]
    checks: list[Check] = [
        Check(
            "Final-source gate",
            "Final manuscript creation is still gated",
            "ready" if creation_locked else "pending",
            f"Phase 1 pending checks: {pending if pending is not None else 'unknown'}",
            "" if creation_locked else "If all gates are complete, create final files only through the preflight process.",
        )
    ]
    for rel_path in final_files:
        exists = (ROOT / rel_path).exists()
        if creation_locked:
            checks.append(
                Check(
                    "Final-source gate",
                    f"`{rel_path}` absent while gates are pending",
                    "ready" if not exists else "missing",
                    "absent" if not exists else "present",
                    "" if not exists else "Remove or clearly downgrade this final-facing file until preflight gates pass.",
                )
            )
        else:
            checks.append(
                Check(
                    "Final-source gate",
                    f"`{rel_path}` after gate completion",
                    "ready" if exists else "pending",
                    "present" if exists else "absent",
                    "" if exists else "Create this final-facing file through the IEEE preflight workflow.",
                )
            )
    return checks


def check_manual_pending_gates() -> list[Check]:
    gate_items = [
        (
            "Target journal final confirmation",
            "paper/ieee_trans/main_tex_preflight.md",
            "Exact IEEE Transactions target selected | Pending",
            "Advisor confirms T-ITS, TGRS, or another exact journal.",
        ),
        (
            "Final method route selected",
            "paper/ieee_trans/main_tex_preflight.md",
            "Final method route selected | Pending",
            "Select TOFC or fallback route only after real result evidence arrives.",
        ),
        (
            "Cross-dataset plan resolved",
            "paper/ieee_trans/main_tex_preflight.md",
            "Cross-dataset plan resolved | Pending",
            "Resolve after UAVDT conversion and runs or explicitly downgrade scope.",
        ),
        (
            "Reference metadata verified",
            "paper/ieee_trans/main_tex_preflight.md",
            "Reference metadata verified | Pending",
            "Verify final BibTeX entries against publisher metadata before references.bib.",
        ),
        (
            "Dataset/code release boundary final confirmation",
            "paper/ieee_trans/manuscript_assembly_checklist.md",
            "Dataset/code release boundary verified | Pending final human confirmation",
            "Confirm release policy with advisor/institution before final package.",
        ),
    ]
    checks: list[Check] = []
    for item, rel_path, token, action in gate_items:
        found = token in read_text(rel_path)
        checks.append(
            Check(
                "Manual pending gate",
                item,
                "pending" if found else "missing",
                token if found else "not found",
                action,
            )
        )
    return checks


def audit() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_required_inputs())
    checks.extend(check_generated_tables())
    checks.extend(check_guardrails())
    checks.extend(check_final_files_guard())
    checks.extend(check_manual_pending_gates())
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE Manuscript Assembly Audit",
        "",
        "This report is generated by `tools/check_ieee_manuscript_assembly.py`. It checks whether the IEEE manuscript workspace has the planning inputs, generated table drafts, guardrails, and final-source locks needed before a final-facing `main.tex` is created.",
        "",
        "The audit does not compile LaTeX and does not create final manuscript files. `PENDING` marks deliberate manual or evidence gates.",
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
            "- `READY` means the assembly input, guardrail, generated table, or final-source lock is in the expected state.",
            "- `PENDING` means the item deliberately waits for advisor confirmation, final evidence, or manuscript creation after the gate opens.",
            "- `MISSING` means the workspace should be fixed before final IEEE manuscript assembly.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

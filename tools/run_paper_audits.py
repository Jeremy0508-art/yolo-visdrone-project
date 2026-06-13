from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


AUDIT_STEPS = [
    ("Journal manuscript gap audit", "tools/check_journal_manuscript_gaps.py"),
    ("LaTeX reference audit", "tools/check_tex_references.py"),
    ("Reference verification audit", "tools/check_reference_verification_matrix.py"),
    ("LaTeX figure audit", "tools/check_tex_figures.py"),
    ("LaTeX cross-reference audit", "tools/check_tex_cross_references.py"),
    ("LaTeX table-source audit", "tools/check_tex_table_sources.py"),
    ("Reproducibility command audit", "tools/check_repro_commands.py"),
    ("Configuration inventory audit", "tools/check_config_inventory.py"),
    ("Evidence audit", "tools/build_evidence_audit.py"),
    ("Manuscript number trace audit", "tools/check_manuscript_number_trace.py"),
    ("Manuscript length audit", "tools/check_manuscript_length.py"),
    ("Section evidence map audit", "tools/check_section_evidence_map.py"),
    ("Submission risk register audit", "tools/check_submission_risk_register.py"),
    ("Text hygiene audit", "tools/check_text_hygiene.py"),
    ("Project README presentation audit", "tools/check_project_readme_presentation.py"),
    ("PDF text readability audit", "tools/check_pdf_text_readability.py"),
    ("PDF layout health audit", "tools/check_pdf_layout_health.py"),
    ("Advisor progress brief", "tools/build_advisor_progress_brief.py"),
    ("Advisor progress brief audit", "tools/check_advisor_progress_brief.py"),
    ("CEA submission package checklist", "tools/build_cea_submission_package_checklist.py"),
    ("CEA server progress report", "tools/build_cea_server_progress_report.py"),
    ("Post-sync manuscript update checklist", "tools/build_post_sync_update_checklist.py"),
    ("Submission material manifest", "tools/build_submission_material_manifest.py"),
    ("Paper consistency audit", "tools/check_paper_consistency.py"),
    ("Claim boundary audit", "tools/check_claim_boundaries.py"),
    ("Submission readiness audit", "tools/audit_submission_readiness.py"),
    ("Submission audit dashboard", "tools/build_submission_audit_dashboard.py"),
]


def run_step(name: str, script: str) -> None:
    print(f"[audit] {name}: {script}", flush=True)
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def main() -> None:
    for name, script in AUDIT_STEPS:
        run_step(name, script)
    print("[audit] complete", flush=True)


if __name__ == "__main__":
    main()

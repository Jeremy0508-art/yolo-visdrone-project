from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AuditStep:
    name: str
    command: list[str]


STEPS = [
    AuditStep("build experiment registry", [sys.executable, "tools/build_ieee_experiment_registry.py"]),
    AuditStep("check scale outputs", [sys.executable, "tools/check_ieee_scale_outputs.py"]),
    AuditStep("build scale interpretation", [sys.executable, "tools/build_ieee_scale_interpretation.py"]),
    AuditStep("build scale AP interpretation", [sys.executable, "tools/build_ieee_scale_ap_interpretation.py"]),
    AuditStep("check UAVDT conversion readiness", [sys.executable, "tools/check_uavdt_conversion_readiness.py"]),
    AuditStep("export UAVDT results", [sys.executable, "tools/export_ieee_uavdt_results.py"]),
    AuditStep("export IEEE tables", [sys.executable, "tools/export_ieee_tables.py"]),
    AuditStep("check IEEE tables", [sys.executable, "tools/check_ieee_tables.py"]),
    AuditStep("check IEEE figures", [sys.executable, "tools/check_ieee_figures.py"]),
    AuditStep("check IEEE claims", [sys.executable, "tools/check_ieee_claims.py"]),
    AuditStep("check IEEE front matter", [sys.executable, "tools/check_ieee_front_matter.py"]),
    AuditStep("build number trace audit", [sys.executable, "tools/build_ieee_number_trace_audit.py"]),
    AuditStep("check main draft numbers", [sys.executable, "tools/check_ieee_main_draft_numbers.py"]),
    AuditStep("check result interpretation matrix", [sys.executable, "tools/check_ieee_result_interpretation_matrix.py"]),
    AuditStep("check evidence-to-section map", [sys.executable, "tools/check_ieee_evidence_map.py"]),
    AuditStep("check manuscript assembly", [sys.executable, "tools/check_ieee_manuscript_assembly.py"]),
    AuditStep("check IEEE references", [sys.executable, "tools/check_ieee_references.py"]),
    AuditStep("check reference metadata readiness", [sys.executable, "tools/check_ieee_reference_metadata_readiness.py"]),
    AuditStep("check dataset compliance", [sys.executable, "tools/check_ieee_dataset_compliance.py"]),
    AuditStep("check IEEE draft shareability", [sys.executable, "tools/check_ieee_draft_shareability.py"]),
    AuditStep("build server progress report", [sys.executable, "tools/build_ieee_server_progress_report.py"]),
    AuditStep("check ScaleGate result gate", [sys.executable, "tools/check_ieee_scalegate_result_gate.py"]),
    AuditStep("check ScaleGate method decision", [sys.executable, "tools/check_ieee_scalegate_method_decision.py"]),
    AuditStep("check CSGate result gate", [sys.executable, "tools/check_ieee_csgate_result_gate.py"]),
    AuditStep("check CSGate method decision", [sys.executable, "tools/check_ieee_csgate_method_decision.py"]),
    AuditStep("build ScaleGate post-result runbook", [sys.executable, "tools/build_ieee_scalegate_post_result_runbook.py"]),
    AuditStep("check ScaleGate post-result runbook", [sys.executable, "tools/check_ieee_scalegate_post_result_runbook.py"]),
    AuditStep("check Phase 1 artifacts", [sys.executable, "tools/check_ieee_phase1_artifacts.py"]),
    AuditStep("check non-result closure", [sys.executable, "tools/check_ieee_non_result_closure.py"]),
    AuditStep("check IEEE goal readiness", [sys.executable, "tools/check_ieee_goal_readiness.py"]),
    AuditStep("refresh Phase 1 artifacts", [sys.executable, "tools/check_ieee_phase1_artifacts.py"]),
    AuditStep("refresh non-result closure", [sys.executable, "tools/check_ieee_non_result_closure.py"]),
    AuditStep("refresh IEEE goal readiness", [sys.executable, "tools/check_ieee_goal_readiness.py"]),
    AuditStep("build submission dashboard", [sys.executable, "tools/build_ieee_submission_dashboard.py"]),
]


def run_step(step: AuditStep) -> None:
    print(f"[IEEE audit] {step.name}")
    subprocess.run(step.command, cwd=ROOT, check=True)


def main() -> None:
    for step in STEPS:
        run_step(step)
    print("[IEEE audit] done")


if __name__ == "__main__":
    main()

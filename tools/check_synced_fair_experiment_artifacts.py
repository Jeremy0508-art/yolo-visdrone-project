from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "paper/tables/cea_experiment_status.csv"
REPORT_PATH = ROOT / "paper/synced_fair_experiment_artifacts_audit.md"
MIN_EPOCHS = 100


@dataclass
class ArtifactCheck:
    experiment: str
    item: str
    status: str
    evidence: str
    action: str = ""


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def count_result_epochs(rel_path: str) -> int:
    path = ROOT / rel_path
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return len(rows)


def read_experiments() -> list[dict[str, str]]:
    if not STATUS_PATH.exists():
        return []
    with STATUS_PATH.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def add_completed_artifact_checks(checks: list[ArtifactCheck], row: dict[str, str]) -> None:
    experiment = row.get("experiment", "unknown")
    run_dir = row.get("run_dir", "")
    server_log = row.get("server_log", "")
    result_path = f"{run_dir}/results.csv"
    args_path = f"{run_dir}/args.yaml"
    best_path = f"{run_dir}/weights/best.pt"
    last_path = f"{run_dir}/weights/last.pt"

    for item, path, action in [
        ("Run directory", run_dir, "Sync the completed run directory from the server."),
        ("results.csv", result_path, "Sync results.csv for metric extraction."),
        ("args.yaml", args_path, "Sync args.yaml for reproducibility evidence."),
        ("best.pt", best_path, "Sync best.pt for validation, speed, and test-dev export."),
        ("last.pt", last_path, "Sync last.pt for resumability evidence."),
    ]:
        checks.append(
            ArtifactCheck(
                experiment,
                item,
                "ready" if exists(path) else "missing",
                path,
                "" if exists(path) else action,
            )
        )

    epochs = count_result_epochs(result_path)
    checks.append(
        ArtifactCheck(
            experiment,
            "Minimum result epochs",
            "ready" if epochs >= MIN_EPOCHS else "missing",
            f"{epochs}/{MIN_EPOCHS} epochs in {result_path}",
            "" if epochs >= MIN_EPOCHS else "Do not integrate this run into paper tables until it has complete 100-epoch evidence.",
        )
    )

    log_ready = bool(server_log) and exists(server_log)
    checks.append(
        ArtifactCheck(
            experiment,
            "Training/server log",
            "ready" if log_ready else "missing",
            server_log or "not recorded",
            "" if log_ready else "Sync or record the training/server log used for this run.",
        )
    )


def audit() -> list[ArtifactCheck]:
    rows = read_experiments()
    if not rows:
        return [
            ArtifactCheck(
                "fair-experiment-matrix",
                "Experiment status table",
                "missing",
                str(STATUS_PATH.relative_to(ROOT)),
                "Restore paper/tables/cea_experiment_status.csv.",
            )
        ]

    checks: list[ArtifactCheck] = [
        ArtifactCheck(
            "fair-experiment-matrix",
            "Experiment status table",
            "ready",
            f"{STATUS_PATH.relative_to(ROOT)} ({len(rows)} rows)",
        )
    ]

    for row in rows:
        experiment = row.get("experiment", "unknown")
        status = row.get("status", "")
        run_dir = row.get("run_dir", "")
        if status == "completed":
            checks.append(
                ArtifactCheck(
                    experiment,
                    "Completion status",
                    "ready",
                    f"completed | {run_dir}",
                )
            )
            add_completed_artifact_checks(checks, row)
        elif status in {"running", "queued"}:
            checks.append(
                ArtifactCheck(
                    experiment,
                    "Completion status",
                    "pending",
                    f"{status} | {run_dir}",
                    "Wait for complete 100-epoch run, then sync with tools/sync_cea_server_results.ps1 -MinEpochs 100.",
                )
            )
        else:
            checks.append(
                ArtifactCheck(
                    experiment,
                    "Completion status",
                    "missing",
                    f"{status or 'blank'} | {run_dir}",
                    "Investigate the planned fair-experiment status row.",
                )
            )

    return checks


def write_report(checks: list[ArtifactCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# Synced Fair-Experiment Artifacts Audit",
        "",
        "This report is generated by `tools/check_synced_fair_experiment_artifacts.py`. It checks whether completed fair-comparison experiments have the local artifacts required before their results may enter paper tables or manuscript claims.",
        "",
        "Pending/running/queued experiments are treated as progress gates, not missing local evidence. Completed experiments must have a run directory, `results.csv`, `args.yaml`, weights, enough epochs, and a training/server log.",
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
        "| Experiment | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.experiment} | {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the artifact exists locally or the status table is available.",
            "- `PENDING` means the experiment is not complete and must not be used as paper evidence.",
            "- `MISSING` means a completed experiment lacks required local evidence and should not be integrated until fixed.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

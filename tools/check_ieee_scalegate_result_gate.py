from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_scalegate_result_gate_audit.md"
SERVER_HISTORY_PATH = ROOT / "paper/tables/ieee_server_status_history.csv"
MIN_EPOCHS = 100

SCALEGATE_MODEL = "YOLO11n-P2-ScaleGate-960"
VISDRONE_RUN = ROOT / "runs/detect/yolo11n_p2_scalegate_960_visdrone"
UAVDT_RUN = ROOT / "runs/detect/yolo11n_p2_scalegate_960_uavdt"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def count_epochs(run_dir: Path) -> int:
    results = run_dir / "results.csv"
    if not results.exists():
        return 0
    with results.open(encoding="utf-8-sig", errors="ignore") as f:
        lines = [line for line in f if line.strip()]
    if not lines:
        return 0
    return max(len(lines) - 1, 0)


def latest_server_run_status(run_name: str) -> dict[str, str] | None:
    if not SERVER_HISTORY_PATH.exists():
        return None
    latest: dict[str, str] | None = None
    with SERVER_HISTORY_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("run") == run_name:
                latest = row
    return latest


def server_progress_suffix(run_name: str) -> str:
    row = latest_server_run_status(run_name)
    if not row:
        return ""
    bits = [
        f"server={row.get('status', '')}",
        f"{row.get('epochs', '0')}/{MIN_EPOCHS}",
        f"timestamp={row.get('timestamp', '')}",
    ]
    last_map50 = row.get("last_map50", "")
    last_map5095 = row.get("last_map50_95", "")
    if last_map50 or last_map5095:
        bits.append(f"progress mAP50={last_map50}")
        bits.append(f"progress mAP50-95={last_map5095}")
    return "; " + "; ".join(bits)


def run_complete(run_dir: Path) -> bool:
    return (
        count_epochs(run_dir) >= MIN_EPOCHS
        and (run_dir / "args.yaml").exists()
        and (run_dir / "weights/best.pt").exists()
    )


def check_run_artifacts(label: str, run_dir: Path) -> Check:
    results = run_dir / "results.csv"
    args = run_dir / "args.yaml"
    weight = run_dir / "weights/best.pt"
    epochs = count_epochs(run_dir)
    missing = [rel(path) for path in [results, args, weight] if not path.exists()]

    if run_complete(run_dir):
        return Check(
            "Core run",
            f"{label} local complete run",
            "ready",
            f"{rel(run_dir)}; epochs={epochs}; args.yaml and weights/best.pt present",
        )

    if results.exists() and (args.exists() or weight.exists()) and missing:
        return Check(
            "Core run",
            f"{label} local complete run",
            "missing",
            f"{rel(run_dir)}; epochs={epochs}; missing: {', '.join(missing)}",
            "Do not use this run as paper evidence; restore artifacts only from a completed guarded sync.",
        )

    return Check(
        "Core run",
        f"{label} local complete run",
        "pending",
        f"{rel(run_dir)}; epochs={epochs}; required={MIN_EPOCHS}{server_progress_suffix(run_dir.name)}",
        "Wait for the server run to finish and sync only through tools/sync_ieee_server_results.ps1.",
    )


def find_rows(path: Path, column: str, value: str) -> list[dict[str, str]]:
    rows = read_csv_rows(path)
    return [row for row in rows if row.get(column, "") == value]


def check_absent_until_complete(
    item: str,
    path: Path,
    column: str,
    complete: bool,
    required_if_complete: bool = True,
) -> Check:
    rows = find_rows(path, column, SCALEGATE_MODEL)
    if complete:
        if rows or not required_if_complete:
            return Check("Paper table gate", item, "ready", f"{rel(path)}; rows={len(rows)}")
        return Check(
            "Paper table gate",
            item,
            "pending",
            f"{rel(path)}; ScaleGate row not exported yet",
            "Refresh exporters and audits after the completed ScaleGate run is synced.",
        )

    if rows:
        return Check(
            "Paper table gate",
            item,
            "missing",
            f"{rel(path)}; premature ScaleGate rows={len(rows)}",
            "Remove the ScaleGate row until both run completion and the post-result protocol allow it.",
        )
    return Check(
        "Paper table gate",
        item,
        "ready",
        f"{rel(path)}; no premature ScaleGate row",
    )


def check_uavdt_status_table(complete: bool) -> Check:
    path = ROOT / "paper/tables/ieee_uavdt_results_status.csv"
    rows = find_rows(path, "model", SCALEGATE_MODEL)
    if not rows:
        return Check(
            "Paper table gate",
            "UAVDT status table has ScaleGate tracking row",
            "missing",
            rel(path),
            "Keep a status row so the missing/complete state is auditable.",
        )
    row = rows[0]
    status = row.get("status", "")
    paper_ready = row.get("paper_ready", "")
    epochs = row.get("epochs", "")
    if complete:
        ok = status == "complete" and paper_ready == "yes" and int(float(epochs or 0)) >= MIN_EPOCHS
        return Check(
            "Paper table gate",
            "UAVDT status table complete state",
            "ready" if ok else "pending",
            f"{rel(path)}; status={status}; epochs={epochs}; paper_ready={paper_ready}",
            "" if ok else "Run export_ieee_uavdt_results.py after the completed UAVDT ScaleGate run is synced.",
        )

    ok = status != "complete" and paper_ready != "yes"
    return Check(
        "Paper table gate",
        "UAVDT status table remains locked before completion",
        "ready" if ok else "missing",
        f"{rel(path)}; status={status}; epochs={epochs}; paper_ready={paper_ready}",
        "" if ok else "Do not mark the UAVDT ScaleGate row paper-ready before the 100-epoch completion gate.",
    )


def check_scale_target(complete: bool) -> Check:
    path = ROOT / "paper/tables/ieee_scale_eval_targets.csv"
    rows = find_rows(path, "model", SCALEGATE_MODEL)
    if not rows:
        return Check(
            "Diagnostic gate",
            "ScaleGate scale-diagnostic target row",
            "missing",
            rel(path),
            "Keep the disabled ScaleGate target row so the post-result protocol is explicit.",
        )
    enabled = rows[0].get("enabled", "").strip().lower()
    if complete:
        ok = enabled == "true"
        return Check(
            "Diagnostic gate",
            "ScaleGate scale-diagnostic target enabled after complete run",
            "ready" if ok else "pending",
            f"{rel(path)}; enabled={enabled}",
            "" if ok else "Enable this row only after the complete VisDrone ScaleGate weights are synced.",
        )

    ok = enabled != "true"
    return Check(
        "Diagnostic gate",
        "ScaleGate scale-diagnostic target disabled while run is incomplete",
        "ready" if ok else "missing",
        f"{rel(path)}; enabled={enabled}",
        "" if ok else "Disable this row until the complete VisDrone ScaleGate weights are synced.",
    )


def check_diagnostic_rows(item: str, path: Path, complete: bool, expected_rows: int = 3) -> Check:
    rows = find_rows(path, "model", SCALEGATE_MODEL)
    if complete:
        ok = len(rows) >= expected_rows
        return Check(
            "Diagnostic gate",
            item,
            "ready" if ok else "pending",
            f"{rel(path)}; ScaleGate rows={len(rows)}",
            "" if ok else "Re-run the diagnostic script after enabling the complete ScaleGate target row.",
        )
    if rows:
        return Check(
            "Diagnostic gate",
            item,
            "missing",
            f"{rel(path)}; premature ScaleGate rows={len(rows)}",
            "Remove or regenerate diagnostics so incomplete ScaleGate results are not used.",
        )
    return Check("Diagnostic gate", item, "ready", f"{rel(path)}; no premature ScaleGate rows")


def check_complexity_table(complete: bool) -> Check:
    path = ROOT / "paper/tables/model_complexity.csv"
    rows = find_rows(path, "model", SCALEGATE_MODEL)
    if not rows:
        return Check(
            "Efficiency gate",
            "ScaleGate complexity row exists",
            "pending" if complete else "ready",
            f"{rel(path)}; no ScaleGate row",
            "Add or refresh complexity after the complete run is synced." if complete else "",
        )
    status = rows[0].get("status", "")
    if complete:
        ok = status == "completed" and rows[0].get("parameters") and rows[0].get("gflops")
        return Check(
            "Efficiency gate",
            "ScaleGate complexity row completed after complete run",
            "ready" if ok else "pending",
            f"{rel(path)}; status={status}; params={rows[0].get('parameters', '')}; gflops={rows[0].get('gflops', '')}",
            "" if ok else "Refresh model complexity after complete ScaleGate weights are available.",
        )
    ok = status != "completed"
    return Check(
        "Efficiency gate",
        "ScaleGate complexity row not marked completed before complete run",
        "ready" if ok else "missing",
        f"{rel(path)}; status={status}",
        "" if ok else "Do not mark ScaleGate complexity completed before the run has passed the completion gate.",
    )


def check_speed_table(complete: bool) -> Check:
    return check_absent_until_complete(
        "ScaleGate speed row",
        ROOT / "paper/tables/speed_results.csv",
        "model",
        complete,
        required_if_complete=True,
    )


def check_main_draft_metric_lock(complete_visdrone: bool, complete_uavdt: bool) -> Check:
    path = ROOT / "paper/ieee_trans/main_draft.tex"
    if not path.exists():
        return Check("Manuscript lock", "main_draft.tex exists for lock scan", "pending", rel(path))
    text = path.read_text(encoding="utf-8", errors="ignore")
    gate_open = complete_visdrone and complete_uavdt
    if gate_open:
        return Check(
            "Manuscript lock",
            "ScaleGate metric wording allowed only after both runs complete",
            "ready",
            "both local completion gates passed",
        )

    metric_terms = r"(mAP|AP50|AP|recall|precision|FPS|GFLOPs|latency|accuracy)"
    patterns = [
        re.compile(rf"ScaleGate[^\n]{{0,120}}{metric_terms}[^\n]{{0,80}}\b0\.\d+", re.I),
        re.compile(rf"\b0\.\d+[^\n]{{0,80}}{metric_terms}[^\n]{{0,120}}ScaleGate", re.I),
        re.compile(r"ScaleAwareP2Gate[^\n]{0,120}\b(improve|gain|outperform|surpass|boost)", re.I),
    ]
    hits: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if r"\includegraphics" in line:
            continue
        for pattern in patterns:
            if pattern.search(line):
                hits.append(f"line {number}: {line.strip()[:140]}")
                break
    if hits:
        return Check(
            "Manuscript lock",
            "No ScaleGate metric or performance claim before gate opens",
            "missing",
            "; ".join(hits[:5]),
            "Remove ScaleGate performance wording until completed VisDrone and UAVDT evidence is audited.",
        )
    return Check(
        "Manuscript lock",
        "No ScaleGate metric or performance claim before gate opens",
        "ready",
        "no premature ScaleGate metric/performance wording found",
    )


def audit() -> list[Check]:
    complete_visdrone = run_complete(VISDRONE_RUN)
    complete_uavdt = run_complete(UAVDT_RUN)
    checks = [
        check_run_artifacts("VisDrone", VISDRONE_RUN),
        check_run_artifacts("UAVDT", UAVDT_RUN),
        check_absent_until_complete(
            "VisDrone main comparison ScaleGate row",
            ROOT / "paper/tables/main_comparison_for_paper.csv",
            "model",
            complete_visdrone,
            required_if_complete=True,
        ),
        check_uavdt_status_table(complete_uavdt),
        check_absent_until_complete(
            "UAVDT paper table ScaleGate row",
            ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv",
            "model",
            complete_uavdt,
            required_if_complete=True,
        ),
        check_complexity_table(complete_visdrone),
        check_speed_table(complete_visdrone),
        check_scale_target(complete_visdrone),
        check_diagnostic_rows(
            "Scale-wise recall/precision rows for ScaleGate",
            ROOT / "paper/tables/ieee_scale_results_visdrone.csv",
            complete_visdrone,
        ),
        check_diagnostic_rows(
            "Local scale-bin AP rows for ScaleGate",
            ROOT / "paper/tables/ieee_scale_ap_results_visdrone.csv",
            complete_visdrone,
        ),
        check_main_draft_metric_lock(complete_visdrone, complete_uavdt),
    ]
    return checks


def gate_status(checks: list[Check]) -> str:
    core = [c for c in checks if c.area == "Core run"]
    if len(core) == 2 and all(c.status == "ready" for c in core):
        return "OPEN_FOR_POST_RESULT_INTEGRATION"
    return "LOCKED_WAITING_FOR_COMPLETE_SCALEGATE_RUNS"


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    complete_runs = sum(1 for run in [VISDRONE_RUN, UAVDT_RUN] if run_complete(run))
    status = gate_status(checks)

    lines = [
        "# IEEE ScaleGate Result Gate Audit",
        "",
        "This report is generated by `tools/check_ieee_scalegate_result_gate.py`. It protects the IEEE manuscript from using partial ScaleAwareP2Gate evidence.",
        "",
        "The audit is intentionally non-blocking while experiments are running: `PENDING` means the result is not available yet and must not be used as a paper claim. `MISSING` means a premature or inconsistent artifact should be fixed.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        f"- Gate status: {status}",
        f"- Complete ScaleGate runs: {complete_runs}/2",
        f"- Required epochs per run: {MIN_EPOCHS}",
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
            "- The ScaleGate method description may remain in planning/draft files and manuscript discussion only as completed mixed/negative evidence unless the separate method-decision audit accepts a route.",
            "- ScaleGate metric wording is allowed only with exact audited values from the generated tables; it is not sufficient for a main-method claim by itself.",
            "- If any row is `MISSING`, fix the inconsistent artifact before sharing the IEEE draft.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {rel(REPORT_PATH)}")


if __name__ == "__main__":
    main()

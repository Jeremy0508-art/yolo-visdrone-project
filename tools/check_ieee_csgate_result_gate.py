from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_csgate_result_gate_audit.md"
SERVER_HISTORY_PATH = ROOT / "paper/tables/ieee_server_status_history.csv"
MIN_EPOCHS = 100

CSGATE_MODEL = "YOLO11n-P2-CSGate-960"
VISDRONE_RUN = ROOT / "runs/detect/yolo11n_p2_csgate_960_visdrone"
UAVDT_RUN = ROOT / "runs/detect/yolo11n_p2_csgate_960_uavdt"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def status_label(status: str) -> str:
    return {"ready": "READY", "pending": "PENDING", "missing": "MISSING"}[status]


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
    return max(len(lines) - 1, 0)


def latest_server_run_status(run_name: str) -> dict[str, str] | None:
    latest: dict[str, str] | None = None
    if not SERVER_HISTORY_PATH.exists():
        return None
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
    if row.get("last_map50") or row.get("last_map50_95"):
        bits.append(f"progress mAP50={row.get('last_map50', '')}")
        bits.append(f"progress mAP50-95={row.get('last_map50_95', '')}")
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
        "Wait for the server run to finish and sync only through tools/intake_ieee_csgate_results.ps1.",
    )


def find_rows(path: Path, column: str, value: str) -> list[dict[str, str]]:
    return [row for row in read_csv_rows(path) if row.get(column, "") == value]


def check_table_row(item: str, path: Path, column: str, complete: bool, required_if_complete: bool = True) -> Check:
    rows = find_rows(path, column, CSGATE_MODEL)
    if complete:
        if rows or not required_if_complete:
            return Check("Paper table gate", item, "ready", f"{rel(path)}; rows={len(rows)}")
        return Check(
            "Paper table gate",
            item,
            "pending",
            f"{rel(path)}; CSGate row not exported yet",
            "Refresh exporters and audits after the completed CSGate run is synced.",
        )
    if rows:
        return Check(
            "Paper table gate",
            item,
            "missing",
            f"{rel(path)}; premature CSGate rows={len(rows)}",
            "Remove the CSGate row until both run completion and the post-result protocol allow it.",
        )
    return Check("Paper table gate", item, "ready", f"{rel(path)}; no premature CSGate row")


def check_uavdt_status_table(complete: bool) -> Check:
    path = ROOT / "paper/tables/ieee_uavdt_results_status.csv"
    rows = find_rows(path, "model", CSGATE_MODEL)
    if not rows:
        return Check(
            "Paper table gate",
            "UAVDT status table has CSGate tracking row",
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
            "" if ok else "Run export_ieee_uavdt_results.py after the completed UAVDT CSGate run is synced.",
        )
    ok = status != "complete" and paper_ready != "yes"
    return Check(
        "Paper table gate",
        "UAVDT status table remains locked before completion",
        "ready" if ok else "missing",
        f"{rel(path)}; status={status}; epochs={epochs}; paper_ready={paper_ready}",
        "" if ok else "Do not mark the UAVDT CSGate row paper-ready before the 100-epoch completion gate.",
    )


def check_scale_target(complete: bool) -> Check:
    path = ROOT / "paper/tables/ieee_scale_eval_targets.csv"
    rows = find_rows(path, "model", CSGATE_MODEL)
    if not rows:
        return Check(
            "Diagnostic gate",
            "CSGate scale-diagnostic target row",
            "missing",
            rel(path),
            "Keep the disabled CSGate target row so the post-result protocol is explicit.",
        )
    enabled = rows[0].get("enabled", "").strip().lower()
    if complete:
        ok = enabled == "true"
        return Check(
            "Diagnostic gate",
            "CSGate scale-diagnostic target enabled after complete run",
            "ready" if ok else "pending",
            f"{rel(path)}; enabled={enabled}",
            "" if ok else "Enable this row only after the complete VisDrone CSGate weights are synced.",
        )
    ok = enabled != "true"
    return Check(
        "Diagnostic gate",
        "CSGate scale-diagnostic target disabled while run is incomplete",
        "ready" if ok else "missing",
        f"{rel(path)}; enabled={enabled}",
        "" if ok else "Disable this row until the complete VisDrone CSGate weights are synced.",
    )


def check_diagnostic_rows(item: str, path: Path, complete: bool, expected_rows: int = 3) -> Check:
    rows = find_rows(path, "model", CSGATE_MODEL)
    if complete:
        ok = len(rows) >= expected_rows
        return Check(
            "Diagnostic gate",
            item,
            "ready" if ok else "pending",
            f"{rel(path)}; CSGate rows={len(rows)}",
            "" if ok else "Re-run the diagnostic script after enabling the complete CSGate target row.",
        )
    if rows:
        return Check(
            "Diagnostic gate",
            item,
            "missing",
            f"{rel(path)}; premature CSGate rows={len(rows)}",
            "Remove or regenerate diagnostics so incomplete CSGate results are not used.",
        )
    return Check("Diagnostic gate", item, "ready", f"{rel(path)}; no premature CSGate rows")


def check_complexity_table(complete: bool) -> Check:
    path = ROOT / "paper/tables/model_complexity.csv"
    rows = find_rows(path, "model", CSGATE_MODEL)
    if not rows:
        return Check(
            "Efficiency gate",
            "CSGate complexity row exists",
            "pending" if complete else "ready",
            f"{rel(path)}; no CSGate row",
            "Add or refresh complexity after the complete run is synced." if complete else "",
        )
    status = rows[0].get("status", "")
    if complete:
        ok = status == "completed" and rows[0].get("parameters") and rows[0].get("gflops")
        return Check(
            "Efficiency gate",
            "CSGate complexity row completed after complete run",
            "ready" if ok else "pending",
            f"{rel(path)}; status={status}; params={rows[0].get('parameters', '')}; gflops={rows[0].get('gflops', '')}",
            "" if ok else "Refresh model complexity after complete CSGate weights are available.",
        )
    ok = status != "completed"
    return Check(
        "Efficiency gate",
        "CSGate complexity row not marked completed before complete run",
        "ready" if ok else "missing",
        f"{rel(path)}; status={status}",
        "" if ok else "Do not mark CSGate complexity completed before the run has passed the completion gate.",
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
            "CSGate metric wording allowed only after both runs complete",
            "ready",
            "both local completion gates passed",
        )
    metric_terms = r"(mAP|AP50|AP|recall|precision|FPS|GFLOPs|latency|accuracy)"
    patterns = [
        re.compile(rf"CSGate[^\n]{{0,120}}{metric_terms}[^\n]{{0,80}}\b0\.\d+", re.I),
        re.compile(rf"\b0\.\d+[^\n]{{0,80}}{metric_terms}[^\n]{{0,120}}CSGate", re.I),
        re.compile(r"CrossScaleP2P3ConsistencyGate[^\n]{0,120}\b(improve|gain|outperform|surpass|boost)", re.I),
    ]
    hits: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            if pattern.search(line):
                hits.append(f"line {number}: {line.strip()[:140]}")
                break
    if hits:
        return Check(
            "Manuscript lock",
            "No CSGate metric or performance claim before gate opens",
            "missing",
            "; ".join(hits[:5]),
            "Remove CSGate performance wording until completed VisDrone and UAVDT evidence is audited.",
        )
    return Check("Manuscript lock", "No CSGate metric or performance claim before gate opens", "ready", "none")


def audit() -> list[Check]:
    complete_visdrone = run_complete(VISDRONE_RUN)
    complete_uavdt = run_complete(UAVDT_RUN)
    checks = [
        check_run_artifacts("VisDrone", VISDRONE_RUN),
        check_run_artifacts("UAVDT", UAVDT_RUN),
        check_table_row("VisDrone main comparison CSGate row", ROOT / "paper/tables/main_comparison_for_paper.csv", "model", complete_visdrone),
        check_uavdt_status_table(complete_uavdt),
        check_table_row("UAVDT paper table CSGate row", ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv", "model", complete_uavdt),
        check_complexity_table(complete_visdrone),
        check_table_row("CSGate speed row", ROOT / "paper/tables/speed_results.csv", "model", complete_visdrone),
        check_scale_target(complete_visdrone),
        check_diagnostic_rows("Scale-wise recall/precision rows for CSGate", ROOT / "paper/tables/ieee_scale_results_visdrone.csv", complete_visdrone),
        check_diagnostic_rows("Local scale-bin AP rows for CSGate", ROOT / "paper/tables/ieee_scale_ap_results_visdrone.csv", complete_visdrone),
        check_main_draft_metric_lock(complete_visdrone, complete_uavdt),
    ]
    return checks


def write_report(checks: list[Check]) -> None:
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    complete_runs = sum(1 for c in checks[:2] if c.status == "ready")
    gate_status = "OPEN_FOR_POST_RESULT_INTEGRATION" if complete_runs == 2 and missing == 0 else "WAITING_FOR_COMPLETE_CSGATE_RESULTS"
    lines = [
        "# IEEE CSGate Result Gate Audit",
        "",
        "This report is generated by `tools/check_ieee_csgate_result_gate.py`. It prevents partial CSGate metrics from entering paper-facing tables or manuscript claims.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(checks)}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        f"- Gate status: {gate_status}",
        f"- Complete CSGate runs: {complete_runs}/2",
        f"- Required epochs per run: {MIN_EPOCHS}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{check.evidence}` | {check.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `OPEN_FOR_POST_RESULT_INTEGRATION` only means complete CSGate artifacts may be integrated through the guarded protocol.",
            "- It does not mean CSGate is the final method.",
            "- Method promotion still requires a separate method-decision audit and manuscript revision.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

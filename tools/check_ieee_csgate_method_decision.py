from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_csgate_method_decision_audit.md"

CSGATE = "YOLO11n-P2-CSGate-960"
SCALEGATE = "YOLO11n-P2-ScaleGate-960"
VIS_P2 = "YOLO11n-P2-960"
UAV_P2 = "YOLO11n-P2-960"
UAV_YOLO11N = "YOLO11n-960"

PRESERVE_RATIO = 0.98
CROSS_DATASET_REPAIR_RATIO = 0.50


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


@dataclass(frozen=True)
class Metrics:
    best_map50: float | None = None
    best_map50_95: float | None = None
    small_recall: float | None = None
    small_ap50: float | None = None


def status_label(status: str) -> str:
    return {"ready": "READY", "pending": "PENDING", "missing": "MISSING"}[status]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def find_row(path: Path, model: str, scale: str | None = None) -> dict[str, str] | None:
    for row in read_csv(path):
        if row.get("model") != model:
            continue
        if scale is not None and row.get("scale") != scale:
            continue
        return row
    return None


def gate_open() -> bool:
    text = read_text(ROOT / "paper/ieee_csgate_result_gate_audit.md")
    match = re.search(r"- Gate status: ([^\n]+)", text)
    return bool(match and match.group(1).strip() == "OPEN_FOR_POST_RESULT_INTEGRATION")


def table_check(path: Path, model: str, label: str, scale: str | None = None) -> Check:
    row = find_row(path, model, scale=scale)
    if row:
        return Check("Input evidence", label, "ready", f"{path.relative_to(ROOT).as_posix()}; row found")
    return Check(
        "Input evidence",
        label,
        "pending",
        f"{path.relative_to(ROOT).as_posix()}; row not found",
        "Generate this row only after complete audited CSGate evidence exists.",
    )


def load_vis_metrics(model: str) -> Metrics:
    row = find_row(ROOT / "paper/tables/main_comparison_for_paper.csv", model)
    scale_row = find_row(ROOT / "paper/tables/ieee_scale_results_visdrone.csv", model, scale="small")
    ap_row = find_row(ROOT / "paper/tables/ieee_scale_ap_results_visdrone.csv", model, scale="small")
    return Metrics(
        best_map50=parse_float(row.get("best_map50") if row else None),
        best_map50_95=parse_float(row.get("best_map50_95") if row else None),
        small_recall=parse_float(scale_row.get("recall") if scale_row else None),
        small_ap50=parse_float(ap_row.get("ap50") if ap_row else None),
    )


def load_uavdt_metrics(model: str) -> Metrics:
    row = find_row(ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv", model)
    return Metrics(
        best_map50=parse_float(row.get("best_map50") if row else None),
        best_map50_95=parse_float(row.get("best_map50_95") if row else None),
    )


def all_present(values: list[float | None]) -> bool:
    return all(value is not None for value in values)


def fmt(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.6f}"


def evaluate_routes() -> tuple[list[Check], list[str], str]:
    checks: list[Check] = []
    if not gate_open():
        checks.append(
            Check(
                "Decision gate",
                "CSGate post-result integration gate",
                "pending",
                "paper/ieee_csgate_result_gate_audit.md is not open",
                "Wait for both complete CSGate runs and post-result diagnostics.",
            )
        )
        return checks, [], "LOCKED_WAITING_FOR_COMPLETE_CSGATE_RESULTS"

    vis_p2 = load_vis_metrics(VIS_P2)
    vis_sg = load_vis_metrics(SCALEGATE)
    vis_csg = load_vis_metrics(CSGATE)
    uav_p2 = load_uavdt_metrics(UAV_P2)
    uav_y11 = load_uavdt_metrics(UAV_YOLO11N)
    uav_csg = load_uavdt_metrics(CSGATE)

    required = [
        vis_p2.best_map50_95,
        vis_p2.small_ap50,
        vis_p2.small_recall,
        vis_sg.best_map50_95,
        vis_csg.best_map50_95,
        vis_csg.small_ap50,
        vis_csg.small_recall,
        uav_p2.best_map50_95,
        uav_y11.best_map50_95,
        uav_csg.best_map50_95,
    ]
    if not all_present(required):
        checks.append(
            Check(
                "Decision gate",
                "All decision metrics present",
                "pending",
                "one or more CSGate aggregate, UAVDT, or small-object diagnostic values are missing",
                "Refresh CSGate result tables, speed/complexity, scale-wise recall, and local scale-bin AP before deciding.",
            )
        )
        return checks, [], "PENDING_REQUIRED_METRICS"

    routes: list[str] = []
    vis_reference = max(vis_p2.best_map50_95, vis_sg.best_map50_95)

    route_a = (
        vis_csg.best_map50_95 > vis_reference
        and vis_csg.small_ap50 >= vis_p2.small_ap50 * PRESERVE_RATIO
        and vis_csg.small_recall >= vis_p2.small_recall * PRESERVE_RATIO
    )
    checks.append(
        Check(
            "Route A",
            "VisDrone balanced gain over static P2 and ScaleGate",
            "ready" if route_a else "pending",
            (
                f"CSGate mAP50-95 {fmt(vis_csg.best_map50_95)} vs reference {fmt(vis_reference)}; "
                f"small AP50 {fmt(vis_csg.small_ap50)} vs preserve floor {fmt(vis_p2.small_ap50 * PRESERVE_RATIO)}; "
                f"small recall {fmt(vis_csg.small_recall)} vs preserve floor {fmt(vis_p2.small_recall * PRESERVE_RATIO)}"
            ),
            "" if route_a else "Route A does not pass under the fixed pre-result thresholds.",
        )
    )
    if route_a:
        routes.append("A_VISDRONE_BALANCED_GAIN")

    static_gap = uav_y11.best_map50_95 - uav_p2.best_map50_95
    csgate_gap = uav_y11.best_map50_95 - uav_csg.best_map50_95
    repair_fraction = (static_gap - csgate_gap) / static_gap if static_gap > 0 else 0.0
    route_b = (
        uav_csg.best_map50_95 > uav_p2.best_map50_95
        and repair_fraction >= CROSS_DATASET_REPAIR_RATIO
        and vis_csg.best_map50_95 >= vis_p2.best_map50_95 * PRESERVE_RATIO
    )
    checks.append(
        Check(
            "Route B",
            "Cross-dataset static-P2 repair",
            "ready" if route_b else "pending",
            (
                f"UAVDT CSGate {fmt(uav_csg.best_map50_95)} vs static P2 {fmt(uav_p2.best_map50_95)}; "
                f"repair fraction {repair_fraction:.3f} vs required {CROSS_DATASET_REPAIR_RATIO:.3f}; "
                f"VisDrone preservation {fmt(vis_csg.best_map50_95)} vs floor {fmt(vis_p2.best_map50_95 * PRESERVE_RATIO)}"
            ),
            "" if route_b else "Route B does not pass under the fixed pre-result thresholds.",
        )
    )
    if route_b:
        routes.append("B_CROSS_DATASET_REPAIR")

    route_c = (
        (vis_csg.small_ap50 > vis_p2.small_ap50 or vis_csg.small_recall > vis_p2.small_recall)
        and vis_csg.best_map50_95 >= vis_p2.best_map50_95 * PRESERVE_RATIO
    )
    checks.append(
        Check(
            "Route C",
            "Small-object diagnostic gain",
            "ready" if route_c else "pending",
            (
                f"small AP50 {fmt(vis_csg.small_ap50)} vs {fmt(vis_p2.small_ap50)}; "
                f"small recall {fmt(vis_csg.small_recall)} vs {fmt(vis_p2.small_recall)}; "
                f"VisDrone preservation {fmt(vis_csg.best_map50_95)} vs floor {fmt(vis_p2.best_map50_95 * PRESERVE_RATIO)}"
            ),
            "" if route_c else "Route C does not pass under the fixed pre-result thresholds.",
        )
    )
    if route_c:
        routes.append("C_SMALL_OBJECT_DIAGNOSTIC_GAIN")

    decision = "CSGATE_CAN_BE_METHOD_CANDIDATE" if routes else "DO_NOT_USE_CSGATE_AS_MAIN_METHOD"
    return checks, routes, decision


def audit() -> tuple[list[Check], list[str], str]:
    checks = [
        table_check(ROOT / "paper/tables/main_comparison_for_paper.csv", VIS_P2, "VisDrone static P2 baseline row"),
        table_check(ROOT / "paper/tables/main_comparison_for_paper.csv", SCALEGATE, "VisDrone ScaleGate row"),
        table_check(ROOT / "paper/tables/main_comparison_for_paper.csv", CSGATE, "VisDrone CSGate row"),
        table_check(ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv", UAV_YOLO11N, "UAVDT YOLO11n baseline row"),
        table_check(ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv", UAV_P2, "UAVDT static P2 row"),
        table_check(ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv", CSGATE, "UAVDT CSGate row"),
        table_check(ROOT / "paper/tables/ieee_scale_results_visdrone.csv", VIS_P2, "VisDrone static P2 small recall row", scale="small"),
        table_check(ROOT / "paper/tables/ieee_scale_results_visdrone.csv", CSGATE, "VisDrone CSGate small recall row", scale="small"),
        table_check(ROOT / "paper/tables/ieee_scale_ap_results_visdrone.csv", VIS_P2, "VisDrone static P2 small AP row", scale="small"),
        table_check(ROOT / "paper/tables/ieee_scale_ap_results_visdrone.csv", CSGATE, "VisDrone CSGate small AP row", scale="small"),
    ]
    route_checks, routes, decision = evaluate_routes()
    checks.extend(route_checks)
    return checks, routes, decision


def write_report(checks: list[Check], routes: list[str], decision: str) -> None:
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE CSGate Method Decision Audit",
        "",
        "This report is generated by `tools/check_ieee_csgate_method_decision.py`. It applies fixed CSGate acceptance routes after the CSGate result gate opens.",
        "",
        "The thresholds below are decision guardrails only; they are not manuscript metrics. They are fixed before final CSGate results are available to reduce post-hoc cherry-picking.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(checks)}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        f"- Decision status: {decision}",
        f"- Accepted routes: {', '.join(routes) if routes else 'none'}",
        f"- Preservation ratio: {PRESERVE_RATIO:.2f}",
        f"- Cross-dataset repair ratio: {CROSS_DATASET_REPAIR_RATIO:.2f}",
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
            "## Decision Rules",
            "",
            "- Route A passes only if CSGate improves VisDrone best mAP50-95 over both static P2 and ScaleGate while preserving at least 98% of static-P2 small AP50 and small recall.",
            "- Route B passes only if CSGate improves UAVDT best mAP50-95 over static P2, repairs at least 50% of the static-P2-to-YOLO11n UAVDT gap, and preserves at least 98% of VisDrone static-P2 best mAP50-95.",
            "- Route C passes only if CSGate improves VisDrone small AP50 or small recall over static P2 while preserving at least 98% of VisDrone static-P2 best mAP50-95.",
            "- If no route passes, CSGate must not enter the title, abstract, contribution list, or conclusion as the main proposed method.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks, routes, decision = audit()
    write_report(checks, routes, decision)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

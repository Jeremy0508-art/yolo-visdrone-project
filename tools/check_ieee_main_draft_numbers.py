from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_DRAFT = ROOT / "paper/ieee_trans/main_draft.tex"
REPORT_PATH = ROOT / "paper/ieee_main_draft_number_audit.md"


@dataclass(frozen=True)
class NumberHit:
    token: str
    line: int
    context: str
    status: str
    evidence: str
    action: str = ""


def read_rows(rel_path: str) -> list[dict[str, str]]:
    path = ROOT / rel_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def quantize(value: str, decimals: int) -> str | None:
    try:
        decimal = Decimal(value)
    except (InvalidOperation, TypeError):
        return None
    quant = Decimal("1") if decimals == 0 else Decimal("1").scaleb(-decimals)
    return str(decimal.quantize(quant, rounding=ROUND_HALF_UP))


def add_value(index: dict[str, list[str]], token: str | None, evidence: str) -> None:
    if token is None:
        return
    index.setdefault(token, []).append(evidence)


def build_value_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}

    for row in read_rows("paper/tables/main_comparison_for_paper.csv"):
        model = row.get("model", "unknown")
        for field in ["final_map50", "final_map50_95", "best_map50", "best_map50_95", "precision", "recall"]:
            value = row.get(field, "")
            for decimals in [3, 5]:
                add_value(
                    index,
                    quantize(value, decimals),
                    f"paper/tables/main_comparison_for_paper.csv::{model}.{field} rounded to {decimals}",
                )

    for row in read_rows("paper/tables/ieee_uavdt_results_for_paper.csv"):
        model = row.get("model", "unknown")
        for field in ["final_map50", "final_map50_95", "best_map50", "best_map50_95", "final_precision", "final_recall"]:
            value = row.get(field, "")
            for decimals in [3, 5]:
                add_value(
                    index,
                    quantize(value, decimals),
                    f"paper/tables/ieee_uavdt_results_for_paper.csv::{model}.{field} rounded to {decimals}",
                )

    uavdt_rows = {row.get("model", ""): row for row in read_rows("paper/tables/ieee_uavdt_results_for_paper.csv")}
    try:
        yolo11n = Decimal(uavdt_rows["YOLO11n-960"]["best_map50_95"])
        static_p2 = Decimal(uavdt_rows["YOLO11n-P2-960"]["best_map50_95"])
        csgate = Decimal(uavdt_rows["YOLO11n-P2-CSGate-960"]["best_map50_95"])
        repair_pct = (csgate - static_p2) / (yolo11n - static_p2) * Decimal("100")
    except (KeyError, InvalidOperation, ZeroDivisionError):
        repair_pct = None
    if repair_pct is not None:
        for decimals in [1, 3]:
            add_value(
                index,
                quantize(str(repair_pct), decimals),
                "derived from paper/tables/ieee_uavdt_results_for_paper.csv::(CSGate-P2)/(YOLO11n-P2) best_map50_95 gap",
            )

    for row in read_rows("paper/tables/model_complexity.csv"):
        model = row.get("model", "unknown")
        for field, decimals_list in {
            "gflops": [1, 3],
            "weight_size_mb": [2, 3],
            "parameters": [0],
        }.items():
            value = row.get(field, "")
            for decimals in decimals_list:
                add_value(
                    index,
                    quantize(value, decimals),
                    f"paper/tables/model_complexity.csv::{model}.{field} rounded to {decimals}",
                )
        params = row.get("parameters", "")
        if params:
            try:
                params_m = str(Decimal(params) / Decimal("1000000"))
            except InvalidOperation:
                params_m = ""
            for decimals in [3]:
                add_value(
                    index,
                    quantize(params_m, decimals),
                    f"paper/tables/model_complexity.csv::{model}.parameters/1e6 rounded to {decimals}",
                )

    for row in read_rows("paper/tables/ieee_scale_results_visdrone.csv"):
        model = row.get("model", "unknown")
        scale = row.get("scale", "unknown")
        for field in ["recall", "precision"]:
            value = row.get(field, "")
            for decimals in [3, 6]:
                add_value(
                    index,
                    quantize(value, decimals),
                    f"paper/tables/ieee_scale_results_visdrone.csv::{model}.{scale}.{field} rounded to {decimals}",
                )

    for row in read_rows("paper/tables/ieee_scale_ap_results_visdrone.csv"):
        model = row.get("model", "unknown")
        scale = row.get("scale", "unknown")
        for field in ["ap50", "map50_95", "precision_at_max_f1", "recall_at_max_f1"]:
            value = row.get(field, "")
            for decimals in [3, 6]:
                add_value(
                    index,
                    quantize(value, decimals),
                    f"paper/tables/ieee_scale_ap_results_visdrone.csv::{model}.{scale}.{field} rounded to {decimals}",
                )

    config_text = (ROOT / "configs/models/yolo11n_p2_scalegate.yaml").read_text(encoding="utf-8", errors="ignore")
    source_text = (ROOT / "src/models/attention/scale_aware_p2_gate.py").read_text(encoding="utf-8", errors="ignore")
    if "ScaleAwareP2Gate, [32, 4, 0.5]" in config_text and "max_delta: float = 0.5" in source_text:
        add_value(
            index,
            "0.5",
            "ScaleAwareP2Gate max_delta from configs/models/yolo11n_p2_scalegate.yaml and src/models/attention/scale_aware_p2_gate.py",
        )

    return index


def extract_hits(index: dict[str, list[str]]) -> list[NumberHit]:
    text = MAIN_DRAFT.read_text(encoding="utf-8", errors="ignore")
    hits: list[NumberHit] = []
    pattern = re.compile(r"(?<![A-Za-z])\d+\.\d+")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in pattern.finditer(line):
            token = match.group(0)
            context = line.strip()
            if r"\includegraphics" in line and "width=" in line:
                hits.append(
                    NumberHit(
                        token,
                        line_no,
                        context,
                        "ignored",
                        "LaTeX figure width/layout parameter, not an experimental value",
                    )
                )
                continue
            evidences = index.get(token, [])
            if evidences:
                hits.append(NumberHit(token, line_no, context, "ready", "; ".join(evidences[:4])))
            else:
                hits.append(
                    NumberHit(
                        token,
                        line_no,
                        context,
                        "missing",
                        "no matching rounded value or documented design constant found",
                        "Trace this number to a CSV/config source, add an explicit allowed design constant, or remove it from the draft.",
                    )
                )
    return hits


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "ignored": "IGNORED",
        "missing": "MISSING",
    }[status]


def write_report(hits: list[NumberHit]) -> None:
    total = len(hits)
    ready = sum(1 for hit in hits if hit.status == "ready")
    ignored = sum(1 for hit in hits if hit.status == "ignored")
    missing = sum(1 for hit in hits if hit.status == "missing")

    lines = [
        "# IEEE Main Draft Number Audit",
        "",
        "This report is generated by `tools/check_ieee_main_draft_numbers.py`. It traces decimal numbers in `paper/ieee_trans/main_draft.tex` to audited CSV sources or explicit design constants.",
        "",
        "The audit is intended for the advisor-review draft. It does not validate pending ScaleGate performance values, and it ignores LaTeX layout dimensions such as figure widths.",
        "",
        "## Summary",
        "",
        f"- Total decimal tokens: {total}",
        f"- Ready: {ready}",
        f"- Ignored layout/design-free tokens: {ignored}",
        f"- Missing: {missing}",
        "",
        "## Number Trace",
        "",
        "| Token | Line | Status | Evidence | Context | Action |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for hit in hits:
        context = hit.context.replace("|", "\\|")
        evidence = hit.evidence.replace("|", "\\|")
        lines.append(
            f"| `{hit.token}` | {hit.line} | {status_label(hit.status)} | `{evidence}` | {context} | {hit.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the rounded number appears in an audited source table or an explicitly checked design constant.",
            "- `IGNORED` means the token is a LaTeX layout parameter, not an experimental claim.",
            "- `MISSING` must be fixed before treating the draft as a trustworthy advisor-review PDF.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    index = build_value_index()
    hits = extract_hits(index)
    write_report(hits)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

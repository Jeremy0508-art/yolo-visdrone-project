from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTION_DRAFT = ROOT / "paper/ieee_trans/section_draft_pack.md"
REPORT_PATH = ROOT / "paper/ieee_number_trace_audit.md"


@dataclass(frozen=True)
class DirectClaim:
    section: str
    label: str
    value_text: str
    source_path: str
    row_key: tuple[str, str]
    field: str
    decimals: int


@dataclass(frozen=True)
class DerivedClaim:
    section: str
    label: str
    value_text: str
    source_path: str
    left_key: tuple[str, str]
    right_key: tuple[str, str]
    field: str
    decimals: int


def read_rows(rel_path: str) -> list[dict[str, str]]:
    path = ROOT / rel_path
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_sources() -> dict[str, list[dict[str, str]]]:
    return {
        "paper/tables/main_comparison_for_paper.csv": read_rows("paper/tables/main_comparison_for_paper.csv"),
        "paper/tables/model_complexity.csv": read_rows("paper/tables/model_complexity.csv"),
        "paper/tables/speed_results.csv": read_rows("paper/tables/speed_results.csv"),
        "paper/tables/ieee_scale_results_visdrone.csv": read_rows("paper/tables/ieee_scale_results_visdrone.csv"),
        "paper/tables/ieee_scale_ap_results_visdrone.csv": read_rows("paper/tables/ieee_scale_ap_results_visdrone.csv"),
    }


def get_row(rows: list[dict[str, str]], key: tuple[str, str]) -> dict[str, str] | None:
    model, scale = key
    for row in rows:
        if row.get("model") == model and (not scale or row.get("scale") == scale):
            return row
    return None


def fmt_decimal(value: str | Decimal, decimals: int) -> str:
    decimal = value if isinstance(value, Decimal) else Decimal(value)
    quant = Decimal("1") if decimals == 0 else Decimal("1").scaleb(-decimals)
    return str(decimal.quantize(quant, rounding=ROUND_HALF_UP))


DIRECT_CLAIMS: list[DirectClaim] = [
    DirectClaim("Main results", "YOLO11n-960 best mAP50", "0.42136", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n baseline 960", ""), "best_map50", 5),
    DirectClaim("Main results", "YOLO11n-960 best mAP50-95", "0.25067", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n baseline 960", ""), "best_map50_95", 5),
    DirectClaim("Main results", "YOLO11n-P2-960 best mAP50", "0.42361", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-960", ""), "best_map50", 5),
    DirectClaim("Main results", "YOLO11n-P2-960 best mAP50-95", "0.25552", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-960", ""), "best_map50_95", 5),
    DirectClaim("Main results", "YOLO11n-P2-CA-960 best mAP50", "0.41996", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-CoordAttention-960", ""), "best_map50", 5),
    DirectClaim("Main results", "YOLO11n-P2-CA-960 best mAP50-95", "0.25174", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-CoordAttention-960", ""), "best_map50_95", 5),
    DirectClaim("Main results", "YOLO11n-P2-TOFC-960 best mAP50", "0.42837", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-TOFC-960", ""), "best_map50", 5),
    DirectClaim("Main results", "YOLO11n-P2-TOFC-960 best mAP50-95", "0.26054", "paper/tables/main_comparison_for_paper.csv", ("YOLO11n-P2-TOFC-960", ""), "best_map50_95", 5),
    DirectClaim("Main results", "YOLO11s-960 best mAP50", "0.48901", "paper/tables/main_comparison_for_paper.csv", ("YOLO11s baseline 960", ""), "best_map50", 5),
    DirectClaim("Main results", "YOLO11s-960 best mAP50-95", "0.29812", "paper/tables/main_comparison_for_paper.csv", ("YOLO11s baseline 960", ""), "best_map50_95", 5),
    DirectClaim("Complexity", "YOLO11n-960 params/M", "2.592", "paper/tables/model_complexity.csv", ("YOLO11n baseline 960", ""), "parameters", 3),
    DirectClaim("Complexity", "YOLO11n-960 GFLOPs", "6.5", "paper/tables/model_complexity.csv", ("YOLO11n baseline 960", ""), "gflops", 1),
    DirectClaim("Complexity", "YOLO11n-P2-960 params/M", "2.894", "paper/tables/model_complexity.csv", ("YOLO11n-P2-960", ""), "parameters", 3),
    DirectClaim("Complexity", "YOLO11n-P2-960 GFLOPs", "10.7", "paper/tables/model_complexity.csv", ("YOLO11n-P2-960", ""), "gflops", 1),
    DirectClaim("Complexity", "YOLO11n-P2-CA-960 params/M", "2.904", "paper/tables/model_complexity.csv", ("YOLO11n-P2-CoordAttention-960", ""), "parameters", 3),
    DirectClaim("Complexity", "YOLO11n-P2-CA-960 GFLOPs", "10.7", "paper/tables/model_complexity.csv", ("YOLO11n-P2-CoordAttention-960", ""), "gflops", 1),
    DirectClaim("Complexity", "YOLO11n-P2-TOFC-960 params/M", "2.896", "paper/tables/model_complexity.csv", ("YOLO11n-P2-TOFC-960", ""), "parameters", 3),
    DirectClaim("Complexity", "YOLO11n-P2-TOFC-960 GFLOPs", "10.8", "paper/tables/model_complexity.csv", ("YOLO11n-P2-TOFC-960", ""), "gflops", 1),
    DirectClaim("Speed", "YOLO11n-960 weight size", "5.25", "paper/tables/model_complexity.csv", ("YOLO11n baseline 960", ""), "weight_size_mb", 2),
    DirectClaim("Speed", "YOLO11n-960 latency", "21.31", "paper/tables/speed_results.csv", ("YOLO11n baseline 960", ""), "mean_latency_ms_wall", 2),
    DirectClaim("Speed", "YOLO11n-P2-960 weight size", "6.06", "paper/tables/model_complexity.csv", ("YOLO11n-P2-960", ""), "weight_size_mb", 2),
    DirectClaim("Speed", "YOLO11n-P2-960 latency", "22.88", "paper/tables/speed_results.csv", ("YOLO11n-P2-960", ""), "mean_latency_ms_wall", 2),
    DirectClaim("Speed", "YOLO11n-P2-CA-960 weight size", "6.09", "paper/tables/model_complexity.csv", ("YOLO11n-P2-CoordAttention-960", ""), "weight_size_mb", 2),
    DirectClaim("Speed", "YOLO11n-P2-CA-960 latency", "23.36", "paper/tables/speed_results.csv", ("YOLO11n-P2-CoordAttention-960", ""), "mean_latency_ms_wall", 2),
    DirectClaim("Speed", "YOLO11n-P2-TOFC-960 weight size", "6.07", "paper/tables/model_complexity.csv", ("YOLO11n-P2-TOFC-960", ""), "weight_size_mb", 2),
    DirectClaim("Speed", "YOLO11n-P2-TOFC-960 latency", "22.61", "paper/tables/speed_results.csv", ("YOLO11n-P2-TOFC-960", ""), "mean_latency_ms_wall", 2),
    DirectClaim("Speed", "YOLO11s-960 params/M", "9.432", "paper/tables/model_complexity.csv", ("YOLO11s baseline 960", ""), "parameters", 3),
    DirectClaim("Speed", "YOLO11s-960 GFLOPs", "21.6", "paper/tables/model_complexity.csv", ("YOLO11s baseline 960", ""), "gflops", 1),
    DirectClaim("Speed", "YOLO11s-960 weight size", "18.32", "paper/tables/model_complexity.csv", ("YOLO11s baseline 960", ""), "weight_size_mb", 2),
    DirectClaim("Speed", "YOLO11s-960 latency", "24.02", "paper/tables/speed_results.csv", ("YOLO11s baseline 960", ""), "mean_latency_ms_wall", 2),
    DirectClaim("Scale recall", "YOLO11n-960 small recall", "0.420259", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-960", "small"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-960 small recall", "0.450124", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-960", "small"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-CA-960 small recall", "0.455089", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-CA-960", "small"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-TOFC-960 small recall", "0.430828", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "small"), "recall", 6),
    DirectClaim("Scale precision", "YOLO11n-960 small precision", "0.661952", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-960", "small"), "precision", 6),
    DirectClaim("Scale precision", "YOLO11n-P2-960 small precision", "0.674799", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-960", "small"), "precision", 6),
    DirectClaim("Scale precision", "YOLO11n-P2-CA-960 small precision", "0.666036", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-CA-960", "small"), "precision", 6),
    DirectClaim("Scale precision", "YOLO11n-P2-TOFC-960 small precision", "0.677857", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "small"), "precision", 6),
    DirectClaim("Scale recall", "YOLO11n-960 medium recall", "0.789464", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-960", "medium"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-960 medium recall", "0.778928", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-960", "medium"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-960 large recall", "0.890449", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-960", "large"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-960 large recall", "0.887640", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-960", "large"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-CA-960 medium recall", "0.781450", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-CA-960", "medium"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-CA-960 large recall", "0.882022", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-CA-960", "large"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-TOFC-960 medium recall", "0.765421", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "medium"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11n-P2-TOFC-960 large recall", "0.874532", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "large"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11s-960 small recall", "0.492703", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11s-960", "small"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11s-960 medium recall", "0.827555", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11s-960", "medium"), "recall", 6),
    DirectClaim("Scale recall", "YOLO11s-960 large recall", "0.899813", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11s-960", "large"), "recall", 6),
    DirectClaim("Local AP", "YOLO11n-960 small AP50", "0.229995", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-960 small mAP50-95", "0.116295", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 small AP50", "0.247659", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 small mAP50-95", "0.131540", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-P2-CA-960 small AP50", "0.239473", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-CA-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-P2-CA-960 small mAP50-95", "0.126067", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-CA-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-P2-TOFC-960 small AP50", "0.229853", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-P2-TOFC-960 small mAP50-95", "0.120661", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-TOFC-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLOv8n-960 small AP50", "0.237713", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLOv8n-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLOv8n-960 small mAP50-95", "0.122135", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLOv8n-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11s-960 small AP50", "0.302540", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11s-960", "small"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11s-960 small mAP50-95", "0.159421", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11s-960", "small"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-960 medium AP50", "0.452575", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "medium"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-960 medium mAP50-95", "0.309690", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "medium"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 medium AP50", "0.438392", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "medium"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 medium mAP50-95", "0.300511", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "medium"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-960 large AP50", "0.577546", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "large"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-960 large mAP50-95", "0.459221", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-960", "large"), "map50_95", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 large AP50", "0.456420", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "large"), "ap50", 6),
    DirectClaim("Local AP", "YOLO11n-P2-960 large mAP50-95", "0.368950", "paper/tables/ieee_scale_ap_results_visdrone.csv", ("YOLO11n-P2-960", "large"), "map50_95", 6),
]


DERIVED_CLAIMS: list[DerivedClaim] = [
    DerivedClaim("Scale recall", "YOLO11n-P2-960 small recall gain over YOLO11n-960", "0.029865", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-960", "small"), ("YOLO11n-960", "small"), "recall", 6),
    DerivedClaim("Scale recall", "YOLO11n-P2-CA-960 small recall gain over YOLO11n-960", "0.034830", "paper/tables/ieee_scale_results_visdrone.csv", ("YOLO11n-P2-CA-960", "small"), ("YOLO11n-960", "small"), "recall", 6),
]


def direct_status(claim: DirectClaim, sources: dict[str, list[dict[str, str]]], draft: str) -> tuple[str, str]:
    rows = sources.get(claim.source_path, [])
    row = get_row(rows, claim.row_key)
    if row is None:
        return "MISSING", "source row not found"
    if claim.field not in row:
        return "MISSING", f"source field `{claim.field}` not found"
    raw = row[claim.field]
    if claim.field == "parameters" and claim.value_text.count(".") == 1:
        actual = fmt_decimal(Decimal(raw) / Decimal("1000000"), claim.decimals)
    else:
        actual = fmt_decimal(raw, claim.decimals)
    if actual != claim.value_text:
        return "MISMATCH", f"source value `{actual}`"
    if claim.value_text not in draft:
        return "SOURCE_ONLY", "value matches source but is not present in section draft"
    return "READY", f"{claim.source_path}: {claim.row_key[0]} {claim.row_key[1]} {claim.field}={raw}"


def derived_status(claim: DerivedClaim, sources: dict[str, list[dict[str, str]]], draft: str) -> tuple[str, str]:
    rows = sources.get(claim.source_path, [])
    left = get_row(rows, claim.left_key)
    right = get_row(rows, claim.right_key)
    if left is None or right is None:
        return "MISSING", "source row not found"
    try:
        actual = fmt_decimal(Decimal(left[claim.field]) - Decimal(right[claim.field]), claim.decimals)
    except KeyError:
        return "MISSING", f"source field `{claim.field}` not found"
    if actual != claim.value_text:
        return "MISMATCH", f"computed value `{actual}`"
    if claim.value_text not in draft:
        return "SOURCE_ONLY", "derived value matches sources but is not present in section draft"
    return "READY", f"{claim.left_key[0]} {claim.left_key[1]} - {claim.right_key[0]} {claim.right_key[1]}"


def find_untracked_decimal_tokens(draft: str, known_values: set[str]) -> list[str]:
    tokens = sorted(set(re.findall(r"(?<![A-Za-z])\d+\.\d+", draft)), key=lambda x: (Decimal(x), x))
    return [token for token in tokens if token not in known_values]


def make_report() -> str:
    draft = SECTION_DRAFT.read_text(encoding="utf-8")
    sources = load_sources()
    direct_rows: list[tuple[DirectClaim, str, str]] = []
    derived_rows: list[tuple[DerivedClaim, str, str]] = []

    for claim in DIRECT_CLAIMS:
        status, evidence = direct_status(claim, sources, draft)
        direct_rows.append((claim, status, evidence))
    for claim in DERIVED_CLAIMS:
        status, evidence = derived_status(claim, sources, draft)
        derived_rows.append((claim, status, evidence))

    known_values = {claim.value_text for claim in DIRECT_CLAIMS}
    known_values.update(claim.value_text for claim in DERIVED_CLAIMS)
    untracked = find_untracked_decimal_tokens(draft, known_values)
    nonready = sum(1 for _, status, _ in direct_rows if status not in {"READY", "SOURCE_ONLY"})
    nonready += sum(1 for _, status, _ in derived_rows if status not in {"READY", "SOURCE_ONLY"})
    ready = sum(1 for _, status, _ in direct_rows if status == "READY")
    ready += sum(1 for _, status, _ in derived_rows if status == "READY")
    source_only = sum(1 for _, status, _ in direct_rows if status == "SOURCE_ONLY")
    source_only += sum(1 for _, status, _ in derived_rows if status == "SOURCE_ONLY")

    lines = [
        "# IEEE Number Trace Audit",
        "",
        "This report is generated by `tools/build_ieee_number_trace_audit.py`. It checks key numeric claims in `paper/ieee_trans/section_draft_pack.md` against audited CSV sources.",
        "",
        "It does not launch training and does not validate pending TOFC or UAVDT results.",
        "",
        "## Summary",
        "",
        f"- Direct claims checked: {len(direct_rows)}",
        f"- Derived claims checked: {len(derived_rows)}",
        f"- Ready in draft: {ready}",
        f"- Source-only matches: {source_only}",
        f"- Non-ready numeric claims: {nonready}",
        f"- Untracked decimal tokens in draft: {len(untracked)}",
        "",
        "## Direct Claim Trace",
        "",
        "| Section | Claim | Draft value | Status | Evidence |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for claim, status, evidence in direct_rows:
        lines.append(f"| {claim.section} | {claim.label} | `{claim.value_text}` | {status} | `{evidence}` |")

    lines.extend(
        [
            "",
            "## Derived Claim Trace",
            "",
            "| Section | Claim | Draft value | Status | Evidence |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for claim, status, evidence in derived_rows:
        lines.append(f"| {claim.section} | {claim.label} | `{claim.value_text}` | {status} | `{evidence}` |")

    lines.extend(
        [
            "",
            "## Untracked Decimal Tokens",
            "",
        ]
    )
    if untracked:
        lines.append("These decimal tokens appear in the section draft but are not part of the audited claim list above. They should be reviewed before moving the text into `main.tex`.")
        lines.append("")
        for token in untracked:
            lines.append(f"- `{token}`")
    else:
        lines.append("No untracked decimal tokens found in the current section draft.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the draft value is present and matches a source CSV or a documented source-derived difference.",
            "- `SOURCE_ONLY` means the source value is valid but the current draft no longer contains that exact number.",
            "- `MISMATCH` or `MISSING` must be resolved before a final IEEE `main.tex` is assembled.",
            "- This audit covers the current draft pack. Any new numerical paragraph should be added to this script or traced by a stronger future checker.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    REPORT_PATH.write_text(make_report(), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

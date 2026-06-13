from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/manuscript_number_trace_audit.md"


TABLE_PATHS = [
    "paper/tables/main_comparison_for_paper.csv",
    "paper/tables/ablation_results.csv",
    "paper/tables/speed_results.csv",
    "paper/tables/model_complexity.csv",
    "paper/tables/object_scale_distribution.csv",
    "paper/tables/scale_group_results.csv",
    "paper/tables/per_class_results.csv",
]


ALLOWED_CONTEXT_VALUES = {
    "0.0": "documented augmentation/configuration value",
    "0.01": "documented training configuration value",
    "0.1": "documented augmentation/configuration value",
    "0.35": "documented augmentation/configuration value",
    "0.7": "documented Ultralytics validation/NMS setting",
    "2.7": "documented PyTorch version family",
    "3.12": "documented Python version family",
    "8.4": "documented Ultralytics version family",
    "10.5": "LaTeX document class size",
    "12.8": "documented CUDA version",
}


@dataclass
class NumberHit:
    value: str
    line: int
    context: str
    status: str
    evidence: str


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
    }[status]


def normalize_number(value: str) -> str:
    try:
        number = float(value)
    except ValueError:
        return value
    if number == 0:
        return "0.0"
    return value.rstrip("0").rstrip(".") if "." in value else value


def decimal_format(value: Decimal, digits: int) -> str:
    quantum = Decimal("1") if digits == 0 else Decimal("1").scaleb(-digits)
    return f"{value.quantize(quantum, rounding=ROUND_HALF_UP):f}"


def add_numeric_variants(evidence: dict[str, str], value: str, source: str) -> None:
    try:
        decimal_value = Decimal(str(value))
        number = float(decimal_value)
    except (TypeError, ValueError, InvalidOperation):
        return

    variants = {value, normalize_number(value)}
    for digits in range(1, 7):
        rounded = decimal_format(decimal_value, digits)
        variants.add(rounded)
        variants.add(normalize_number(rounded))

    if abs(number) < 1:
        percent = decimal_value * Decimal("100")
        for digits in range(1, 4):
            rounded = decimal_format(percent, digits)
            variants.add(rounded)
            variants.add(normalize_number(rounded))

    if abs(number) >= 100_000:
        millions = decimal_value / Decimal("1000000")
        for digits in range(1, 4):
            rounded = decimal_format(millions, digits)
            variants.add(rounded)
            variants.add(normalize_number(rounded))

    for variant in variants:
        evidence.setdefault(variant, source)


def build_evidence_numbers() -> dict[str, str]:
    evidence: dict[str, str] = {}
    decimal_values: list[tuple[Decimal, str]] = []
    for value, source in ALLOWED_CONTEXT_VALUES.items():
        evidence[value] = source
        evidence[normalize_number(value)] = source

    for rel_path in TABLE_PATHS:
        path = ROOT / rel_path
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                for key, value in row.items():
                    if value is None:
                        continue
                    stripped = value.strip().lstrip("+")
                    if re.fullmatch(r"-?\d+(\.\d+)?", stripped):
                        add_numeric_variants(evidence, stripped, f"{rel_path}:{key}")
                        try:
                            decimal_values.append((Decimal(stripped), f"{rel_path}:{key}"))
                        except InvalidOperation:
                            pass

    small_values = [(value, source) for value, source in decimal_values if abs(value) < 1]
    for idx, (left, left_source) in enumerate(small_values):
        for right, right_source in small_values[idx + 1 :]:
            diff = abs(left - right)
            if diff == 0 or diff >= 1:
                continue
            source = f"derived difference between {left_source} and {right_source}"
            add_numeric_variants(evidence, str(diff), source)
    return evidence


def manuscript_body() -> str:
    if not MANUSCRIPT_PATH.exists():
        return ""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8-sig")
    marker = r"\begin{document}"
    idx = text.find(marker)
    body = text[idx + len(marker) :] if idx >= 0 else text
    bibliography_marker = r"\begin{thebibliography}"
    bibliography_idx = body.find(bibliography_marker)
    return body[:bibliography_idx] if bibliography_idx >= 0 else body


def extract_number_hits(text: str, evidence: dict[str, str]) -> list[NumberHit]:
    hits: list[NumberHit] = []
    number_pattern = re.compile(r"(?<![A-Za-z])(?<!\\)\b\d+\.\d+\b")
    for match in number_pattern.finditer(text):
        value = match.group(0)
        normalized = normalize_number(value)
        line_no = text.count("\n", 0, match.start()) + 1
        line = text.splitlines()[line_no - 1].strip()
        if r"\includegraphics" in line or r"\begin{tabular}" in line:
            continue
        if value in evidence:
            status = "ready"
            source = evidence[value]
        elif normalized in evidence:
            status = "ready"
            source = evidence[normalized]
        else:
            status = "missing"
            source = "not found in paper tables or allowed configuration values"
        hits.append(NumberHit(value, line_no, line[:140], status, source))
    return hits


def write_report(hits: list[NumberHit]) -> None:
    total = len(hits)
    ready = sum(1 for hit in hits if hit.status == "ready")
    missing = sum(1 for hit in hits if hit.status == "missing")

    lines = [
        "# Manuscript Number Trace Audit",
        "",
        "This report is generated by `tools/check_manuscript_number_trace.py`. It scans decimal numbers in `paper/manuscript_submission_candidate.tex` and checks whether they can be traced to paper-facing CSV tables or documented configuration/version constants.",
        "",
        "This audit is intentionally conservative. It checks decimal values only; integer counts, section numbers, citations, and page layout values are outside its scope.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Value | Line | Status | Evidence | Context |",
        "| ---: | ---: | --- | --- | --- |",
    ]
    for hit in hits:
        context = hit.context.replace("|", "\\|")
        lines.append(
            f"| {hit.value} | {hit.line} | {status_symbol(hit.status)} | `{hit.evidence}` | {context} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the decimal value appears in an audited table, a derived rounded form of a table value, or the documented allowlist for configuration/version constants.",
            "- `MISSING` means the value should be checked manually before final submission and either traced to evidence or removed from the manuscript.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    evidence = build_evidence_numbers()
    hits = extract_number_hits(manuscript_body(), evidence)
    write_report(hits)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

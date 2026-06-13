from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/manuscript_length_audit.md"


MIN_CHINESE_CHARS = 7500
MIN_SECTIONS = 6
MIN_SUBSECTIONS = 10
MIN_TABLES = 7
MIN_FIGURES = 5
MIN_REFERENCES = 25


@dataclass
class LengthCheck:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "partial": "PARTIAL",
        "missing": "MISSING",
    }[status]


def strip_latex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", "", text, flags=re.S)
    text = re.sub(r"\\(includegraphics|label|ref|cite|url|href)(\[[^\]]*\])?\{[^}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}$&#_^~]", " ", text)
    return text


def count_chinese_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def count_english_words(text: str) -> int:
    return len(re.findall(r"\b[A-Za-z][A-Za-z0-9-]*\b", text))


def audit() -> list[LengthCheck]:
    if not TEX_PATH.exists():
        return [
            LengthCheck(
                "LaTeX manuscript exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore or regenerate the LaTeX manuscript.",
            )
        ]

    text = TEX_PATH.read_text(encoding="utf-8")
    body_text = strip_latex(text)
    chinese_chars = count_chinese_chars(body_text)
    english_words = count_english_words(body_text)
    section_count = len(re.findall(r"\\section\{", text))
    subsection_count = len(re.findall(r"\\subsection\{", text))
    table_count = len(re.findall(r"\\begin\{table\}", text))
    figure_count = len(re.findall(r"\\begin\{figure\}", text))
    reference_count = len(re.findall(r"\\bibitem\{", text))

    checks = [
        LengthCheck(
            "Chinese character volume",
            "ready" if chinese_chars >= MIN_CHINESE_CHARS else "partial",
            f"{chinese_chars} Chinese characters; target >= {MIN_CHINESE_CHARS}",
            ""
            if chinese_chars >= MIN_CHINESE_CHARS
            else "Expand introduction, related work, method rationale, fair-comparison analysis, discussion, and limitations after server results are complete.",
        ),
        LengthCheck(
            "English technical token volume",
            "ready" if english_words >= 300 else "partial",
            f"{english_words} English/technical tokens",
            "" if english_words >= 300 else "Ensure model names, metrics, datasets, and method terms are clearly introduced.",
        ),
        LengthCheck(
            "Section count",
            "ready" if section_count >= MIN_SECTIONS else "partial",
            f"{section_count} sections; target >= {MIN_SECTIONS}",
            "" if section_count >= MIN_SECTIONS else "Keep journal sections for introduction, related work, method, experiments, discussion, and conclusion.",
        ),
        LengthCheck(
            "Subsection count",
            "ready" if subsection_count >= MIN_SUBSECTIONS else "partial",
            f"{subsection_count} subsections; target >= {MIN_SUBSECTIONS}",
            "" if subsection_count >= MIN_SUBSECTIONS else "Add dedicated subsections for fair-resolution comparison, mainstream YOLO comparison, scale analysis, failure cases, and limitations.",
        ),
        LengthCheck(
            "Table count",
            "ready" if table_count >= MIN_TABLES else "partial",
            f"{table_count} table environments; target >= {MIN_TABLES}",
            "" if table_count >= MIN_TABLES else "Add final fair-comparison and post-sync result tables after complete experiments are synced.",
        ),
        LengthCheck(
            "Figure count",
            "ready" if figure_count >= MIN_FIGURES else "partial",
            f"{figure_count} figure environments; target >= {MIN_FIGURES}",
            "" if figure_count >= MIN_FIGURES else "Add or retain method, scale, trade-off, qualitative, and failure-case figures.",
        ),
        LengthCheck(
            "Reference count",
            "ready" if reference_count >= MIN_REFERENCES else "partial",
            f"{reference_count} references; target >= {MIN_REFERENCES}",
            "" if reference_count >= MIN_REFERENCES else "Use only verified references from the reference matrix.",
        ),
    ]
    return checks


def write_report(checks: list[LengthCheck]) -> None:
    total = len(checks)
    ready = sum(1 for check in checks if check.status == "ready")
    partial = sum(1 for check in checks if check.status == "partial")
    missing = sum(1 for check in checks if check.status == "missing")

    lines = [
        "# Manuscript Length Audit",
        "",
        "This report is generated by `tools/check_manuscript_length.py`. It estimates the current LaTeX manuscript's length and structural density for the CEA journal-submission track. It does not judge scientific correctness or add experiment results.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Partial: {partial}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the manuscript meets the configured structural or length threshold.",
            "- `PARTIAL` means the manuscript is usable as a candidate draft but still needs journal-length expansion.",
            "- The character threshold is a local planning gate based on the CEA-oriented roadmap, not an official acceptance guarantee.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

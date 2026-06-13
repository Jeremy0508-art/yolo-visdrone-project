from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/tex_cross_reference_audit.md"


@dataclass
class CrossRefCheck:
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


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.S))


def labels_by_prefix(text: str, prefix: str) -> list[str]:
    return re.findall(rf"\\label\{{({re.escape(prefix)}:[^}}]+)\}}", text)


def refs(text: str) -> list[str]:
    found: list[str] = []
    for command in ["ref", "pageref", "autoref"]:
        for match in re.finditer(rf"\\{command}\{{([^}}]+)\}}", text):
            found.extend(item.strip() for item in match.group(1).split(",") if item.strip())
    return found


def caption_near_environment(text: str, env: str) -> list[tuple[int, bool, bool]]:
    pattern = re.compile(rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}", re.S)
    rows: list[tuple[int, bool, bool]] = []
    for match in pattern.finditer(text):
        start_line = text.count("\n", 0, match.start()) + 1
        body = match.group(1)
        rows.append((start_line, "\\caption" in body, "\\label" in body))
    return rows


def audit() -> list[CrossRefCheck]:
    if not TEX_PATH.exists():
        return [
            CrossRefCheck(
                "LaTeX source exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore or regenerate the LaTeX manuscript.",
            )
        ]

    text = TEX_PATH.read_text(encoding="utf-8")
    checks: list[CrossRefCheck] = []
    figure_labels = labels_by_prefix(text, "fig")
    table_labels = labels_by_prefix(text, "tab")
    all_labels = re.findall(r"\\label\{([^}]+)\}", text)
    ref_list = refs(text)
    ref_set = set(ref_list)

    duplicate_labels = sorted({label for label in all_labels if all_labels.count(label) > 1})
    undefined_refs = sorted(set(ref_list) - set(all_labels))
    unreferenced_figures = sorted(label for label in figure_labels if label not in ref_set)
    unreferenced_tables = sorted(label for label in table_labels if label not in ref_set)

    figure_envs = caption_near_environment(text, "figure")
    table_envs = caption_near_environment(text, "table")
    figure_missing_caption = [line for line, has_caption, _ in figure_envs if not has_caption]
    table_missing_caption = [line for line, has_caption, _ in table_envs if not has_caption]
    figure_missing_label = [line for line, _, has_label in figure_envs if not has_label]
    table_missing_label = [line for line, _, has_label in table_envs if not has_label]

    checks.extend(
        [
            CrossRefCheck(
                "Figure labels are referenced",
                "ready" if not unreferenced_figures else "partial",
                "all figure labels are referenced" if not unreferenced_figures else ", ".join(unreferenced_figures),
                "" if not unreferenced_figures else "Reference or remove unreferenced figure labels.",
            ),
            CrossRefCheck(
                "Table labels are referenced",
                "ready" if not unreferenced_tables else "partial",
                "all table labels are referenced" if not unreferenced_tables else ", ".join(unreferenced_tables),
                "" if not unreferenced_tables else "Reference or remove unreferenced table labels.",
            ),
            CrossRefCheck(
                "Undefined refs",
                "ready" if not undefined_refs else "missing",
                "all refs resolve to labels" if not undefined_refs else ", ".join(undefined_refs),
                "" if not undefined_refs else "Fix refs or add matching labels.",
            ),
            CrossRefCheck(
                "Duplicate labels",
                "ready" if not duplicate_labels else "missing",
                "no duplicate labels" if not duplicate_labels else ", ".join(duplicate_labels),
                "" if not duplicate_labels else "Rename duplicate labels.",
            ),
            CrossRefCheck(
                "Figure captions",
                "ready" if not figure_missing_caption else "missing",
                f"{len(figure_envs)} figure environments checked"
                if not figure_missing_caption
                else "missing caption at line " + ", ".join(map(str, figure_missing_caption)),
                "" if not figure_missing_caption else "Add captions to all figures.",
            ),
            CrossRefCheck(
                "Table captions",
                "ready" if not table_missing_caption else "missing",
                f"{len(table_envs)} table environments checked"
                if not table_missing_caption
                else "missing caption at line " + ", ".join(map(str, table_missing_caption)),
                "" if not table_missing_caption else "Add captions to all tables.",
            ),
            CrossRefCheck(
                "Figure labels",
                "ready" if not figure_missing_label else "missing",
                f"{len(figure_envs)} figure environments checked"
                if not figure_missing_label
                else "missing label at line " + ", ".join(map(str, figure_missing_label)),
                "" if not figure_missing_label else "Add labels to all figures.",
            ),
            CrossRefCheck(
                "Table labels",
                "ready" if not table_missing_label else "missing",
                f"{len(table_envs)} table environments checked"
                if not table_missing_label
                else "missing label at line " + ", ".join(map(str, table_missing_label)),
                "" if not table_missing_label else "Add labels to all tables.",
            ),
            CrossRefCheck(
                "Cross-reference density",
                "ready" if len(ref_list) >= len(figure_labels) + len(table_labels) else "partial",
                f"{len(ref_list)} refs for {len(figure_labels)} figures and {len(table_labels)} tables",
                "Ensure every important figure/table is discussed in the body.",
            ),
        ]
    )
    return checks


def write_report(checks: list[CrossRefCheck]) -> None:
    total = len(checks)
    ready = sum(1 for check in checks if check.status == "ready")
    partial = sum(1 for check in checks if check.status == "partial")
    missing = sum(1 for check in checks if check.status == "missing")

    lines = [
        "# LaTeX Cross-Reference Audit",
        "",
        "This report is generated by `tools/check_tex_cross_references.py`. It checks whether LaTeX figure and table labels are captioned, referenced, unique, and resolvable. It does not judge the scientific quality of the discussion.",
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
            "- `READY` means cross-reference structure is complete for this item.",
            "- `PARTIAL` means the manuscript can compile, but body discussion or reference density should be improved.",
            "- `MISSING` means a label, ref, or caption problem should be fixed before submission.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

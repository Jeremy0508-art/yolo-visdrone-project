from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/manuscript_journal_gap_audit.md"


@dataclass
class GapCheck:
    area: str
    item: str
    status: str
    evidence: str
    action: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.MULTILINE))


def contains(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def has_failure_case_analysis(text: str) -> bool:
    required_patterns = [
        r"\\label\{fig:failure\}",
        r"\\label\{tab:failure_reason\}",
        r"失败案例主要来自尺度、遮挡、类别边界和背景干扰",
    ]
    return all(contains(pattern, text) for pattern in required_patterns)


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "partial": "PARTIAL",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def audit() -> list[GapCheck]:
    if not TEX_PATH.exists():
        return [
            GapCheck(
                "Manuscript",
                "LaTeX source exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore or regenerate the LaTeX manuscript source.",
            )
        ]

    text = read_text(TEX_PATH)
    checks: list[GapCheck] = []

    section_count = count(r"\\section\{", text)
    subsection_count = count(r"\\subsection\{", text)
    table_count = count(r"\\begin\{table\}", text)
    figure_count = count(r"\\begin\{figure\}", text)
    citation_count = count(r"\\cite\{", text)
    bibitem_count = count(r"\\bibitem\{", text)

    checks.append(
        GapCheck(
            "Scale",
            "Journal-length section count",
            "partial" if section_count < 7 else "ready",
            f"{section_count} sections",
            "Expand into introduction, related work, method, experimental setup, results, discussion, and conclusion.",
        )
    )
    checks.append(
        GapCheck(
            "Scale",
            "Subsection density",
            "ready" if subsection_count >= 12 else "partial",
            f"{subsection_count} subsections",
            "Add finer subsections for fair-resolution comparison, mainstream YOLO comparison, discussion, and limitations.",
        )
    )
    checks.append(
        GapCheck(
            "Evidence",
            "Table count",
            "ready" if table_count >= 7 else "partial",
            f"{table_count} table environments",
            "Target at least dataset/config, main results, fair-resolution, ablation, scale analysis, per-class, and speed tables.",
        )
    )
    checks.append(
        GapCheck(
            "Evidence",
            "Figure count",
            "ready" if figure_count >= 5 else "partial",
            f"{figure_count} figure environments",
            "Use method, scale distribution, training/PR, trade-off, qualitative, and failure-case figures.",
        )
    )
    checks.append(
        GapCheck(
            "References",
            "Citation density",
            "ready" if bibitem_count >= 25 else "partial",
            f"{citation_count} citation commands, {bibitem_count} bibitem entries",
            "Increase verified references before final submission; target 25-35 bibliography entries.",
        )
    )

    required_sections = [
        ("Introduction", r"\\section\{引言\}", "ready", "Keep and expand the introduction."),
        ("Related work", r"\\section\{相关工作\}", "ready", "Keep and expand related work."),
        ("Method", r"\\section\{方法\}", "ready", "Keep and expand method details."),
        ("Experiments", r"\\section\{实验", "ready", "Split experimental setup and result analysis in the journal draft."),
        ("Discussion", r"\\section\{讨论\}", "ready", "Add a discussion section after result analysis."),
        ("Conclusion", r"\\section\{结论\}", "ready", "Rewrite conclusion after fair experiments finish."),
    ]
    for item, pattern, ok_status, action in required_sections:
        found = contains(pattern, text)
        checks.append(
            GapCheck(
                "Structure",
                item,
                ok_status if found else "missing",
                "found" if found else "not found",
                "" if found else action,
            )
        )

    expected_topics = [
        ("Fair-resolution comparison", r"分辨率公平|公平分辨率|YOLO11n-960|YOLO11n-P2-960", "pending", "pending", "Write after server 100-epoch fair experiments are synced."),
        ("Mainstream YOLO comparison", r"YOLOv5n|YOLOv8n|YOLO11s", "partial", "missing", "Complete after YOLOv5n and 960 baselines finish."),
        ("Scale-group analysis", r"尺度分组|small|medium|large", "ready", "missing", "Keep scale-group metric definition explicit."),
        ("Speed-complexity trade-off", r"FPS|推理速度|复杂度|Latency|延迟", "ready", "missing", "Update after new server models are benchmarked."),
        ("Official test-dev boundary", r"test-dev|官方", "ready", "missing", "Keep wording clear that no official AP is available yet."),
    ]
    for item, pattern, if_found_status, if_missing_status, action in expected_topics:
        found = contains(pattern, text)
        checks.append(
            GapCheck(
                "Content",
                item,
                if_found_status if found else if_missing_status,
                "mentioned" if found else "not mentioned",
                action,
            )
        )

    failure_ready = has_failure_case_analysis(text)
    failure_mentioned = contains(r"失败|漏检|误检|混淆|遮挡", text)
    checks.append(
        GapCheck(
            "Content",
            "Failure-case analysis",
            "ready" if failure_ready else ("partial" if failure_mentioned else "missing"),
            "figure, table, and attribution paragraph found" if failure_ready else ("mentioned" if failure_mentioned else "not mentioned"),
            "" if failure_ready else "Expand qualitative cases into categorized failure analysis.",
        )
    )

    return checks


def write_report(checks: list[GapCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# Journal Manuscript Gap Audit",
        "",
        "This report is generated by `tools/check_journal_manuscript_gaps.py`. It compares the current LaTeX candidate with the journal-manuscript blueprint and records structural gaps. It does not validate new experiment results.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Partial: {partial}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in checks:
        lines.append(
            f"| {c.area} | {c.item} | {status_symbol(c.status)} | `{c.evidence}` | {c.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the current manuscript already contains enough structure for this item at the present stage.",
            "- `PARTIAL` means the item exists but needs expansion for a journal-length paper.",
            "- `PENDING` means the item depends on completed fair-comparison experiments.",
            "- `MISSING` means the current LaTeX candidate lacks the expected structure or discussion.",
            "",
            "The current LaTeX file should be treated as a candidate draft, not the final journal manuscript, until the missing and partial items are resolved after fair experiments finish.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

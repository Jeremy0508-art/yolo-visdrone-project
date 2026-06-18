from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "paper/cea_template_migration/manuscript_cea_template_draft.docx"
REPORT_PATH = ROOT / "paper/cea_template_migration/cea_word_draft_quality_audit.md"


@dataclass(frozen=True)
class Check:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {"ready": "READY", "partial": "PARTIAL", "pending": "PENDING", "missing": "MISSING"}[status]


def read_docx_text() -> tuple[str, int, int, list[int], bool]:
    if not DOCX_PATH.exists():
        return "", 0, 0, [], False
    try:
        with zipfile.ZipFile(DOCX_PATH) as archive:
            document = archive.read("word/document.xml")
            root = ET.fromstring(document)
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            paragraphs: list[str] = []
            for para in root.findall(".//w:p", ns):
                parts = [node.text for node in para.findall(".//w:t", ns) if node.text]
                if parts:
                    paragraphs.append("".join(parts))
            table_count = len(root.findall(".//w:tbl", ns))
            media_count = len([name for name in archive.namelist() if name.startswith("word/media/")])
            section_cols: list[int] = []
            for sect in root.findall(".//w:sectPr", ns):
                cols = sect.find("w:cols", ns)
                if cols is None:
                    section_cols.append(1)
                    continue
                raw = cols.attrib.get(f"{{{ns['w']}}}num")
                section_cols.append(int(raw) if raw else 1)
        return "\n".join(paragraphs), table_count, media_count, section_cols, True
    except Exception as exc:  # pragma: no cover - report generation path
        return f"ERROR: {exc}", 0, 0, [], False


def count_cjk(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def extract_between(text: str, start: str, end: str) -> str:
    s = text.find(start)
    if s < 0:
        return ""
    s += len(start)
    e = text.find(end, s)
    if e < 0:
        return text[s:].strip()
    return text[s:e].strip()


def audit() -> list[Check]:
    text, table_count, media_count, section_cols, valid = read_docx_text()
    checks: list[Check] = [
        Check(
            "CEA Word draft exists",
            "ready" if DOCX_PATH.exists() else "missing",
            str(DOCX_PATH.relative_to(ROOT)) if DOCX_PATH.exists() else "missing",
            "" if DOCX_PATH.exists() else "Run python tools/build_cea_word_draft.py.",
        ),
        Check(
            "DOCX package is readable",
            "ready" if valid else "missing",
            "word/document.xml parsed" if valid else text,
            "" if valid else "Regenerate the Word draft.",
        ),
    ]
    if not valid:
        return checks

    paragraphs = [line.strip() for line in text.splitlines() if line.strip()]
    title = paragraphs[0] if paragraphs else ""
    title_cjk = count_cjk(title)
    checks.append(
        Check(
            "Chinese title length",
            "ready" if title and title_cjk <= 25 else "partial",
            f"{title_cjk} Chinese characters; title=`{title}`",
            "" if title and title_cjk <= 25 else "Shorten the title to match the CEA template recommendation.",
        )
    )

    checks.append(
        Check(
            "CEA section layout",
            "ready" if section_cols[:2] == [1, 2] else "partial",
            f"section columns={section_cols}",
            "" if section_cols[:2] == [1, 2] else "Use single-column front matter and two-column main text.",
        )
    )

    abstract = extract_between(text, "摘  要：", "关键词：")
    abstract_cjk = count_cjk(abstract)
    checks.append(
        Check(
            "Chinese abstract length",
            "ready" if 240 <= abstract_cjk <= 380 else "partial",
            f"{abstract_cjk} Chinese characters",
            "" if 240 <= abstract_cjk <= 380 else "Compress the abstract toward the CEA template's about-300-character recommendation.",
        )
    )

    keywords = extract_between(text, "关键词：", "文献标志码：")
    keyword_items = [item.strip() for item in re.split(r"[；;]", keywords) if item.strip()]
    checks.append(
        Check(
            "Chinese keywords",
            "ready" if 3 <= len(keyword_items) <= 8 else "partial",
            f"{len(keyword_items)} keywords: {', '.join(keyword_items)}",
            "" if 3 <= len(keyword_items) <= 8 else "Keep 3-8 keywords separated by semicolons.",
        )
    )

    english_abstract = extract_between(text, "Abstract: ", "Key words:")
    checks.append(
        Check(
            "English abstract present",
            "ready" if len(english_abstract.split()) >= 80 else "partial",
            f"{len(english_abstract.split())} English words",
            "" if len(english_abstract.split()) >= 80 else "Review and complete the English abstract.",
        )
    )

    chinese_tables = len(re.findall(r"表[0-9]+", text))
    english_tables = len(re.findall(r"Table [0-9]+", text))
    checks.append(
        Check(
            "Bilingual table captions",
            "ready" if chinese_tables >= 10 and english_tables >= 10 and table_count == 10 else "partial",
            f"{chinese_tables} Chinese table captions, {english_tables} English table captions, {table_count} Word tables",
            "" if chinese_tables >= 10 and english_tables >= 10 and table_count == 10 else "Check table captions and parsed Word tables.",
        )
    )

    chinese_figures = len(re.findall(r"图[0-9]+", text))
    english_figures = len(re.findall(r"Fig\.[0-9]+", text))
    checks.append(
        Check(
            "Bilingual figure captions",
            "ready" if chinese_figures >= 6 and english_figures >= 6 else "partial",
            f"{chinese_figures} Chinese figure captions, {english_figures} English figure captions, {media_count} media files",
            "" if chinese_figures >= 6 and english_figures >= 6 else "Check figure captions and embedded images.",
        )
    )

    reference_section = text.split("参考文献:", 1)[-1] if "参考文献:" in text else ""
    ref_count = len(re.findall(r"^\[[0-9]+\]", reference_section, flags=re.M))
    checks.append(
        Check(
            "Reference count",
            "ready" if ref_count >= 20 else "partial",
            f"{ref_count} numbered references",
            "" if ref_count >= 20 else "CEA template recommends 20 or more references.",
        )
    )

    broken_tokens = [token for token in ["YOLO11n-P2Nine", "YOLO11n-P2CANine", "待补充", "TODO"] if token in text]
    checks.append(
        Check(
            "Broken migration tokens",
            "ready" if not broken_tokens else "missing",
            "none" if not broken_tokens else ", ".join(broken_tokens),
            "" if not broken_tokens else "Fix LaTeX macro conversion or unfinished placeholders.",
        )
    )

    internal_notes = [token for token in ["引言部分按", "机械审计", "内部说明"] if token in text]
    checks.append(
        Check(
            "Internal notes removed from manuscript text",
            "ready" if not internal_notes else "partial",
            "none" if not internal_notes else ", ".join(internal_notes),
            "" if not internal_notes else "Move workflow notes out of the Word manuscript body.",
        )
    )

    author_placeholders = [token for token in ["待导师确认", "待确认", "to be confirmed"] if token in text]
    checks.append(
        Check(
            "Author metadata placeholders",
            "pending" if author_placeholders else "ready",
            ", ".join(author_placeholders) if author_placeholders else "no placeholders detected",
            "Replace placeholders after user/advisor confirms author, affiliation, email, phone, address, funding, acknowledgements, and declarations."
            if author_placeholders
            else "",
        )
    )
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for check in checks if check.status == "ready")
    partial = sum(1 for check in checks if check.status == "partial")
    pending = sum(1 for check in checks if check.status == "pending")
    missing = sum(1 for check in checks if check.status == "missing")
    lines = [
        "# CEA Word Draft Quality Audit",
        "",
        "This report is generated by `tools/check_cea_word_draft.py`. It checks whether the first-pass CEA Word migration draft satisfies basic template-facing requirements. It is a mechanical audit, not a substitute for visual inspection in Word/WPS.",
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
            "- `READY` means the mechanical check passes.",
            "- `PARTIAL` means the draft exists but should be improved for CEA formatting quality.",
            "- `PENDING` means user/advisor metadata or manual visual review is still required.",
            "- `MISSING` means the Word draft or a required content element is absent.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

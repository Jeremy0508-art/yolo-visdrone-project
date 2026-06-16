from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md"


@dataclass
class SourceItem:
    sid: str
    source: str
    url: str
    authority: str
    use: str
    manual_check: str


@dataclass
class OnlineCheck:
    cid: str
    source_id: str
    date: str
    result: str
    implication: str


SOURCES = [
    SourceItem(
        "S1",
        "CEA official template/download column candidate",
        "https://cea.ceaj.org/CN/column/column18.shtml",
        "official-candidate",
        "Use as the first place to verify the current writing template, download center, and submission instructions.",
        "Open manually before final submission and record the current template file, date, and required upload format.",
    ),
    SourceItem(
        "S2",
        "CEA editorial-office homepage candidate",
        "https://jsjgcyyy.juqk.net/",
        "official-candidate",
        "Use as a secondary route to confirm template, author submission entrance, and notices if the main official site is unavailable.",
        "Confirm that the site is the current editorial-office page before using any instruction from it.",
    ),
    SourceItem(
        "S3",
        "CEA submission notice candidate",
        "https://jsjgcyyy.juqk.net/buy/",
        "official-candidate",
        "Use only for manually checking submission notices, template reminders, originality/author responsibility wording, and system instructions.",
        "Do not copy requirements into the manuscript package until the page is manually verified near submission time.",
    ),
    SourceItem(
        "S4",
        "CCF WISA page mentioning CEA template URL",
        "https://ccf.org.cn/WISA2025/general_3015",
        "cross-reference",
        "Use only as supporting evidence that the CEA template URL may be used by a related Chinese-paper workflow.",
        "Do not treat conference page requirements as CEA journal requirements.",
    ),
    SourceItem(
        "S5",
        "Third-party CEA guide pages",
        "not fixed",
        "third-party",
        "Use only as weak background for common submission-process questions.",
        "Never treat third-party fee, cycle, template, or formatting claims as authoritative without official-site confirmation.",
    ),
]

ONLINE_CHECKS = [
    OnlineCheck(
        "C1",
        "S1",
        "2026-06-16",
        "Direct open attempt for `https://cea.ceaj.org/CN/column/column18.shtml` returned an unavailable/502-style result from this environment.",
        "Do not assume the current local manuscript matches the official CEA template; manual browser download remains required.",
    ),
    OnlineCheck(
        "C2",
        "S2",
        "2026-06-16",
        "Web search found `https://jsjgcyyy.juqk.net/` with CEA editorial-office/homepage wording and author-contact reminders.",
        "Use only as a source candidate until the user or advisor confirms it is the current official editorial-office route.",
    ),
    OnlineCheck(
        "C3",
        "S3",
        "2026-06-16",
        "Web search found `https://jsjgcyyy.juqk.net/buy/` with submission-notice snippets including column/category and manuscript requirement wording.",
        "Record as a manual-check lead, not as final upload-format evidence.",
    ),
    OnlineCheck(
        "C4",
        "S4",
        "2026-06-16",
        "CCF WISA search result mentions the CEA template URL `http://cea.ceaj.org/CN/column/column18.shtml` for Chinese paper formatting.",
        "This cross-reference supports the template URL as a lead but cannot define CEA journal submission requirements.",
    ),
    OnlineCheck(
        "C5",
        "S5",
        "2026-06-16",
        "Search results include multiple third-party guide or journal-info pages with fees, contact details, and template claims.",
        "Treat third-party pages as non-authoritative background only; do not copy their fee, schedule, or formatting claims into the submission package.",
    ),
]

MANUAL_FIELDS = [
    ("M1", "Template file", "Current official Word/LaTeX/PDF template file name, version/date, and download URL."),
    ("M2", "Upload file type", "Whether initial submission requires Word, PDF, source package, figures, or separate attachment files."),
    ("M3", "Author metadata", "Required author names, affiliations, corresponding author marker, email, phone, ORCID, postal address, and author order rules."),
    ("M4", "Declarations", "Required funding, acknowledgement, conflict-of-interest, data availability, ethics, copyright, or originality statements."),
    ("M5", "Length and format", "Required word/page count, Chinese/English title, abstracts, keywords, section style, figure/table style, and reference style."),
    ("M6", "Submission-system behavior", "Whether uploaded manuscripts can be replaced after submission and what manuscript ID/contact process is used."),
    ("M7", "Fees and attachments", "Any review fee, page fee, copyright transfer, membership discount, or signed document requirements."),
]


def write_report() -> None:
    lines = [
        "# CEA Official Requirements Tracker",
        "",
        "This file is generated by `tools/build_cea_official_requirements_tracker.py`.",
        "",
        "It tracks external requirement sources for the `Computer Engineering and Applications` submission route. Because journal websites and submission systems can change, this file records what must be manually verified before final upload. It is not itself proof of current official requirements.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(SOURCES) + len(MANUAL_FIELDS)}",
        f"- Ready: {len(SOURCES)}",
        f"- Pending: {len(MANUAL_FIELDS)}",
        "- Missing: 0",
        "",
        "## Source Candidates",
        "",
        "| ID | Source | URL | Authority | Use | Manual check |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in SOURCES:
        lines.append(
            f"| {item.sid} | {item.source} | `{item.url}` | {item.authority} | {item.use} | {item.manual_check} |"
        )

    lines.extend(
        [
            "",
            "## Latest Online Check Note",
            "",
            "- Current date for this workspace: 2026-06-16.",
            "- Web search finds the editorial-office candidate page `https://jsjgcyyy.juqk.net/` and related submission notice candidate `https://jsjgcyyy.juqk.net/buy/`, but direct page access from this environment is unstable.",
            "- Direct access to `https://cea.ceaj.org/CN/column/column18.shtml` returned an unavailable/502-style result in this environment; do not assume the local package matches the current official template until a browser/manual download confirms it.",
            "- Search snippets indicate author-contact information and column/category requirement reminders, but snippets are not sufficient evidence for final upload format.",
            "- Keep all official-template and upload-format fields as PENDING until the final submission-system check is performed.",
            "",
            "## Online Check Log",
            "",
            "| ID | Source ID | Date | Result | Implication |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in ONLINE_CHECKS:
        lines.append(f"| {item.cid} | {item.source_id} | {item.date} | {item.result} | {item.implication} |")

    lines.extend(
        [
            "",
            "## Manual Requirement Fields",
            "",
            "| ID | Field | What to record before final upload | Status |",
            "| --- | --- | --- | --- |",
        ]
    )
    for mid, field, note in MANUAL_FIELDS:
        lines.append(f"| {mid} | {field} | {note} | PENDING |")

    lines.extend(
        [
            "",
            "## Use Rule",
            "",
            "- Official-candidate pages should be opened and checked manually close to the actual submission date.",
            "- Cross-reference pages can help locate a template URL but cannot define journal requirements.",
            "- Third-party pages are not authoritative and should not be cited as final submission rules.",
            "- Final manuscript and package changes must be made only after the official template/upload requirements are confirmed.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_report()
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

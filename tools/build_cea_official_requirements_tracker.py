from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md"
TEMPLATE_DIR = ROOT / "paper/templates"
TEMPLATE_SUMMARY = ROOT / "paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md"
OFFICIAL_REQUIREMENTS_URL = "http://cea.ceaj.org/CN/column/column16.shtml"


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


@dataclass
class ManualField:
    mid: str
    field: str
    note: str
    status: str


def find_template() -> Path | None:
    files = sorted(TEMPLATE_DIR.glob("*.docx"))
    return files[0] if files else None


def file_size_note(path: Path) -> str:
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def template_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SOURCES = [
    SourceItem(
        "S1",
        "CEA official submission requirements page provided by user",
        OFFICIAL_REQUIREMENTS_URL,
        "official-candidate",
        "Use as the first place to verify current submission requirements, writing template, and upload instructions.",
        "Open manually in a browser before final submission; direct access from the current tool environment may be unstable.",
    ),
    SourceItem(
        "S2",
        "CEA official template/download column candidate from earlier workflow",
        "https://cea.ceaj.org/CN/column/column18.shtml",
        "official-candidate",
        "Keep as a secondary official-site lead for template/download checks if linked by the journal site.",
        "Do not treat it as current unless the journal page or submission system points to it near submission time.",
    ),
    SourceItem(
        "S3",
        "CEA editorial-office homepage candidate",
        "https://jsjgcyyy.juqk.net/",
        "official-candidate",
        "Use as a secondary route to confirm template, author submission entrance, and notices if the main official site is unavailable.",
        "Confirm that the site is the current editorial-office page before using any instruction from it.",
    ),
    SourceItem(
        "S4",
        "CEA submission notice candidate",
        "https://jsjgcyyy.juqk.net/buy/",
        "official-candidate",
        "Use only for manually checking submission notices, template reminders, originality/author responsibility wording, and system instructions.",
        "Do not copy requirements into the manuscript package until the page is manually verified near submission time.",
    ),
    SourceItem(
        "S5",
        "CCF WISA page mentioning CEA template URL",
        "https://ccf.org.cn/WISA2025/general_3015",
        "cross-reference",
        "Use only as supporting evidence that a CEA template URL may be used by a related Chinese-paper workflow.",
        "Do not treat conference page requirements as CEA journal requirements.",
    ),
    SourceItem(
        "S6",
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
        "2026-06-18",
        f"Browser-like request returned HTTP 200 for `{OFFICIAL_REQUIREMENTS_URL}` with page title `计算机工程与应用 投稿指南`; the guide was mechanically summarized into this tracker.",
        "The official guide confirms the paper should follow the writing template, use online author submission, provide ordered author/contact metadata, and treat post-submission manuscript updates cautiously; the exact upload package still requires final system confirmation.",
    ),
    OnlineCheck(
        "C2",
        "S2",
        "2026-06-16",
        "Direct open attempt for `https://cea.ceaj.org/CN/column/column18.shtml` returned an unavailable/502-style result from this environment.",
        "Keep this URL as an official-site lead only; do not assume it is the current template page.",
    ),
    OnlineCheck(
        "C3",
        "S3",
        "2026-06-16",
        "Web search found `https://jsjgcyyy.juqk.net/` with CEA editorial-office/homepage wording and author-contact reminders.",
        "Use only as a source candidate until the user or advisor confirms it is the current official editorial-office route.",
    ),
    OnlineCheck(
        "C4",
        "S4",
        "2026-06-16",
        "Web search found `https://jsjgcyyy.juqk.net/buy/` with submission-notice snippets including column/category and manuscript requirement wording.",
        "Record as a manual-check lead, not as final upload-format evidence.",
    ),
    OnlineCheck(
        "C5",
        "S5",
        "2026-06-16",
        "CCF WISA search result mentions the CEA template URL `http://cea.ceaj.org/CN/column/column18.shtml` for Chinese paper formatting.",
        "This cross-reference supports the template URL as a lead but cannot define CEA journal submission requirements.",
    ),
    OnlineCheck(
        "C6",
        "S6",
        "2026-06-16",
        "Search results include multiple third-party guide or journal-info pages with fees, contact details, and template claims.",
        "Treat third-party pages as non-authoritative background only; do not copy their fee, schedule, or formatting claims into the submission package.",
    ),
]

def build_manual_fields() -> list[ManualField]:
    template = find_template()
    template_ready = template is not None and TEMPLATE_SUMMARY.exists()
    return [
        ManualField(
            "M1",
            "Template file",
            "Current CEA Word template has been copied into `paper/templates/` and summarized in `paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md`.",
            "READY" if template_ready else "PENDING",
        ),
        ManualField(
            "M2",
            "Upload file type",
            "The guide points authors to online submission and the writing template, but the exact upload package--Word, PDF, source package, figures, or attachments--must still be checked in the submission system.",
            "PENDING",
        ),
        ManualField(
            "M3",
            "Author metadata",
            "The guide requires ordered author entry and detailed contact information; final author names, affiliations, corresponding author, email, phone, postal address, and optional ORCID still need user/advisor confirmation.",
            "PENDING",
        ),
        ManualField(
            "M4",
            "Declarations",
            "The guide emphasizes originality, no duplicate submission, intellectual-property responsibility, confidentiality handling, copyright transfer after acceptance, and CCF membership marking when applicable; project-specific funding, acknowledgement, conflict-of-interest, data availability, and originality wording still need confirmation.",
            "PENDING",
        ),
        ManualField(
            "M5",
            "Length and format",
            "The guide recommends general papers be over 7500 Chinese characters and records title, author, unit, abstract, keywords, funding, classification number, body, references, and author bio requirements; the local template summary records detailed figure/table/body-layout requirements.",
            "READY" if template_ready else "PENDING",
        ),
        ManualField(
            "M6",
            "Submission-system behavior",
            "The guide states author order and metadata should be checked before upload and that successful submission does not provide a manuscript update function; still verify the live system behavior before final upload.",
            "PENDING",
        ),
        ManualField(
            "M7",
            "Fees and attachments",
            "The guide gives review/page-fee, copyright-transfer, and CCF-discount notes, but fee standards and required signed files should be confirmed again near submission.",
            "PENDING",
        ),
    ]


def write_report() -> None:
    template = find_template()
    manual_fields = build_manual_fields()
    ready = len(SOURCES) + sum(1 for item in manual_fields if item.status == "READY")
    pending = sum(1 for item in manual_fields if item.status == "PENDING")
    lines = [
        "# CEA Official Requirements Tracker",
        "",
        "This file is generated by `tools/build_cea_official_requirements_tracker.py`.",
        "",
        "It tracks external requirement sources for the `Computer Engineering and Applications` submission route. Because journal websites and submission systems can change, this file records what must be manually verified before final upload. It is not itself proof of current official requirements.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(SOURCES) + len(manual_fields)}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
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
            "- Current date for this workspace: 2026-06-18.",
            f"- The official submission-guide URL `{OFFICIAL_REQUIREMENTS_URL}` was reachable with a browser-like request and returned the page title `计算机工程与应用 投稿指南`.",
            "- The guide confirms a template-based academic-paper format, online author submission, ordered author metadata, detailed contact information, originality/copyright responsibilities, and post-submission caution about manuscript updates.",
            "- The uploaded local Word template remains the concrete formatting source for the manuscript draft; the live submission system still needs manual confirmation for accepted upload file types and attachments.",
            "- Because journal pages can change, these notes should be checked again in a browser immediately before final submission.",
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
            "## Local Template Evidence",
            "",
            "| Field | Value |",
            "| --- | --- |",
        ]
    )
    if template is None:
        lines.append("| Local template | MISSING |")
    else:
        lines.extend(
            [
                f"| Local template | `{template.relative_to(ROOT).as_posix()}` |",
                f"| Size | {file_size_note(template)} |",
                f"| SHA256 | `{template_hash(template)}` |",
                f"| Requirement summary | `paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md` |",
            ]
        )

    lines.extend(
        [
            "",
            "## Manual Requirement Fields",
            "",
            "| ID | Field | What to record before final upload | Status |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in manual_fields:
        lines.append(f"| {item.mid} | {item.field} | {item.note} | {item.status} |")

    lines.extend(
        [
            "",
            "## Use Rule",
            "",
            "- Official-candidate pages should be opened and checked manually close to the actual submission date.",
            "- Cross-reference pages can help locate a template URL but cannot define journal requirements.",
            "- Third-party pages are not authoritative and should not be cited as final submission rules.",
            "- Final manuscript and package changes must be made only after the official template/upload requirements are manually verified in the journal system.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_report()
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

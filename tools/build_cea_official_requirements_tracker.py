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
        f"User provided the official submission-requirements link `{OFFICIAL_REQUIREMENTS_URL}` and uploaded the Word template `paper/templates/计算机工程与应用论文模版.docx`.",
        "The local package now has a concrete template file to migrate into, but the upload-system file type and final browser verification remain manual gates.",
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
            "Whether initial submission requires Word, PDF, source package, figures, or separate attachment files.",
            "PENDING",
        ),
        ManualField(
            "M3",
            "Author metadata",
            "Required author names, affiliations, corresponding author marker, email, phone, ORCID, postal address, and author order rules.",
            "PENDING",
        ),
        ManualField(
            "M4",
            "Declarations",
            "Required funding, acknowledgement, conflict-of-interest, data availability, ethics, copyright, or originality statements.",
            "PENDING",
        ),
        ManualField(
            "M5",
            "Length and format",
            "Template summary records title, abstract, keyword, figure, table, body-layout, reference, and contact-detail requirements; final migrated manuscript still needs manual verification.",
            "READY" if template_ready else "PENDING",
        ),
        ManualField(
            "M6",
            "Submission-system behavior",
            "Whether uploaded manuscripts can be replaced after submission and what manuscript ID/contact process is used.",
            "PENDING",
        ),
        ManualField(
            "M7",
            "Fees and attachments",
            "Any review fee, page fee, copyright transfer, membership discount, or signed document requirements.",
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
            f"- The user provided the official submission-requirements link `{OFFICIAL_REQUIREMENTS_URL}` and uploaded the Word template now stored under `paper/templates/`.",
            "- Direct browser/tool access to the official site may still be unstable in this environment, so final upload format and submission-system behavior remain manual gates.",
            "- The local template evidence is enough to start template migration, but it does not prove the submission system will accept a specific file package.",
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

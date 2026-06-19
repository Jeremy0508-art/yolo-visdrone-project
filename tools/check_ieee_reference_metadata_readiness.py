from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "paper/ieee_trans/references_seed.bib"
CITATION_PLAN_PATH = ROOT / "paper/ieee_trans/citation_plan.md"
GAP_REPORT_PATH = ROOT / "paper/ieee_reference_gap_report.md"
REPORT_PATH = ROOT / "paper/ieee_reference_metadata_readiness_audit.md"


ENTRY_HEADER_RE = re.compile(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.M)
FIELD_RE = re.compile(r"^\s*(?P<field>[A-Za-z]+)\s*=\s*[\{\"](?P<value>.*?)[\}\"]\s*,?\s*$")


@dataclass(frozen=True)
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_bib(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    matches = list(ENTRY_HEADER_RE.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        fields: dict[str, str] = {}
        for line in body.splitlines():
            field_match = FIELD_RE.match(line.strip())
            if field_match:
                fields[field_match.group("field").lower()] = field_match.group("value").strip()
        entries.append(BibEntry(match.group("type").lower(), match.group("key"), fields))
    return entries


def has_url_like(entry: BibEntry) -> bool:
    joined = " ".join(entry.fields.values())
    return "\\url{" in joined or "http://" in joined or "https://" in joined


def has_identifier(entry: BibEntry) -> bool:
    return "doi" in entry.fields or "eprint" in entry.fields or has_url_like(entry)


def has_core_fields(entry: BibEntry) -> bool:
    if not {"author", "title"} <= set(entry.fields):
        return False
    if "year" in entry.fields:
        return True
    return entry.entry_type == "misc" and has_url_like(entry) and "note" in entry.fields


def check_bib_structure(entries: list[BibEntry], text: str) -> list[Check]:
    checks: list[Check] = []
    keys = [entry.key for entry in entries]
    duplicates = sorted(key for key, count in Counter(keys).items() if count > 1)
    checks.append(
        Check(
            "Structure",
            "Seed bibliography exists",
            "ready" if text else "missing",
            "paper/ieee_trans/references_seed.bib",
            "" if text else "Restore the seed bibliography.",
        )
    )
    checks.append(
        Check(
            "Structure",
            "Entry count",
            "ready" if len(entries) >= 20 else "pending",
            f"{len(entries)} entries",
            "" if len(entries) >= 20 else "Add missing dataset, method, and recent-work references.",
        )
    )
    checks.append(
        Check(
            "Structure",
            "Duplicate keys absent",
            "ready" if not duplicates else "missing",
            "none" if not duplicates else ", ".join(duplicates),
            "" if not duplicates else "Rename duplicate BibTeX keys.",
        )
    )
    return checks


def check_required_fields(entries: list[BibEntry]) -> list[Check]:
    checks: list[Check] = []
    missing_core = [
        entry.key
        for entry in entries
        if not has_core_fields(entry)
    ]
    checks.append(
        Check(
            "Fields",
            "All entries have core bibliographic fields",
            "ready" if not missing_core else "missing",
            "none" if not missing_core else ", ".join(missing_core),
            "" if not missing_core else "Add author/title and year or accessed online-resource metadata.",
        )
    )

    type_requirements = {
        "article": ["journal"],
        "inproceedings": ["booktitle"],
        "misc": [],
    }
    for entry_type, required in type_requirements.items():
        bad = [
            entry.key
            for entry in entries
            if entry.entry_type == entry_type and not set(required) <= set(entry.fields)
        ]
        if entry_type == "misc":
            bad = [
                entry.key
                for entry in entries
                if entry.entry_type == entry_type and not ("note" in entry.fields or has_identifier(entry))
            ]
        checks.append(
            Check(
                "Fields",
                "misc entries have note or durable identifier"
                if entry_type == "misc"
                else f"{entry_type} entries have {', '.join(required)}",
                "ready" if not bad else "missing",
                "none" if not bad else ", ".join(bad),
                "" if not bad else f"Complete required fields for {entry_type} entries.",
            )
        )

    no_identifier = [entry.key for entry in entries if not has_identifier(entry)]
    checks.append(
        Check(
            "Fields",
            "Entries have DOI, arXiv eprint, or URL where available",
            "ready" if not no_identifier else "pending",
            "none" if not no_identifier else ", ".join(no_identifier),
            "" if not no_identifier else "Before final references.bib, check publisher metadata and add DOI/URL/eprint where available.",
        )
    )
    return checks


def check_reference_roles(entries: list[BibEntry]) -> list[Check]:
    keys = {entry.key for entry in entries}
    groups = {
        "Primary datasets": [
            "du2019visdrone_det",
            "visdrone_dataset_repo",
            "du2018uavdt",
            "uavdt_project_page",
        ],
        "Feature pyramid/fusion": ["lin2017fpn", "liu2018panet", "tan2020efficientdet"],
        "Attention": ["hou2021coordinate_attention"],
        "Tiny/aerial datasets": [
            "wang2021aitod",
            "xu2022aitodv2_nwd",
            "bozcan2020auair",
            "yu2020tinyperson",
            "suo2023hituav",
        ],
        "Recent UAV/YOLO methods": [
            "li2024sod_yolo",
            "qu2025sma_yolo",
            "lu2025masf_yolo",
            "xu2025srtsod_yolo",
            "khalili2024sod_yolov8",
        ],
    }
    checks: list[Check] = []
    for group, required_keys in groups.items():
        missing = [key for key in required_keys if key not in keys]
        checks.append(
            Check(
                "Coverage",
                group,
                "ready" if not missing else "missing",
                "all required keys present" if not missing else ", ".join(missing),
                "" if not missing else "Add these seed references before related-work drafting.",
            )
        )

    recent_count = sum(1 for entry in entries if int(entry.fields.get("year", "0") or 0) >= 2024)
    checks.append(
        Check(
            "Coverage",
            "Recent 2024+ method/context references",
            "ready" if recent_count >= 5 else "pending",
            f"{recent_count} entries from 2024 or later",
            "" if recent_count >= 5 else "Add more recent UAV/YOLO small-object references.",
        )
    )
    return checks


def check_planning_links(entries: list[BibEntry]) -> list[Check]:
    keys = {entry.key for entry in entries}
    citation_plan = read_text(CITATION_PLAN_PATH)
    gap_report = read_text(GAP_REPORT_PATH)
    checks = [
        Check(
            "Planning",
            "Citation plan exists",
            "ready" if citation_plan else "missing",
            "paper/ieee_trans/citation_plan.md",
            "" if citation_plan else "Restore citation plan.",
        ),
        Check(
            "Planning",
            "Reference gap report exists",
            "ready" if gap_report else "missing",
            "paper/ieee_reference_gap_report.md",
            "" if gap_report else "Restore reference gap report.",
        ),
    ]

    missing_in_plan = sorted(key for key in keys if key not in citation_plan)
    checks.append(
        Check(
            "Planning",
            "Seed keys are represented in citation plan",
            "ready" if not missing_in_plan else "pending",
            "all seed keys found" if not missing_in_plan else ", ".join(missing_in_plan),
            "" if not missing_in_plan else "Map these seed keys to manuscript roles or mark them optional.",
        )
    )

    checks.append(
        Check(
            "Planning",
            "Final metadata verification remains explicit",
            "ready" if "verify publisher metadata" in citation_plan.lower() or "publisher metadata" in gap_report.lower() else "missing",
            "publisher metadata verification mentioned",
            "Keep final reference verification as an explicit manual gate.",
        )
    )
    return checks


def check_text_hygiene(text: str) -> list[Check]:
    forbidden = ["TODO", "待补充", "\ufffe", "�"]
    hits = [token for token in forbidden if token in text]
    return [
        Check(
            "Hygiene",
            "No placeholders or replacement characters in seed BibTeX",
            "ready" if not hits else "missing",
            "none" if not hits else ", ".join(hits),
            "" if not hits else "Remove placeholder or corrupted characters from references_seed.bib.",
        )
    ]


def audit() -> list[Check]:
    text = read_text(BIB_PATH)
    entries = parse_bib(text)
    checks: list[Check] = []
    checks.extend(check_bib_structure(entries, text))
    checks.extend(check_required_fields(entries))
    checks.extend(check_reference_roles(entries))
    checks.extend(check_planning_links(entries))
    checks.extend(check_text_hygiene(text))
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE Reference Metadata Readiness Audit",
        "",
        "This report is generated by `tools/check_ieee_reference_metadata_readiness.py`. It performs a stricter planning-stage check of `paper/ieee_trans/references_seed.bib` than the lightweight reference audit.",
        "",
        "This report does not certify final IEEE bibliography correctness. The final `references.bib` still requires publisher-metadata verification after the target journal and final manuscript are fixed.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Area | Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{check.evidence}` | {check.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the seed bibliography or citation-planning item satisfies the local planning check.",
            "- `PENDING` means the item is acceptable for planning but should be verified before final `references.bib` creation.",
            "- `MISSING` means the reference seed or citation plan should be fixed before final manuscript assembly.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

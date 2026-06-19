from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT / "paper/ieee_trans/title_abstract_index_terms_workbench.md"
METADATA = ROOT / "paper/ieee_trans/submission_metadata_workbench.md"
AUTHOR_REQUIREMENTS = ROOT / "paper/ieee_tits_author_requirements_audit.md"
REPORT_PATH = ROOT / "paper/ieee_front_matter_audit.md"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading < 0 else rest[:next_heading]


def blockquote(section_text: str) -> str:
    lines: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            lines.append(stripped.lstrip(">").strip())
    return " ".join(lines).strip()


def bullet_items(section_text: str) -> list[str]:
    items: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def labeled_block(text: str, label: str) -> str:
    marker = f"{label}:"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    next_label = re.search(r"\n[A-Za-z -]+:\n", rest)
    return rest if next_label is None else rest[: next_label.start()]


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def audit() -> list[Check]:
    text = read(WORKBENCH)
    metadata = read(METADATA)
    requirements = read(AUTHOR_REQUIREMENTS)
    checks: list[Check] = []

    checks.append(
        Check(
            "Source",
            "T-ITS front-matter workbench",
            "ready" if WORKBENCH.exists() else "missing",
            WORKBENCH.relative_to(ROOT).as_posix(),
            "" if WORKBENCH.exists() else "Restore the title/abstract/index-term workbench.",
        )
    )
    checks.append(
        Check(
            "Source",
            "T-ITS author requirements audit",
            "ready" if AUTHOR_REQUIREMENTS.exists() else "missing",
            AUTHOR_REQUIREMENTS.relative_to(ROOT).as_posix(),
            "" if AUTHOR_REQUIREMENTS.exists() else "Create or restore the official-source requirements audit.",
        )
    )

    rules_ready = all(token in text for token in ["150-250 words", "Maximum six", "UAV-assisted traffic perception"])
    checks.append(
        Check(
            "Rules",
            "Workbench records T-ITS abstract and keyword limits",
            "ready" if rules_ready else "missing",
            "150-250 words / maximum six / traffic perception",
            "" if rules_ready else "Add official T-ITS front-matter limits to the workbench.",
        )
    )

    official_ready = all(token in requirements for token in ["Abstract length", "Maximum six keywords", "Regular 10 pages"])
    checks.append(
        Check(
            "Rules",
            "Official-source requirements contain front-matter constraints",
            "ready" if official_ready else "missing",
            "author requirements audit tokens",
            "" if official_ready else "Re-check the T-ITS official page and update the requirements audit.",
        )
    )

    safe = blockquote(section(text, "Current Safe Abstract Template"))
    safe_words = count_words(safe)
    checks.append(
        Check(
            "Abstract",
            "Current safe abstract exists",
            "ready" if safe else "missing",
            f"{safe_words} words" if safe else "not found",
            "" if safe else "Add an internal safe abstract template.",
        )
    )
    one_paragraph = bool(safe) and "\n" not in safe.strip()
    checks.append(
        Check(
            "Abstract",
            "Current safe abstract is one paragraph",
            "ready" if one_paragraph else "missing",
            "single blockquote paragraph" if one_paragraph else "not one paragraph",
            "" if one_paragraph else "Rewrite the safe abstract as one paragraph.",
        )
    )
    length_status = "ready" if 150 <= safe_words <= 250 else "pending"
    checks.append(
        Check(
            "Abstract",
            "Final abstract length compliance",
            length_status,
            f"{safe_words} words; final requirement is 150-250",
            "" if length_status == "ready" else "Current safe abstract is internal only; rewrite the final abstract after final evidence is available.",
        )
    )
    traffic_fit = bool(re.search(r"\b(UAV|unmanned aerial vehicle)\b", safe, re.I)) and bool(
        re.search(r"\btraffic|road users?\b", safe, re.I)
    )
    checks.append(
        Check(
            "Abstract",
            "T-ITS traffic-sensing framing appears in safe abstract",
            "ready" if traffic_fit else "missing",
            "UAV plus traffic/road-user wording" if traffic_fit else "traffic framing not found",
            "" if traffic_fit else "Make the transportation application visible in the abstract.",
        )
    )
    forbidden_safe = bool(re.search(r"\\cite|\[[0-9]+\]|\\begin\{tabular\}|\\begin\{equation\}", safe))
    checks.append(
        Check(
            "Abstract",
            "Safe abstract avoids references, displayed equations, and tables",
            "ready" if not forbidden_safe else "missing",
            "no citation/equation/table markers" if not forbidden_safe else "forbidden marker found",
            "" if not forbidden_safe else "Remove references, displayed equations, and tables from the abstract.",
        )
    )

    locked = blockquote(section(text, "Locked Final Abstract Template"))
    placeholders = re.findall(r"\[[A-Z0-9 -]+\]", locked)
    checks.append(
        Check(
            "Abstract",
            "Final abstract template remains locked with placeholders",
            "ready" if len(placeholders) >= 5 else "missing",
            f"{len(placeholders)} placeholders",
            "" if len(placeholders) >= 5 else "Do not partially fill the final abstract without evidence.",
        )
    )
    guard_ready = "Do not fill any bracketed placeholder without a traceable table or run artifact." in text
    checks.append(
        Check(
            "Abstract",
            "Placeholder evidence guard is present",
            "ready" if guard_ready else "missing",
            "guard sentence found" if guard_ready else "guard sentence missing",
            "" if guard_ready else "Add explicit guard wording below the locked final abstract template.",
        )
    )

    index_section = section(text, "Candidate Index Terms")
    methodology = bullet_items(labeled_block(index_section, "Methodology candidates"))
    applications = bullet_items(labeled_block(index_section, "Application candidates"))
    free_keywords = bullet_items(labeled_block(index_section, "Free-keyword candidates"))
    checks.append(
        Check(
            "Index Terms",
            "Methodology candidate terms exist",
            "ready" if len(methodology) >= 2 else "missing",
            f"{len(methodology)} methodology candidates",
            "" if len(methodology) >= 2 else "Add one to two official methodology terms.",
        )
    )
    checks.append(
        Check(
            "Index Terms",
            "Application candidate terms exist",
            "ready" if len(applications) >= 2 else "missing",
            f"{len(applications)} application candidates",
            "" if len(applications) >= 2 else "Add one to two official application terms.",
        )
    )
    checks.append(
        Check(
            "Index Terms",
            "Free-keyword pool is available",
            "ready" if len(free_keywords) >= 2 else "pending",
            f"{len(free_keywords)} free-keyword candidates; final can use at most two",
            "" if len(free_keywords) >= 2 else "Add optional free-keyword candidates.",
        )
    )
    max_six_rule = "no more than six" in index_section and "no more than two optional free keywords" in index_section
    checks.append(
        Check(
            "Index Terms",
            "Final keyword-count guard is present",
            "ready" if max_six_rule else "missing",
            "max-six and max-two-free guard" if max_six_rule else "keyword-count guard missing",
            "" if max_six_rule else "Add the T-ITS keyword-count guard to the workbench.",
        )
    )

    portal_ready = "https://ieee.atyponrex.com/journal/t-its" in metadata
    checks.append(
        Check(
            "Submission Metadata",
            "T-ITS submission portal recorded",
            "ready" if portal_ready else "missing",
            "IEEE Author Portal URL" if portal_ready else "portal URL missing",
            "" if portal_ready else "Record the T-ITS submission portal in the metadata workbench.",
        )
    )
    manual_pending = all(token in metadata for token in ["Author 1 name", "Funding agency", "Open access choice"])
    checks.append(
        Check(
            "Submission Metadata",
            "Manual metadata fields remain explicit",
            "ready" if manual_pending else "missing",
            "author/funding/OA fields present" if manual_pending else "manual fields missing",
            "" if manual_pending else "Restore manual-confirmation metadata fields.",
        )
    )

    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE Front Matter Audit",
        "",
        "This report is generated by `tools/check_ieee_front_matter.py`. It checks the T-ITS title, abstract, index-term, and submission-metadata workbenches without creating final-facing manuscript text.",
        "",
        "The audit does not launch training and does not turn planning placeholders into final claims.",
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
            "- `READY` means the workbench currently satisfies the planning-level front-matter guard.",
            "- `PENDING` means the item is intentionally incomplete until final evidence or advisor metadata exists.",
            "- `MISSING` means a required front-matter rule or guard should be restored before manuscript assembly.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

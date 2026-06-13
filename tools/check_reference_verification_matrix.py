from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "paper/reference_verification_matrix.md"
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/reference_verification_audit.md"


@dataclass
class MatrixRow:
    row_id: str
    topic: str
    source: str
    url: str
    use: str
    status: str


@dataclass
class RefCheck:
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


def parse_markdown_rows(text: str) -> list[MatrixRow]:
    rows: list[MatrixRow] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("| R"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"R[0-9]{2}", cells[0]):
            rows.append(MatrixRow(*cells[:6]))
    return rows


def extract_bibitems(tex: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    pattern = re.compile(r"\\bibitem\{([^}]+)\}\s*(.*?)(?=\\bibitem\{|\\end\{thebibliography\})", re.S)
    for match in pattern.finditer(tex):
        key = match.group(1).strip()
        body = re.sub(r"\s+", " ", match.group(2)).strip()
        items.append((key, body))
    return items


def normalized_words(text: str) -> set[str]:
    cleaned = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)
    cleaned = re.sub(r"[^A-Za-z0-9]+", " ", cleaned).lower()
    return {word for word in cleaned.split() if len(word) >= 4}


def row_matches_bibitem(row: MatrixRow, bib_body: str) -> bool:
    row_words = normalized_words(f"{row.source} {row.url}")
    bib_words = normalized_words(bib_body)
    if not row_words or not bib_words:
        return False
    return len(row_words & bib_words) >= 2


def audit() -> list[RefCheck]:
    checks: list[RefCheck] = []
    if not MATRIX_PATH.exists():
        return [
            RefCheck(
                "Reference verification matrix exists",
                "missing",
                str(MATRIX_PATH.relative_to(ROOT)),
                "Create the reference verification matrix.",
            )
        ]
    if not TEX_PATH.exists():
        return [
            RefCheck(
                "LaTeX manuscript exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore the LaTeX manuscript source.",
            )
        ]

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8-sig")
    tex_text = TEX_PATH.read_text(encoding="utf-8")
    rows = parse_markdown_rows(matrix_text)
    bibitems = extract_bibitems(tex_text)

    checks.append(
        RefCheck(
            "Reference verification matrix exists",
            "ready",
            str(MATRIX_PATH.relative_to(ROOT)),
        )
    )
    checks.append(
        RefCheck(
            "Verified core row count",
            "ready" if len(rows) >= 25 else "partial",
            f"{len(rows)} R-prefixed core rows",
            "Target at least 25 verified core rows before final submission." if len(rows) < 25 else "",
        )
    )
    checks.append(
        RefCheck(
            "LaTeX bibliography count",
            "ready" if len(bibitems) >= 25 else "partial",
            f"{len(bibitems)} bibitem entries",
            "Target 25-35 references for the journal manuscript." if len(bibitems) < 25 else "",
        )
    )

    duplicate_rows = sorted({row.row_id for row in rows if [r.row_id for r in rows].count(row.row_id) > 1})
    checks.append(
        RefCheck(
            "Unique matrix row IDs",
            "ready" if not duplicate_rows else "missing",
            "no duplicate R-prefixed IDs" if not duplicate_rows else ", ".join(duplicate_rows),
            "" if not duplicate_rows else "Rename or merge duplicate reference rows.",
        )
    )

    rows_without_url = [row.row_id for row in rows if not row.url.startswith(("http://", "https://"))]
    checks.append(
        RefCheck(
            "Core rows have source URLs",
            "ready" if not rows_without_url else "missing",
            f"{len(rows)} source URLs checked" if not rows_without_url else ", ".join(rows_without_url),
            "" if not rows_without_url else "Add official, publisher, arXiv, CVF, or documentation URLs.",
        )
    )

    weak_status = [
        row.row_id
        for row in rows
        if not re.search(r"verified|official|source|publisher|arxiv|cvf|pmlr|documentation|cross-checked", row.status, re.I)
    ]
    checks.append(
        RefCheck(
            "Core row verification status",
            "ready" if not weak_status else "partial",
            "all core rows have verification-oriented status" if not weak_status else ", ".join(weak_status),
            "" if not weak_status else "Clarify verification status for these references before final submission.",
        )
    )

    matched_bibitems: list[str] = []
    unmatched_bibitems: list[str] = []
    for key, body in bibitems:
        if any(row_matches_bibitem(row, body) for row in rows):
            matched_bibitems.append(key)
        else:
            unmatched_bibitems.append(key)

    checks.append(
        RefCheck(
            "LaTeX bibliography covered by matrix",
            "ready" if not unmatched_bibitems else "partial",
            f"{len(matched_bibitems)}/{len(bibitems)} bibitems matched to matrix rows"
            if not unmatched_bibitems
            else "unmatched: " + ", ".join(unmatched_bibitems),
            "" if not unmatched_bibitems else "Add or refine matrix rows for unmatched LaTeX bibliography entries.",
        )
    )

    candidate_rows = len(re.findall(r"^\| C[0-9]{2} \|", matrix_text, flags=re.M))
    chinese_candidate_rows = len(re.findall(r"^\| CJ[0-9]{2} \|", matrix_text, flags=re.M))
    checks.append(
        RefCheck(
            "Candidate literature leads separated from core references",
            "ready" if candidate_rows or chinese_candidate_rows else "partial",
            f"{candidate_rows} international candidates, {chinese_candidate_rows} Chinese-journal leads",
            "Keep unverified candidates out of final bibliography until metadata is checked.",
        )
    )

    return checks


def write_report(checks: list[RefCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# Reference Verification Audit",
        "",
        "This report is generated by `tools/check_reference_verification_matrix.py`. It checks whether the reference verification matrix covers the LaTeX bibliography and keeps verified core references separate from candidate literature leads. It does not browse the web or certify scholarly correctness.",
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
            "- `READY` means the local reference tracking structure is complete for this item.",
            "- `PARTIAL` means the item is usable but still needs human verification before final journal submission.",
            "- `MISSING` means a required matrix field, URL, ID, or manuscript source is absent.",
            "",
            "The final bibliography should still be manually checked against publisher, arXiv, CVF, PMLR, official documentation, CNKI, Wanfang, or the journal website before submission.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

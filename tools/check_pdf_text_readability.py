from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "paper/manuscript_submission_candidate.pdf"
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/pdf_text_readability_audit.md"


EXPECTED_TOKENS = [
    ("Chinese title phrase", "\u9762\u5411\u65e0\u4eba\u673a\u822a\u62cd\u5c0f\u76ee\u6807\u68c0\u6d4b"),
    ("Model family", "YOLO11n"),
    ("Dataset", "VisDrone"),
    ("Primary metric", "mAP50"),
]

MOJIBAKE_PATTERNS = [
    ("replacement character", re.compile("\ufffd")),
    ("noncharacter U+FFFE", re.compile("\ufffe")),
    ("soft hyphen", re.compile("\u00ad")),
    ("common mojibake token: U+9286", re.compile("\u9286")),
    ("common mojibake token: U+9428", re.compile("\u9428")),
    ("common mojibake token: U+9429", re.compile("\u9429")),
    ("common mojibake token: U+93C8", re.compile("\u93c8")),
    ("common mojibake token: U+59AB", re.compile("\u59ab")),
]


@dataclass
class PdfTextCheck:
    item: str
    status: str
    evidence: str
    action: str = ""


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
    }[status]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def extract_text() -> tuple[str, str]:
    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local environment
        return "", f"PyMuPDF import failed: {type(exc).__name__}: {exc}"

    try:
        with fitz.open(PDF_PATH) as doc:
            text = "\n".join(page.get_text() for page in doc)
            return text, f"PyMuPDF extracted {len(text)} characters from {doc.page_count} pages"
    except Exception as exc:  # pragma: no cover - depends on PDF backend
        return "", f"PDF text extraction failed: {type(exc).__name__}: {exc}"


def audit() -> list[PdfTextCheck]:
    checks: list[PdfTextCheck] = []

    if not PDF_PATH.exists():
        return [
            PdfTextCheck(
                "Compiled PDF exists",
                "missing",
                str(PDF_PATH.relative_to(ROOT)),
                "Rebuild the LaTeX paper PDF.",
            )
        ]

    checks.append(
        PdfTextCheck(
            "Compiled PDF exists",
            "ready",
            f"{PDF_PATH.relative_to(ROOT)} ({PDF_PATH.stat().st_size / 1024:.1f} KB)",
        )
    )

    if TEX_PATH.exists():
        pdf_mtime = PDF_PATH.stat().st_mtime
        tex_mtime = TEX_PATH.stat().st_mtime
        checks.append(
            PdfTextCheck(
                "PDF is newer than LaTeX source",
                "ready" if pdf_mtime >= tex_mtime else "missing",
                f"pdf_mtime={pdf_mtime:.0f}, tex_mtime={tex_mtime:.0f}",
                "" if pdf_mtime >= tex_mtime else "Rebuild the PDF after editing the LaTeX source.",
            )
        )
    else:
        checks.append(
            PdfTextCheck(
                "LaTeX source exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore the LaTeX source used to build the PDF.",
            )
        )

    text, extraction_evidence = extract_text()
    checks.append(
        PdfTextCheck(
            "PDF text extraction",
            "ready" if text else "missing",
            extraction_evidence,
            "" if text else "Install or repair PyMuPDF/PDF extraction support before final text QA.",
        )
    )

    if not text:
        return checks

    normalized = normalize_text(text)
    checks.append(
        PdfTextCheck(
            "Extracted text length",
            "ready" if len(text) >= 1000 else "missing",
            f"{len(text)} extracted characters",
            "" if len(text) >= 1000 else "Check whether the PDF is image-only or font extraction failed.",
        )
    )

    for item, token in EXPECTED_TOKENS:
        found = token in normalized
        checks.append(
            PdfTextCheck(
                f"Expected text token: {item}",
                "ready" if found else "missing",
                token if found else "not found in extracted PDF text",
                "" if found else "Inspect the compiled PDF and rebuild from the current LaTeX source.",
            )
        )

    hygiene_hits: list[str] = []
    for label, pattern in MOJIBAKE_PATTERNS:
        matches = list(pattern.finditer(text))
        if matches:
            line_numbers = sorted({text.count("\n", 0, m.start()) + 1 for m in matches})
            shown = ", ".join(str(n) for n in line_numbers[:5])
            if len(line_numbers) > 5:
                shown += ", ..."
            hygiene_hits.append(f"{label} at extracted-text line {shown}")

    checks.append(
        PdfTextCheck(
            "Extracted PDF text hygiene",
            "ready" if not hygiene_hits else "missing",
            "no mojibake or hidden-character patterns found" if not hygiene_hits else "; ".join(hygiene_hits),
            "" if not hygiene_hits else "Rebuild the PDF after cleaning source text or font encoding issues.",
        )
    )

    return checks


def write_report(checks: list[PdfTextCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# PDF Text Readability Audit",
        "",
        "This report is generated by `tools/check_pdf_text_readability.py`. It extracts text from the compiled submission PDF and checks whether the main title phrase, core model/dataset/metric tokens, and common text-corruption markers are present or absent as expected.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Item | Status | Evidence | Action |",
        "| --- | --- | --- | --- |",
    ]
    for c in checks:
        lines.append(f"| {c.item} | {status_symbol(c.status)} | `{c.evidence}` | {c.action} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the compiled PDF can be text-extracted and contains the expected paper-identifying tokens.",
            "- `MISSING` means the PDF should be rebuilt or manually inspected before submission.",
            "- This audit does not judge scientific completeness; it only checks the compiled PDF artifact for basic readability and text-corruption risks.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

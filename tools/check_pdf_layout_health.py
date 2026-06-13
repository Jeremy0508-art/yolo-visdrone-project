from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "paper/manuscript_submission_candidate.pdf"
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
REPORT_PATH = ROOT / "paper/pdf_layout_health_audit.md"


@dataclass
class LayoutCheck:
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


def audit() -> list[LayoutCheck]:
    checks: list[LayoutCheck] = []

    if not PDF_PATH.exists():
        return [
            LayoutCheck(
                "Compiled PDF exists",
                "missing",
                str(PDF_PATH.relative_to(ROOT)),
                "Build the paper PDF before layout inspection.",
            )
        ]

    checks.append(
        LayoutCheck(
            "Compiled PDF exists",
            "ready",
            f"{PDF_PATH.relative_to(ROOT)} ({PDF_PATH.stat().st_size / 1024:.1f} KB)",
        )
    )

    if TEX_PATH.exists():
        pdf_mtime = PDF_PATH.stat().st_mtime
        tex_mtime = TEX_PATH.stat().st_mtime
        checks.append(
            LayoutCheck(
                "PDF freshness",
                "ready" if pdf_mtime >= tex_mtime else "partial",
                f"pdf_mtime={pdf_mtime:.0f}, tex_mtime={tex_mtime:.0f}",
                "" if pdf_mtime >= tex_mtime else "Rebuild the PDF after LaTeX edits.",
            )
        )
    else:
        checks.append(
            LayoutCheck(
                "LaTeX source exists",
                "missing",
                str(TEX_PATH.relative_to(ROOT)),
                "Restore the LaTeX source for reproducible PDF generation.",
            )
        )

    try:
        import fitz  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local environment
        checks.append(
            LayoutCheck(
                "PDF parser available",
                "missing",
                f"PyMuPDF import failed: {type(exc).__name__}: {exc}",
                "Install PyMuPDF to enable PDF layout inspection.",
            )
        )
        return checks

    try:
        doc = fitz.open(PDF_PATH)
    except Exception as exc:  # pragma: no cover - depends on local PDF state
        checks.append(
            LayoutCheck(
                "PDF opens",
                "missing",
                f"{type(exc).__name__}: {exc}",
                "Rebuild the PDF and inspect the build log.",
            )
        )
        return checks

    with doc:
        page_count = doc.page_count
        checks.append(
            LayoutCheck(
                "Page count",
                "ready" if page_count >= 6 else "partial",
                f"{page_count} pages",
                "" if page_count >= 6 else "Check whether the manuscript is too short for the journal-oriented draft.",
            )
        )

        page_sizes: list[str] = []
        blank_pages: list[int] = []
        low_text_no_media_pages: list[int] = []
        figure_dominant_pages: list[int] = []
        image_heavy_pages: list[int] = []
        page_text_lengths: list[int] = []

        for index, page in enumerate(doc, start=1):
            rect = page.rect
            page_sizes.append(f"{rect.width:.1f}x{rect.height:.1f}")
            text = page.get_text("text")
            text_len = len(text.strip())
            page_text_lengths.append(text_len)
            image_count = len(page.get_images(full=True))
            drawings_count = len(page.get_drawings())
            if text_len < 20 and image_count == 0 and drawings_count == 0:
                blank_pages.append(index)
            if text_len < 80 and image_count == 0 and drawings_count == 0:
                low_text_no_media_pages.append(index)
            if text_len < 120 and (image_count > 0 or drawings_count > 0):
                figure_dominant_pages.append(index)
            if image_count >= 3 and text_len < 500:
                image_heavy_pages.append(index)

        unique_sizes = sorted(set(page_sizes))
        checks.append(
            LayoutCheck(
                "Page size consistency",
                "ready" if len(unique_sizes) == 1 else "partial",
                "; ".join(unique_sizes),
                "" if len(unique_sizes) == 1 else "Inspect PDF pages with inconsistent media boxes.",
            )
        )

        checks.append(
            LayoutCheck(
                "Blank pages",
                "ready" if not blank_pages else "missing",
                "none" if not blank_pages else ", ".join(str(p) for p in blank_pages),
                "" if not blank_pages else "Remove unintended blank pages before submission.",
            )
        )

        checks.append(
            LayoutCheck(
                "Low-text non-media pages",
                "ready" if not low_text_no_media_pages else "partial",
                "none" if not low_text_no_media_pages else ", ".join(str(p) for p in low_text_no_media_pages),
                "" if not low_text_no_media_pages else "Manually inspect low-text pages that do not contain figures or drawing objects.",
            )
        )

        checks.append(
            LayoutCheck(
                "Figure-dominant pages",
                "ready" if len(figure_dominant_pages) <= 2 else "partial",
                "none" if not figure_dominant_pages else ", ".join(str(p) for p in figure_dominant_pages),
                "" if len(figure_dominant_pages) <= 2 else "Inspect whether large visual pages should be resized or split.",
            )
        )

        checks.append(
            LayoutCheck(
                "Image-heavy pages",
                "ready" if len(image_heavy_pages) <= 2 else "partial",
                "none" if not image_heavy_pages else ", ".join(str(p) for p in image_heavy_pages),
                "" if len(image_heavy_pages) <= 2 else "Inspect whether large visual figures should be resized or moved.",
            )
        )

        total_text = sum(page_text_lengths)
        checks.append(
            LayoutCheck(
                "Extracted text volume",
                "ready" if total_text >= 5000 else "partial",
                f"{total_text} extracted characters across {page_count} pages",
                "" if total_text >= 5000 else "Check whether the PDF is image-heavy or text extraction failed.",
            )
        )

    return checks


def write_report(checks: list[LayoutCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# PDF Layout Health Audit",
        "",
        "This report is generated by `tools/check_pdf_layout_health.py`. It checks basic compiled-PDF layout health: file freshness, page count, page-size consistency, blank pages, low-text pages, image-heavy pages, and extracted text volume.",
        "",
        "It is a mechanical preflight check, not a substitute for manual visual inspection before submission.",
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
        lines.append(
            f"| {check.item} | {status_symbol(check.status)} | `{check.evidence}` | {check.action} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the compiled PDF passes the configured mechanical layout check.",
            "- `PARTIAL` means the PDF can exist and compile, but a page-level issue should be manually inspected.",
            "- `MISSING` means the PDF artifact or a basic layout condition is absent and should be fixed before submission.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

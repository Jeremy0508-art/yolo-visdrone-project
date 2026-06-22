from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_draft_shareability_audit.md"

MAIN_TEX = ROOT / "paper/ieee_trans/main_draft.tex"
MAIN_PDF = ROOT / "paper/ieee_trans/main_draft.pdf"
MAIN_LOG = ROOT / "paper/ieee_trans/main_draft.log"


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


def line_hits(path: Path, pattern: re.Pattern[str], allow_negated: bool = False) -> list[str]:
    text = read_text(path)
    negation = re.compile(
        r"\b(no|not|do not|does not|cannot|must not|may not|without|rather than|instead of|avoid|locked|pending|before complete|before completed)\b",
        re.I,
    )
    hits: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not pattern.search(line):
            continue
        if allow_negated and negation.search(line):
            continue
        hits.append(f"{path.relative_to(ROOT).as_posix()}:{number}: {line.strip()[:180]}")
    return hits


def check_exists(path: Path, label: str) -> Check:
    return Check(
        "Build artifact",
        label,
        "ready" if path.exists() else "missing",
        path.relative_to(ROOT).as_posix(),
        "" if path.exists() else f"Create or rebuild `{path.relative_to(ROOT).as_posix()}`.",
    )


def check_pdf_freshness() -> Check:
    if not MAIN_TEX.exists() or not MAIN_PDF.exists():
        return Check(
            "Build artifact",
            "PDF is available and not older than source",
            "missing",
            "main_draft.tex or main_draft.pdf missing",
            "Compile the advisor-review draft before sharing.",
        )
    tex_time = MAIN_TEX.stat().st_mtime
    pdf_time = MAIN_PDF.stat().st_mtime
    if pdf_time >= tex_time:
        return Check(
            "Build artifact",
            "PDF is available and not older than source",
            "ready",
            f"pdf_time={MAIN_PDF.stat().st_mtime_ns}; tex_time={MAIN_TEX.stat().st_mtime_ns}",
        )
    return Check(
        "Build artifact",
        "PDF is available and not older than source",
        "pending",
        f"PDF older than TeX source: {MAIN_PDF.relative_to(ROOT).as_posix()}",
        "Recompile `main_draft.tex` before sharing the PDF.",
    )


def check_latex_log() -> list[Check]:
    if not MAIN_LOG.exists():
        return [
            Check(
                "Build artifact",
                "LaTeX log exists",
                "pending",
                MAIN_LOG.relative_to(ROOT).as_posix(),
                "Recompile the draft to refresh the log.",
            )
        ]
    log = read_text(MAIN_LOG)
    fatal_patterns = [
        "Undefined control sequence",
        "LaTeX Error",
        "Fatal error",
        "Emergency stop",
    ]
    warning_patterns = [
        "Citation `",
        "Reference `",
        "undefined references",
        "undefined citations",
    ]
    fatal_hits = [p for p in fatal_patterns if p in log]
    warning_hits = [p for p in warning_patterns if p in log]
    return [
        Check(
            "Build artifact",
            "LaTeX fatal errors absent",
            "ready" if not fatal_hits else "missing",
            "none" if not fatal_hits else ", ".join(fatal_hits),
            "" if not fatal_hits else "Fix LaTeX errors before sharing the PDF.",
        ),
        Check(
            "Build artifact",
            "Undefined references/citations absent",
            "ready" if not warning_hits else "missing",
            "none" if not warning_hits else ", ".join(warning_hits),
            "" if not warning_hits else "Resolve undefined references or citations before sharing.",
        ),
    ]


def check_status_label() -> Check:
    text = read_text(MAIN_TEX)
    needed = "Evidence-bounded IEEE draft"
    return Check(
        "Draft boundary",
        "Draft source declares non-final status",
        "ready" if needed in text and "not a submission-ready manuscript" in text else "missing",
        needed if needed in text else "not found",
        "" if needed in text else "Add an explicit non-final/advisor-review status comment.",
    )


def check_placeholder_authors() -> Check:
    text = read_text(MAIN_TEX)
    has_placeholder = "First~Author" in text or "Second~Author" in text or "Third~Author" in text
    if has_placeholder:
        return Check(
            "Draft boundary",
            "Author placeholders are acceptable only because this is advisor-review",
            "pending",
            "First/Second/Third Author placeholders found",
            "Replace with real authors only after advisor metadata is confirmed.",
        )
    return Check("Draft boundary", "Author placeholders removed", "ready", "no placeholder author names found")


def check_forbidden_markers() -> list[Check]:
    files = [
        ROOT / "paper/ieee_trans/main_draft.tex",
        ROOT / "paper/ieee_trans/README.md",
        ROOT / "paper/README.md",
    ]
    patterns = [
        ("TODO marker", re.compile(r"\bTODO\b", re.I)),
        ("Chinese pending marker", re.compile("\u5f85\u8865\u5145")),
        ("TBD marker", re.compile(r"\bTBD\b", re.I)),
        ("placeholder ellipsis marker", re.compile(r"\.\.\.|……")),
    ]
    checks: list[Check] = []
    for label, pattern in patterns:
        hits: list[str] = []
        for path in files:
            hits.extend(line_hits(path, pattern))
        checks.append(
            Check(
                "Text hygiene",
                label,
                "ready" if not hits else "missing",
                "none" if not hits else "; ".join(hits[:8]),
                "" if not hits else "Remove placeholder text before advisor sharing.",
            )
        )
    return checks


def check_claim_patterns() -> list[Check]:
    checks: list[Check] = []
    path = MAIN_TEX
    patterns = [
        (
            "Unqualified SOTA wording",
            re.compile(r"\b(state[- ]of[- ]the[- ]art|SOTA)\b", re.I),
            True,
            "Keep SOTA only in negated/boundary statements.",
        ),
        (
            "Unqualified cross-dataset robustness/generalization",
            re.compile(r"\b(robust across datasets|cross[- ]dataset robustness|generalization guarantee|generalize[s]?)\b", re.I),
            True,
            "Keep cross-dataset wording only as a boundary or negative statement until evidence supports it.",
        ),
        (
            "Unqualified larger-model superiority",
            re.compile(r"\b(outperform(?:s|ed|ing)?|surpass(?:es|ed|ing)?|beats?)\b.*\b(YOLO11s|larger|all)\b", re.I),
            True,
            "Do not imply the nano model beats YOLO11s or all larger models.",
        ),
        (
            "ScaleGate performance claim before gate",
            re.compile(r"Scale(?:Aware)?P2Gate[^\n]{0,140}\b(improve|gain|outperform|surpass|boost|robust|mAP|AP50|recall|precision|FPS)\b", re.I),
            True,
            "ScaleGate can be described structurally, but not with performance claims before the result gate opens.",
        ),
    ]
    for label, pattern, allow_negated, action in patterns:
        hits = line_hits(path, pattern, allow_negated=allow_negated)
        checks.append(
            Check(
                "Claim discipline",
                label,
                "ready" if not hits else "missing",
                "none" if not hits else "; ".join(hits[:8]),
                "" if not hits else action,
            )
        )
    return checks


def check_dual_route_language() -> list[Check]:
    files = [
        ROOT / "README.md",
        ROOT / "paper/README.md",
        ROOT / "paper/ieee_trans/README.md",
    ]
    abandoned_pattern = re.compile(r"\b(abandoned|historical|old project|legacy|deprecated)\b", re.I)
    hits: list[str] = []
    for path in files:
        hits.extend(line_hits(path, abandoned_pattern, allow_negated=True))
    text = "\n".join(read_text(path) for path in files)
    has_parallel = bool(
        re.search(r"\bparallel\b", text, re.I)
        or "\u5e76\u884c" in text
        or re.search(r"\btwo active paper routes\b", text, re.I)
        or re.search(r"\btwo routes share\b", text, re.I)
    )
    checks = [
        Check(
            "Dual-route boundary",
            "CEA route is not described as abandoned",
            "ready" if not hits else "missing",
            "none" if not hits else "; ".join(hits[:8]),
            "" if not hits else "Revise wording so the Chinese route remains active/parallel, not abandoned.",
        ),
        Check(
            "Dual-route boundary",
            "Parallel Chinese/English route wording present",
            "ready" if has_parallel else "pending",
            "parallel/并行 wording found" if has_parallel else "not found",
            "" if has_parallel else "Add explicit wording that CEA and IEEE are parallel routes.",
        ),
    ]
    return checks


def audit() -> list[Check]:
    checks: list[Check] = []
    checks.append(check_exists(MAIN_TEX, "main_draft.tex exists"))
    checks.append(check_exists(MAIN_PDF, "main_draft.pdf exists"))
    checks.append(check_pdf_freshness())
    checks.extend(check_latex_log())
    checks.append(check_status_label())
    checks.append(check_placeholder_authors())
    checks.extend(check_forbidden_markers())
    checks.extend(check_claim_patterns())
    checks.extend(check_dual_route_language())
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# IEEE Draft Shareability Audit",
        "",
        "This report is generated by `tools/check_ieee_draft_shareability.py`. It checks whether the current advisor-review IEEE draft can be shared without accidentally presenting itself as a final submission or leaking unsupported claims.",
        "",
        "This is stricter than a build check but lighter than final submission review. Author placeholders and target-journal metadata may remain pending in an advisor-review draft.",
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
        evidence = check.evidence.replace("\n", "<br>")
        lines.append(f"| {check.area} | {check.item} | {status_label(check.status)} | `{evidence}` | {check.action} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the advisor-review draft passes that shareability check.",
            "- `PENDING` means the item is acceptable for advisor review but must be resolved before final submission.",
            "- `MISSING` means the draft should be fixed before sharing as the current IEEE PDF.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

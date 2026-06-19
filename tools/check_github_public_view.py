from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass


REPORT_PATH = "paper/github_public_view_audit.md"

REPO_URL = "https://github.com/Jeremy0508-art/yolo-visdrone-project"
RAW_README_URL = "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/README.md"


@dataclass(frozen=True)
class Check:
    item: str
    status: str
    evidence: str
    action: str = ""


def fetch_text(url: str, timeout: int = 20) -> tuple[int | None, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "yolo-visdrone-submission-audit",
            "Accept": "text/plain,text/html,*/*",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            return response.status, body, ""
    except urllib.error.HTTPError as exc:
        return exc.code, "", str(exc)
    except urllib.error.URLError as exc:
        return None, "", str(exc)


def check_url(url: str, timeout: int = 20) -> tuple[bool, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "yolo-visdrone-submission-audit"},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 405:
            status, _, err = fetch_text(url, timeout=timeout)
            return status is not None and 200 <= status < 400, f"GET HTTP {status}" if status else err
        return False, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return False, str(exc)


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "missing": "MISSING",
        "partial": "PARTIAL",
    }[status]


def audit() -> list[Check]:
    checks: list[Check] = []

    repo_status, repo_text, repo_error = fetch_text(REPO_URL)
    repo_ready = repo_status is not None and 200 <= repo_status < 400
    checks.append(
        Check(
            "Repository page reachable",
            "ready" if repo_ready else "missing",
            f"HTTP {repo_status}" if repo_status else repo_error,
            "" if repo_ready else "Open the repository page manually or confirm the repository is public.",
        )
    )
    if repo_ready:
        required_repo_tokens = [
            ("Repository owner/name", "Jeremy0508-art/yolo-visdrone-project"),
            ("Public repository marker", "Public"),
            ("README area", "README"),
        ]
        for item, token in required_repo_tokens:
            found = token in repo_text
            checks.append(
                Check(
                    item,
                    "ready" if found else "missing",
                    token if found else "not found in repository page HTML",
                    "" if found else "Inspect GitHub rendering manually.",
                )
            )

    readme_status, readme_text, readme_error = fetch_text(RAW_README_URL)
    readme_ready = readme_status is not None and 200 <= readme_status < 400
    checks.append(
        Check(
            "Raw README reachable",
            "ready" if readme_ready else "missing",
            f"HTTP {readme_status}, {len(readme_text)} characters" if readme_ready else readme_error,
            "" if readme_ready else "Confirm README.md is pushed to the default branch.",
        )
    )
    if readme_ready:
        required_readme_tokens = [
            ("Current lightweight conclusion", "YOLO11n-P2-960"),
            ("Best nano mAP50", "0.42361"),
            ("YOLO11s capacity reference", "YOLO11s-960"),
            ("IEEE route", "IEEE Transactions"),
            ("IEEE dashboard link", "paper/ieee_submission_dashboard.md"),
            ("Method selection protocol link", "paper/ieee_method_selection_protocol.md"),
            ("Reviewer risk register link", "paper/ieee_reviewer_risk_register.md"),
            ("Scale AP interpretation link", "paper/ieee_scale_ap_interpretation.md"),
            ("IEEE workspace link", "paper/ieee_trans/"),
            ("Reproducibility command link", "paper/commands.md"),
        ]
        for item, token in required_readme_tokens:
            found = token in readme_text
            checks.append(
                Check(
                    item,
                    "ready" if found else "missing",
                    token if found else "not found in raw README",
                    "" if found else "Update README.md and push it to GitHub.",
                )
            )

        forbidden_tokens = [
            ("Stale unfinished wording", "还没完成"),
            ("Placeholder wording", "待补充"),
            ("Unsupported guarantee wording", "保证录用"),
            ("Old future-experiment wording", "后续建议实验"),
        ]
        for item, token in forbidden_tokens:
            found = token in readme_text
            checks.append(
                Check(
                    item,
                    "missing" if found else "ready",
                    f"found `{token}`" if found else f"`{token}` not found",
                    "Remove stale or unsupported public-facing wording from README.md." if found else "",
                )
            )

    public_artifacts = [
        (
            "Paper README raw",
            "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/paper/README.md",
        ),
        (
            "IEEE dashboard raw",
            "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/paper/ieee_submission_dashboard.md",
        ),
        (
            "IEEE workspace README raw",
            "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/paper/ieee_trans/README.md",
        ),
        (
            "IEEE scale AP interpretation raw",
            "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/paper/ieee_scale_ap_interpretation.md",
        ),
        (
            "IEEE scale AP figure raw",
            "https://raw.githubusercontent.com/Jeremy0508-art/yolo-visdrone-project/main/paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png",
        ),
    ]
    for item, url in public_artifacts:
        ok, evidence = check_url(url)
        checks.append(
            Check(
                item,
                "ready" if ok else "missing",
                evidence,
                "" if ok else f"Confirm `{url}` is committed and publicly reachable.",
            )
        )

    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# GitHub Public View Audit",
        "",
        "This report is generated by `tools/check_github_public_view.py`. It checks public GitHub reachability, raw README content, and a small set of public paper-material links.",
        "",
        "It is an automated public-link check, not a substitute for manual browser review of GitHub rendering.",
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
            "- `READY` means the public page, raw README token, or artifact URL was reachable during this audit.",
            "- `MISSING` means a public-facing item should be fixed or manually checked before sharing the repository.",
            "- Manual review is still needed to confirm visual rendering, image display, and browser-specific GitHub behavior.",
        ]
    )
    from pathlib import Path

    Path(REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()

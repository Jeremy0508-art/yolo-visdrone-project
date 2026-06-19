from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/ieee_dataset_compliance_audit.md"


@dataclass(frozen=True)
class Check:
    area: str
    item: str
    status: str
    evidence: str
    action: str = ""


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def git_ls_files(prefix: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", prefix],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def status_label(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "missing": "MISSING",
    }[status]


def check_license_audit() -> list[Check]:
    text = read_text("paper/ieee_dataset_license_audit.md")
    if not text:
        return [
            Check(
                "Dataset policy",
                "License audit document",
                "missing",
                "paper/ieee_dataset_license_audit.md",
                "Create the dataset license and citation audit before final manuscript assembly.",
            )
        ]

    required_urls = [
        "https://github.com/VisDrone/VisDrone-Dataset",
        "https://aiskyeye.com/data-protection/",
        "https://sites.google.com/view/grli-uavdt",
    ]
    missing_urls = [url for url in required_urls if url not in text]
    return [
        Check(
            "Dataset policy",
            "Official dataset-source URLs recorded",
            "ready" if not missing_urls else "missing",
            ", ".join(required_urls if not missing_urls else missing_urls),
            "" if not missing_urls else "Record the official dataset/provider URLs in the license audit.",
        )
    ]


def check_gitignore_boundaries() -> list[Check]:
    gitignore = read_text(".gitignore")
    required_patterns = [
        "data/raw/",
        "data/processed/",
        "*.pt",
        "*.zip",
        "*.tar",
        "*.tar.gz",
        "*.7z",
    ]
    checks: list[Check] = []
    for pattern in required_patterns:
        checks.append(
            Check(
                "Repository boundary",
                f"Gitignore protects `{pattern}`",
                "ready" if pattern in gitignore else "missing",
                ".gitignore",
                "" if pattern in gitignore else f"Add `{pattern}` to .gitignore before publishing artifacts.",
            )
        )
    return checks


def check_tracked_dataset_files() -> list[Check]:
    tracked = git_ls_files("data")
    forbidden = [
        path
        for path in tracked
        if path.startswith("data/raw/") or path.startswith("data/processed/")
    ]
    return [
        Check(
            "Repository boundary",
            "No raw or converted dataset files tracked by Git",
            "ready" if not forbidden else "missing",
            "tracked data files: " + (", ".join(forbidden[:10]) if forbidden else ", ".join(tracked) or "none"),
            "" if not forbidden else "Remove raw/converted dataset files from Git tracking and keep only dataset instructions.",
        )
    ]


def check_dataset_citations() -> list[Check]:
    refs = read_text("paper/ieee_trans/references_seed.bib")
    required_keys = [
        "du2019visdrone_det",
        "visdrone_dataset_repo",
        "du2018uavdt",
        "uavdt_project_page",
    ]
    checks: list[Check] = []
    for key in required_keys:
        checks.append(
            Check(
                "Citation coverage",
                f"Seed citation `{key}`",
                "ready" if key in refs else "missing",
                "paper/ieee_trans/references_seed.bib",
                "" if key in refs else f"Add and verify the `{key}` BibTeX entry before final references.bib.",
            )
        )
    return checks


def check_metadata_workbench() -> list[Check]:
    text = read_text("paper/ieee_trans/submission_metadata_workbench.md")
    required_tokens = [
        "paper/ieee_dataset_license_audit.md",
        "paper/ieee_dataset_compliance_audit.md",
        "Raw datasets, converted datasets, and trained weights are not redistributed",
    ]
    missing = [token for token in required_tokens if token not in text]
    return [
        Check(
            "Submission metadata",
            "Code/data statement links license and compliance audits",
            "ready" if not missing else "pending",
            "missing tokens: " + (", ".join(missing) if missing else "none"),
            "" if not missing else "Update the submission metadata workbench with dataset compliance audit links and safe data-release wording.",
        )
    ]


def check_config_presence() -> list[Check]:
    configs = [
        "configs/dataset/visdrone.yaml",
        "configs/dataset/uavdt.yaml",
    ]
    checks: list[Check] = []
    for rel_path in configs:
        path = ROOT / rel_path
        checks.append(
            Check(
                "Dataset configuration",
                rel_path,
                "ready" if path.exists() else "missing",
                rel_path,
                "" if path.exists() else "Restore the dataset YAML used by reproducibility commands.",
            )
        )
    return checks


def audit() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_license_audit())
    checks.extend(check_gitignore_boundaries())
    checks.extend(check_tracked_dataset_files())
    checks.extend(check_dataset_citations())
    checks.extend(check_metadata_workbench())
    checks.extend(check_config_presence())
    checks.append(
        Check(
            "Manual gate",
            "Advisor/institution final dataset-license confirmation",
            "pending",
            "required before final IEEE submission or public weight release",
            "Re-check official dataset pages and confirm release policy with the advisor before final submission.",
        )
    )
    return checks


def write_report(checks: list[Check]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    missing = sum(1 for c in checks if c.status == "missing")

    lines = [
        "# IEEE Dataset Compliance Audit",
        "",
        "This report is generated by `tools/check_ieee_dataset_compliance.py`. It checks the repository-facing dataset boundary, citation coverage, and submission-metadata wording for the IEEE route.",
        "",
        "The audit does not download datasets, connect to a server, or launch training. `PENDING` means manual advisor/institution confirmation is still required.",
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
        lines.append(
            f"| {check.area} | {check.item} | {status_label(check.status)} | `{evidence}` | {check.action} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `READY` means the repository currently respects the checked dataset boundary or has the required planning/citation material.",
            "- `PENDING` means human confirmation is required before final submission or public weight release.",
            "- `MISSING` means a repository or manuscript-preparation item should be fixed before sharing the final package.",
            "",
            "## Current Policy Boundary",
            "",
            "Raw datasets, converted datasets, dataset archives, and trained weights are not redistributed by this repository. The public project should provide code, configurations, reproducibility commands, result-summary scripts, and links to original dataset providers.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {rel(REPORT_PATH)}")


if __name__ == "__main__":
    main()

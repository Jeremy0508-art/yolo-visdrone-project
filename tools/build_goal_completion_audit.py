from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/GOAL_COMPLETION_AUDIT.md"


@dataclass(frozen=True)
class GoalCheck:
    requirement: str
    status: str
    evidence: str
    interpretation: str
    next_action: str = ""


def read_text(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8-sig")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def summary_values(path: str) -> dict[str, int]:
    text = read_text(path)
    values: dict[str, int] = {}
    for key in ["Total checks", "Ready", "Partial", "Pending", "Missing"]:
        match = re.search(rf"- {re.escape(key)}:\s*([0-9]+)", text)
        if match:
            values[key] = int(match.group(1))
    return values


def dashboard_values() -> dict[str, int]:
    text = read_text("paper/submission_audit_dashboard.md")
    values: dict[str, int] = {}
    patterns = {
        "total": r"- Total audit reports:\s*([0-9]+)",
        "ready": r"- Ready reports:\s*([0-9]+)",
        "partial": r"- Partial reports:\s*([0-9]+)",
        "pending": r"- Pending reports:\s*([0-9]+)",
        "missing": r"- Missing reports:\s*([0-9]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            values[key] = int(match.group(1))
    return values


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "pending": "PENDING",
        "partial": "PARTIAL",
        "missing": "MISSING",
    }[status]


def audit() -> list[GoalCheck]:
    checks: list[GoalCheck] = []

    dashboard = dashboard_values()
    material = summary_values("paper/submission_material_manifest.md")
    fair = summary_values("paper/synced_fair_experiment_artifacts_audit.md")
    preflight = summary_values("paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md")
    package = read_text("paper/advisor_review_package_manifest.md")

    checks.append(
        GoalCheck(
            "公平对比实验补强",
            "ready" if fair.get("Missing", 1) == 0 and fair.get("Pending", 1) == 0 else "pending",
            "paper/synced_fair_experiment_artifacts_audit.md; paper/tables/main_comparison_for_paper.csv",
            "YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960、YOLOv5n-640 的本地结果、权重、日志和 100-epoch 证据均已同步并审计。",
        )
    )

    checks.append(
        GoalCheck(
            "小目标专项分析",
            "ready"
            if exists("paper/tables/object_scale_distribution.csv")
            and exists("paper/tables/scale_group_results.csv")
            and exists("paper/figures/scale_analysis/object_scale_distribution.png")
            else "missing",
            "paper/tables/object_scale_distribution.csv; paper/tables/scale_group_results.csv; paper/figures/scale_analysis/",
            "已包含尺度分布、尺度组匹配分析和对应图表；该分析明确不是官方 AP。",
        )
    )

    checks.append(
        GoalCheck(
            "论文结构重写与投稿候选稿",
            "ready" if exists("paper/manuscript_submission_candidate.tex") and exists("paper/manuscript_submission_candidate.pdf") else "missing",
            "paper/manuscript_submission_candidate.tex; paper/manuscript_submission_candidate.pdf; paper/manuscript_journal_gap_audit.md",
            "当前 LaTeX/PDF 候选稿具备期刊论文结构，包含方法、实验、讨论、结论和图表。",
        )
    )

    checks.append(
        GoalCheck(
            "真实数值和证据追踪",
            "ready"
            if summary_values("paper/evidence_audit.md").get("Missing", 1) == 0
            and summary_values("paper/manuscript_number_trace_audit.md").get("Missing", 1) == 0
            else "missing",
            "paper/evidence_audit.md; paper/manuscript_number_trace_audit.md; paper/tables/",
            "论文数值已通过证据审计和数值追踪审计；不以未完成或无日志结果作为论文证据。",
        )
    )

    checks.append(
        GoalCheck(
            "LaTeX/PDF 本地可读性",
            "ready"
            if summary_values("paper/pdf_text_readability_audit.md").get("Missing", 1) == 0
            and summary_values("paper/pdf_layout_health_audit.md").get("Missing", 1) == 0
            else "missing",
            "paper/pdf_text_readability_audit.md; paper/pdf_layout_health_audit.md; paper/pdf_visual_contact_sheet.md",
            "PDF 可提取文本、基础版式健康，且已生成 15 页缩略图总览辅助人工页检。",
        )
    )

    checks.append(
        GoalCheck(
            "GitHub 材料同步与公开访问",
            "ready" if summary_values("paper/github_public_view_audit.md").get("Missing", 1) == 0 else "missing",
            "paper/github_public_view_audit.md; README.md; paper/README.md",
            "公开仓库、raw README、PDF、审计面板、导师说明和 PDF contact sheet 均通过自动链接检查。",
        )
    )

    checks.append(
        GoalCheck(
            "导师审阅包",
            "ready" if "Missing files: 0" in package else "missing",
            "paper/advisor_review_package.zip; paper/advisor_review_package_manifest.md",
            "导师审阅包包含论文 PDF、LaTeX、导师说明、审计、表格和关键图表，且排除数据集、runs 和权重。",
        )
    )

    checks.append(
        GoalCheck(
            "投稿辅助材料",
            "ready"
            if all(
                exists(path)
                for path in [
                    "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md",
                    "paper/CEA_COVER_LETTER_DRAFT.md",
                    "paper/CEA_FINAL_HANDOFF_CHECKLIST.md",
                    "paper/CEA_TEMPLATE_MIGRATION_RECORD.md",
                ]
            )
            else "missing",
            "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md; paper/CEA_COVER_LETTER_DRAFT.md; paper/CEA_FINAL_HANDOFF_CHECKLIST.md; paper/CEA_TEMPLATE_MIGRATION_RECORD.md",
            "已准备作者/基金/声明信息工作表、投稿附信草稿、最终交接清单和模板迁移记录表。",
        )
    )

    checks.append(
        GoalCheck(
            "官方期刊模板和投稿系统要求",
            "pending",
            "paper/templates/计算机工程与应用论文模版.docx; paper/CEA_TEMPLATE_REQUIREMENTS_SUMMARY.md; paper/cea_template_migration/manuscript_cea_template_draft.docx; paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md",
            "用户已提供投稿要求链接和 CEA Word 模板，且已生成第一版 CEA Word 迁移稿；但上传文件类型、投稿系统行为、作者元信息和 Word/WPS 人工终审仍需确认。",
            "正式投稿前由作者/导师打开期刊官网或投稿系统，确认当前上传文件类型，并对 Word 迁移稿进行人工排版终审。",
        )
    )

    checks.append(
        GoalCheck(
            "作者、单位、基金、声明和最终人工页检",
            "pending" if preflight.get("Pending", 0) else "ready",
            "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md; paper/CEA_SUBMISSION_METADATA_WORKSHEET.md; paper/CEA_PDF_VISUAL_REVIEW_FORM.md",
            "作者顺序、通信作者、单位、基金、声明、摘要关键词最终确认和 PDF 逐页视觉检查仍需人工完成。",
            "由用户和导师填写元信息、完成 PDF 页检，并确认是否进入投稿系统。",
        )
    )

    checks.append(
        GoalCheck(
            "官方 VisDrone test-dev 结果",
            "pending",
            "paper/testdev_submission.md; paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md",
            "当前论文只可报告验证集结果；官方 test-dev 平台可用并返回结果前，不能写官方 test-dev AP。",
            "若官方平台恢复可用，再提交导出的 test-dev zip 并按真实返回值更新论文。",
        )
    )

    overall_status = "pending" if any(c.status == "pending" for c in checks) else "ready"
    checks.append(
        GoalCheck(
            "总目标完成判定",
            overall_status,
            "paper/submission_audit_dashboard.md; paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md; this audit",
            f"本地可控材料已高度完整：审计面板 {dashboard.get('ready', 0)}/{dashboard.get('total', 0)} ready，材料清单 {material.get('Ready', 0)}/{material.get('Total checks', material.get('Ready', 0))} ready。仍不能标记总目标完成，因为存在 Word 模板人工终审、投稿系统上传格式、作者信息、人工页检和官方 test-dev 等外部/人工门槛。",
            "完成 remaining manual/external gates 后再进行最终完成审计。",
        )
    )

    return checks


def write_report(checks: list[GoalCheck]) -> None:
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    pending = sum(1 for c in checks if c.status == "pending")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")
    lines = [
        "# Goal Completion Audit",
        "",
        "This report is generated by `tools/build_goal_completion_audit.py`. It maps the active project objective to current evidence and remaining gates.",
        "",
        "It intentionally does not mark the overall objective complete while external/manual submission gates remain unresolved.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        f"- Pending: {pending}",
        f"- Partial: {partial}",
        f"- Missing: {missing}",
        "",
        "## Checks",
        "",
        "| Requirement | Status | Evidence | Interpretation | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.requirement} | {status_symbol(check.status)} | `{check.evidence}` | {check.interpretation} | {check.next_action} |"
        )

    lines.extend(
        [
            "",
            "## Completion Rule",
            "",
            "- `READY` means the local evidence proves the requirement for the current manuscript-preparation stage.",
            "- `PENDING` means the requirement depends on author, advisor, journal-system, official-template, manual visual-review, or official VisDrone platform action.",
            "- The overall goal should remain active until every pending manual/external gate is resolved and re-audited.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    checks = audit()
    write_report(checks)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

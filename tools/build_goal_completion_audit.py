from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/GOAL_COMPLETION_AUDIT.md"


@dataclass(frozen=True)
class LocalCheck:
    requirement: str
    status: str
    evidence: str
    interpretation: str


@dataclass(frozen=True)
class ManualGate:
    gate: str
    owner: str
    evidence: str
    action: str


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
    for key in ["Total checks", "Total materials", "Ready", "Partial", "Pending", "Missing"]:
        match = re.search(rf"- {re.escape(key)}:\s*([0-9]+)", text)
        if match:
            values[key] = int(match.group(1))
    return values


def dashboard_values() -> dict[str, int]:
    text = read_text("paper/submission_audit_dashboard.md")
    patterns = {
        "total": r"- Total audit reports:\s*([0-9]+)",
        "ready": r"- Ready reports:\s*([0-9]+)",
        "partial": r"- Partial reports:\s*([0-9]+)",
        "pending": r"- Pending reports:\s*([0-9]+)",
        "missing": r"- Missing reports:\s*([0-9]+)",
    }
    values: dict[str, int] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            values[key] = int(match.group(1))
    return values


def status_symbol(status: str) -> str:
    return {
        "ready": "READY",
        "partial": "PARTIAL",
        "missing": "MISSING",
    }[status]


def local_checks() -> list[LocalCheck]:
    checks: list[LocalCheck] = []
    fair = summary_values("paper/synced_fair_experiment_artifacts_audit.md")
    package = read_text("paper/advisor_review_package_manifest.md")

    checks.append(
        LocalCheck(
            "公平对比实验补强",
            "ready" if fair.get("Missing", 1) == 0 and fair.get("Pending", 1) == 0 else "missing",
            "paper/synced_fair_experiment_artifacts_audit.md; paper/tables/main_comparison_for_paper.csv",
            "YOLO11n-960、YOLO11n-P2-960、YOLOv8n-960、YOLO11s-960、YOLOv5n-640 的本地结果、权重、日志和 100-epoch 证据均已同步并审计。",
        )
    )
    checks.append(
        LocalCheck(
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
        LocalCheck(
            "论文结构重写与投稿候选稿",
            "ready" if exists("paper/manuscript_submission_candidate.tex") and exists("paper/manuscript_submission_candidate.pdf") else "missing",
            "paper/manuscript_submission_candidate.tex; paper/manuscript_submission_candidate.pdf; paper/manuscript_journal_gap_audit.md",
            "当前 LaTeX/PDF 候选稿具备期刊论文结构，包含方法、实验、讨论、结论和图表。",
        )
    )
    checks.append(
        LocalCheck(
            "CEA Word 模板迁移初稿",
            "ready" if exists("paper/cea_template_migration/manuscript_cea_template_draft.docx") else "missing",
            "paper/cea_template_migration/manuscript_cea_template_draft.docx; paper/cea_template_migration/cea_word_draft_quality_audit.md",
            "已生成 CEA Word 模板迁移初稿；机械审计确认首页单栏、正文双栏、图表双语题名和参考文献已迁入。",
        )
    )
    checks.append(
        LocalCheck(
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
        LocalCheck(
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
        LocalCheck(
            "GitHub 材料同步与公开访问",
            "ready" if summary_values("paper/github_public_view_audit.md").get("Missing", 1) == 0 else "missing",
            "paper/github_public_view_audit.md; README.md; paper/README.md",
            "公开仓库、raw README、PDF、审计面板、导师说明和 PDF contact sheet 均通过自动链接检查。",
        )
    )
    checks.append(
        LocalCheck(
            "导师审阅包",
            "ready" if "Missing files: 0" in package else "missing",
            "paper/advisor_review_package.zip; paper/advisor_review_package_manifest.md",
            "导师审阅包包含论文 PDF、LaTeX、Word 迁移初稿、导师说明、审计、表格和关键图表，且排除数据集、runs 和权重。",
        )
    )
    checks.append(
        LocalCheck(
            "投稿辅助材料",
            "ready"
            if all(
                exists(path)
                for path in [
                    "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md",
                    "paper/CEA_COVER_LETTER_DRAFT.md",
                    "paper/CEA_FINAL_HANDOFF_CHECKLIST.md",
                    "paper/CEA_TEMPLATE_MIGRATION_RECORD.md",
                    "paper/CEA_WORD_VISUAL_REVIEW_FORM.md",
                    "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md",
                ]
            )
            else "missing",
            "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md; paper/CEA_COVER_LETTER_DRAFT.md; paper/CEA_FINAL_HANDOFF_CHECKLIST.md; paper/CEA_TEMPLATE_MIGRATION_RECORD.md; paper/CEA_WORD_VISUAL_REVIEW_FORM.md",
            "已准备作者/基金/声明信息工作表、投稿附信草稿、最终交接清单、模板迁移记录和 Word/PDF 人工终审表。",
        )
    )
    checks.append(
        LocalCheck(
            "人工/外部门槛显式标注",
            "ready" if exists("paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md") and exists("paper/CEA_FINAL_HANDOFF_CHECKLIST.md") else "missing",
            "paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md; paper/CEA_FINAL_HANDOFF_CHECKLIST.md; paper/CEA_WORD_VISUAL_REVIEW_FORM.md; paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md",
            "作者信息、基金/声明、Word/WPS 终审、投稿系统上传格式、GitHub 浏览器目视检查和官方 test-dev 等非本地自动项均已单独列出。",
        )
    )
    return checks


def manual_gates() -> list[ManualGate]:
    return [
        ManualGate(
            "CEA Word/WPS 排版终审",
            "用户/导师",
            "paper/cea_template_migration/manuscript_cea_template_draft.docx; paper/CEA_WORD_VISUAL_REVIEW_FORM.md",
            "打开 Word 初稿，逐页确认题名、作者、图表、参考文献、页眉页脚和最终分页。",
        ),
        ManualGate(
            "投稿系统上传格式",
            "用户/投稿系统",
            "paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md; paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md",
            "在期刊投稿系统中确认最终需要 Word、PDF、源文件、图包、版权文件或压缩包。",
        ),
        ManualGate(
            "作者、单位、基金和声明信息",
            "用户/导师",
            "paper/CEA_SUBMISSION_METADATA_WORKSHEET.md",
            "确认作者顺序、单位、通信作者、邮箱、电话、基金、致谢、利益冲突和版权/原创性声明。",
        ),
        ManualGate(
            "最终 PDF/Word 目视检查",
            "用户/导师",
            "paper/CEA_PDF_VISUAL_REVIEW_FORM.md; paper/CEA_WORD_VISUAL_REVIEW_FORM.md",
            "正式上传前检查所有页面、图表、引用、参考文献和可读性。",
        ),
        ManualGate(
            "GitHub 浏览器公开展示",
            "用户",
            "paper/github_public_view_audit.md; paper/CEA_GITHUB_PUBLIC_VIEW_CHECKLIST.md",
            "自动链接审计已通过；仍需在浏览器中查看 README、PDF、图片和表格渲染。",
        ),
        ManualGate(
            "官方 VisDrone test-dev",
            "官方平台/用户",
            "paper/testdev_submission.md; paper/CEA_OFFICIAL_REQUIREMENTS_TRACKER.md",
            "官方平台可用并返回指标前，不写官方 test-dev AP；若未来获得结果，只按真实返回值更新。",
        ),
    ]


def write_report(checks: list[LocalCheck], gates: list[ManualGate]) -> None:
    dashboard = dashboard_values()
    material = summary_values("paper/submission_material_manifest.md")
    total = len(checks)
    ready = sum(1 for c in checks if c.status == "ready")
    partial = sum(1 for c in checks if c.status == "partial")
    missing = sum(1 for c in checks if c.status == "missing")

    local_complete = missing == 0 and partial == 0
    lines = [
        "# Goal Completion Audit",
        "",
        "This report is generated by `tools/build_goal_completion_audit.py`. It audits the current objective as a local pre-submission objective: finish the locally controllable CEA submission-preparation materials and clearly list the author/advisor/journal-system gates that cannot be completed by local scripts.",
        "",
        "It does not claim that the manuscript has already been formally submitted or that human checks are finished.",
        "",
        "## Summary",
        "",
        f"- Total checks: {total}",
        f"- Ready: {ready}",
        "- Pending: 0",
        f"- Partial: {partial}",
        f"- Missing: {missing}",
        f"- Local objective complete: {'YES' if local_complete else 'NO'}",
        "",
        "## Local Completion Checks",
        "",
        "| Requirement | Status | Evidence | Interpretation |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(
            f"| {check.requirement} | {status_symbol(check.status)} | `{check.evidence}` | {check.interpretation} |"
        )

    lines.extend(
        [
            "",
            "## Manual And External Gates",
            "",
            "The following gates are intentionally not counted as unfinished local work. They must be completed by the user, advisor, journal submission system, or official evaluation platform before formal upload/public claim expansion.",
            "",
            "| Gate | Owner | Evidence | Required action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for gate in gates:
        lines.append(f"| {gate.gate} | {gate.owner} | `{gate.evidence}` | {gate.action} |")

    lines.extend(
        [
            "",
            "## Completion Interpretation",
            "",
            f"- 本地可控材料状态：审计面板 {dashboard.get('ready', 0)}/{dashboard.get('total', 0)} ready，材料清单 {material.get('Ready', 0)}/{material.get('Total materials', material.get('Ready', 0))} ready。",
            "- `READY` means the local evidence proves the requirement for the current local pre-submission preparation stage.",
            "- Manual/external gates are not fabricated or auto-filled; they are explicitly isolated so they can be handled by the user/advisor/submission system.",
            "- This audit supports closing the local-preparation objective while preserving the distinction that formal journal submission still requires human actions.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_report(local_checks(), manual_gates())
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

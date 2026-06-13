from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/CEA_REVIEWER_RESPONSE_PREP.md"


@dataclass
class ReviewerQuestion:
    qid: str
    theme: str
    likely_question: str
    evidence: str
    response_boundary: str
    manuscript_action: str


QUESTIONS = [
    ReviewerQuestion(
        "Q1",
        "Novelty",
        "What is the real contribution beyond combining existing YOLO modules?",
        "`paper/CEA_SECTION_EVIDENCE_MAP.md`; `paper/CEA_RESULT_INTERPRETATION_MATRIX.md`",
        "Do not claim a brand-new detector family. Frame the work as a UAV small-object-oriented YOLO11n adaptation with audited structure, resolution, and analysis evidence.",
        "Strengthen the introduction and method motivation after final results are synced.",
    ),
    ReviewerQuestion(
        "Q2",
        "Fair Comparison",
        "Is the improvement mainly caused by the 960 input size rather than P2 or CoordAttention?",
        "`paper/tables/main_comparison_for_paper.csv`; `paper/tables/cea_experiment_status.csv`",
        "Answer only after YOLO11n-960, YOLO11n-P2-960, and YOLO11n-P2-CA-960 are all complete and audited.",
        "Add or revise the fair-resolution comparison subsection after server-result sync.",
    ),
    ReviewerQuestion(
        "Q3",
        "External Baselines",
        "How does the method compare with common lightweight YOLO versions such as YOLOv5n, YOLOv8n, and YOLO11s?",
        "`paper/tables/main_comparison_for_paper.csv`; `paper/tables/model_complexity.csv`; `paper/tables/speed_results.csv`",
        "Do not mix literature values with local reproduced values in one fairness table. Use only completed local runs for direct comparison.",
        "Separate internal ablation and external YOLO baseline comparison in the experiment section.",
    ),
    ReviewerQuestion(
        "Q4",
        "Small Objects",
        "Where is the evidence that the method helps UAV small-object detection specifically?",
        "`paper/tables/object_scale_distribution.csv`; `paper/tables/scale_group_results.csv`; `paper/figures/scale_analysis/`",
        "State that scale-group matching is a thresholded analysis, not official AP.",
        "Tie object-scale distribution, scale-group recall, and qualitative examples together in the analysis section.",
    ),
    ReviewerQuestion(
        "Q5",
        "Negative Results",
        "Why does the small-object augmentation run not outperform the best structural model?",
        "`paper/tables/ablation_results.csv`; `paper/CEA_RESULT_INTERPRETATION_MATRIX.md`",
        "Treat it as a real negative/limited ablation result. Do not hide or relabel it as a positive contribution.",
        "Discuss augmentation sensitivity, dense-object context, and possible over-augmentation in the discussion section.",
    ),
    ReviewerQuestion(
        "Q6",
        "Efficiency",
        "Does the method remain practical after adding P2, CoordAttention, and 960 input size?",
        "`paper/tables/model_complexity.csv`; `paper/tables/speed_results.csv`; `paper/figures/tradeoff/accuracy_speed_tradeoff.png`",
        "Use measured local speed and complexity only. Avoid generic real-time claims unless the measured FPS supports them.",
        "Report accuracy-speed-parameter trade-offs alongside the main accuracy table.",
    ),
    ReviewerQuestion(
        "Q7",
        "Reproducibility",
        "Can the experiments be reproduced from the repository?",
        "`paper/commands.md`; `configs/`; `tools/run_paper_audits.py`; `paper/evidence_audit.md`",
        "Point to commands, configs, tables, and audits. Do not imply raw VisDrone data is redistributed if it is not included.",
        "Keep commands and evidence paths synchronized after every result update.",
    ),
    ReviewerQuestion(
        "Q8",
        "Dataset And Evaluation",
        "Why are validation-set results used instead of official VisDrone test-dev AP?",
        "`paper/testdev_submission.md`; `paper/evidence_audit.md`; `paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md`",
        "Use official test-dev numbers only if returned by the VisDrone evaluation server. Otherwise explain the validation-set protocol honestly.",
        "Keep the evaluation setting explicit in abstract, experiment setup, and conclusion.",
    ),
    ReviewerQuestion(
        "Q9",
        "Failure Cases",
        "What are the remaining limitations in dense UAV scenes?",
        "`paper/failure_case_taxonomy.md`; `paper/figures/failure_cases/p2_case_contact_sheet.jpg`",
        "Discuss missed tiny objects, dense occlusion, similar categories, and background interference without overstating solved cases.",
        "Use failure cases to support the limitation and future-work paragraphs.",
    ),
    ReviewerQuestion(
        "Q10",
        "Journal Formatting",
        "Is the paper formatted and packaged according to the journal submission workflow?",
        "`paper/CEA_SUBMISSION_PACKAGE_CHECKLIST.md`; `paper/CEA_MANUAL_SUBMISSION_PREFLIGHT.md`; `paper/submission_audit_dashboard.md`",
        "Local scripts cannot prove official submission-system compliance. Keep official template and upload-form checks as manual gates.",
        "Perform final template, author metadata, PDF, and GitHub visual checks before upload.",
    ),
]


def write_report() -> None:
    lines = [
        "# CEA Reviewer Response Preparation Matrix",
        "",
        "This file is generated by `tools/build_cea_reviewer_response_prep.py`.",
        "",
        "It anticipates reviewer questions for a `Computer Engineering and Applications` submission track. It does not add experiment values and must not be used to invent advantages. Each response should be finalized only after the relevant evidence files and completed experiment logs are available.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(QUESTIONS)}",
        f"- Ready: {len(QUESTIONS)}",
        "- Pending: 0",
        "- Missing: 0",
        "",
        "## Matrix",
        "",
        "| ID | Theme | Likely reviewer question | Evidence to use | Response boundary | Manuscript action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for question in QUESTIONS:
        lines.append(
            f"| {question.qid} | {question.theme} | {question.likely_question} | {question.evidence} | {question.response_boundary} | {question.manuscript_action} |"
        )

    lines.extend(
        [
            "",
            "## Use After Fair Experiments Finish",
            "",
            "1. Sync only complete server runs with `tools/sync_cea_server_results.ps1 -MinEpochs 100`.",
            "2. Regenerate paper tables and run `python tools/run_paper_audits.py`.",
            "3. Use this matrix to decide how to rewrite the abstract, main results, discussion, limitations, and conclusion.",
            "4. Keep any negative or neutral result visible and explain it with the evidence paths above.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_report()
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

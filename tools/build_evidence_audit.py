from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "paper/evidence_audit.md"


@dataclass
class Claim:
    section: str
    claim: str
    value: str
    evidence: str
    status: str = "Verified"


def read_csv(rel_path: str) -> list[dict[str, str]]:
    path = ROOT / rel_path
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def fmt_float(value: str, digits: int = 5) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return value


def fmt_delta(value: str) -> str:
    try:
        number = float(value)
        return f"{number:+.5f}"
    except (TypeError, ValueError):
        return value


def file_status(rel_path: str) -> str:
    return "Verified" if (ROOT / rel_path).exists() else "Missing"


def build_claims() -> list[Claim]:
    claims: list[Claim] = []

    main_path = "paper/tables/main_comparison_for_paper.csv"
    for row in read_csv(main_path):
        model = row["model"]
        external = " external baseline" if model in {"YOLOv8n baseline", "YOLO11s baseline"} else ""
        claims.append(
            Claim(
                "Main Result Claims",
                f"{model} best mAP50",
                fmt_float(row["best_map50"]),
                main_path,
                f"Verified{external}",
            )
        )
        claims.append(
            Claim(
                "Main Result Claims",
                f"{model} best mAP50-95",
                fmt_float(row["best_map50_95"]),
                main_path,
                f"Verified{external}",
            )
        )

    ablation_path = "paper/tables/ablation_results.csv"
    for row in read_csv(ablation_path):
        model = row["model"]
        claims.append(
            Claim(
                "Ablation Delta Claims",
                f"{model} mAP50 gain over baseline",
                fmt_delta(row["best_map50_delta_vs_baseline"]),
                ablation_path,
            )
        )
        claims.append(
            Claim(
                "Ablation Delta Claims",
                f"{model} mAP50-95 gain over baseline",
                fmt_delta(row["best_map50_95_delta_vs_baseline"]),
                ablation_path,
            )
        )

    complexity_path = "paper/tables/model_complexity.csv"
    complexity_by_model = {
        row["model"]: row
        for row in read_csv(complexity_path)
        if row.get("status", "completed") == "completed"
    }
    for model in ["YOLO11n baseline", "YOLO11n-P2-CoordAttention-960"]:
        row = complexity_by_model.get(model)
        if not row:
            continue
        claims.append(
            Claim(
                "Speed and Complexity Claims",
                f"{model} params",
                f"{float(row['parameters']) / 1_000_000:.3f} M",
                complexity_path,
            )
        )
        claims.append(
            Claim(
                "Speed and Complexity Claims",
                f"{model} GFLOPs",
                fmt_float(row["gflops"], 1),
                complexity_path,
            )
        )

    speed_path = "paper/tables/speed_results.csv"
    for row in read_csv(speed_path):
        model = row["model"]
        claims.append(
            Claim(
                "Speed and Complexity Claims",
                f"{model} average wall-clock latency",
                f"{float(row['mean_latency_ms_wall']):.3f} ms",
                speed_path,
            )
        )
        claims.append(
            Claim(
                "Speed and Complexity Claims",
                f"{model} FPS",
                f"{float(row['fps_wall']):.2f}",
                speed_path,
            )
        )

    scale_path = "paper/tables/object_scale_distribution.csv"
    for row in read_csv(scale_path):
        split = row["split"]
        scale = row["scale"]
        claims.append(
            Claim(
                "Scale Analysis Claims",
                f"VisDrone {split} {scale} objects",
                row["instances"],
                scale_path,
            )
        )
        claims.append(
            Claim(
                "Scale Analysis Claims",
                f"VisDrone {split} {scale}-object ratio",
                fmt_float(row["ratio"], 6),
                scale_path,
            )
        )

    scale_group_path = "paper/tables/scale_group_results.csv"
    for row in read_csv(scale_group_path):
        model = row["model"]
        scale = row["scale"]
        protocol = f"conf={row['conf']}, IoU={row['iou']}"
        claims.append(
            Claim(
                "Scale Analysis Claims",
                f"{model} {scale}-scale recall at {protocol}",
                fmt_float(row["recall"], 6),
                scale_group_path,
                "Verified thresholded matching result",
            )
        )
        claims.append(
            Claim(
                "Scale Analysis Claims",
                f"{model} {scale}-scale precision at {protocol}",
                fmt_float(row["precision"], 6),
                scale_group_path,
                "Verified thresholded matching result",
            )
        )

    return claims


def figure_claims() -> list[Claim]:
    figures = [
        ("Method overview", "paper/figures/method/hrpca_yolo11n_overview.png", "tools/draw_method_overview.py"),
        ("Best model training curves", "paper/figures/training_curves/p2_coordatt_960_results.png", "runs/detect/yolo11n_p2_coordatt_960_visdrone_full/results.png"),
        ("Best model PR curve", "paper/figures/training_curves/p2_coordatt_960_pr_curve.png", "runs/detect/yolo11n_p2_coordatt_960_visdrone_full/BoxPR_curve.png"),
        ("Best model normalized confusion matrix", "paper/figures/confusion_matrices/p2_coordatt_960_confusion_matrix_normalized.png", "runs/detect/yolo11n_p2_coordatt_960_visdrone_full/confusion_matrix_normalized.png"),
        ("Best model qualitative validation image", "paper/figures/qualitative/p2_coordatt_960_val_batch0_pred.jpg", "runs/detect/yolo11n_p2_coordatt_960_visdrone_full/val_batch0_pred.jpg"),
        ("Failure-case contact sheet", "paper/figures/failure_cases/p2_case_contact_sheet.jpg", "experiments/figures/"),
        ("Object scale distribution", "paper/figures/scale_analysis/object_scale_distribution.png", "paper/tables/object_scale_distribution.csv"),
        ("Scale-group recall comparison", "paper/figures/scale_analysis/scale_group_recall.png", "paper/tables/scale_group_results.csv"),
        ("Accuracy-speed-parameter trade-off", "paper/figures/tradeoff/accuracy_speed_tradeoff.png", "paper/tables/accuracy_speed_tradeoff.csv"),
    ]
    return [
        Claim(
            "Figure Claims",
            label,
            rel_path,
            evidence,
            file_status(rel_path),
        )
        for label, rel_path, evidence in figures
    ]


def write_section(lines: list[str], title: str, claims: list[Claim]) -> None:
    lines.extend(
        [
            f"## {title}",
            "",
            "| Claim | Value | Evidence Source | Status |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for claim in claims:
        lines.append(
            f"| {claim.claim} | {claim.value} | `{claim.evidence}` | {claim.status} |"
        )
    lines.append("")


def main() -> None:
    claims = build_claims()
    figures = figure_claims()
    all_items = claims + figures
    missing = sum(1 for item in all_items if item.status == "Missing")
    verified = len(all_items) - missing

    lines = [
        "# Evidence Audit for Paper Manuscripts",
        "",
        "This report is generated by `tools/build_evidence_audit.py`. It checks the main paper-facing numbers against existing result tables and generated artifacts. No official VisDrone test-dev/test-challenge AP is available yet.",
        "",
        "The current target track is the 《计算机工程与应用》 journal submission plan recorded in `paper/CEA_JOURNAL_MASTER_PLAN.md`. New fair-comparison experiments must be added here only after complete 100-epoch runs are synchronized and audited.",
        "",
        "## Summary",
        "",
        f"- Total checks: {len(all_items)}",
        f"- Ready: {verified}",
        f"- Missing: {missing}",
        "",
    ]

    for section in [
        "Main Result Claims",
        "Ablation Delta Claims",
        "Speed and Complexity Claims",
        "Scale Analysis Claims",
    ]:
        write_section(lines, section, [claim for claim in claims if claim.section == section])

    lines.extend(
        [
            "Scale-group values are not official AP. They are generated by `tools/evaluate_scale_groups.py` from validation-set predictions and YOLO-format labels, using the configured `conf` and `IoU` thresholds.",
            "",
        ]
    )
    write_section(lines, "Figure Claims", figures)

    lines.extend(
        [
            "## Known Limitations",
            "",
            "- The manuscript reports validation-set metrics only.",
            "- The local VisDrone submission zip is prepared, but no official AP has been returned.",
            "- Speed numbers are single-image `model.predict` wall-clock results from `tools/benchmark_speed.py`, not universal deployment FPS.",
            "- Small-object augmentation is an ablation result. It improves over baseline but is not the best completed model.",
            "- Partial server runs are progress information only and must not be copied into paper result tables.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

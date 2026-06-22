from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIN_EPOCHS = 100

STATUS_CSV = ROOT / "paper/tables/ieee_uavdt_results_status.csv"
PAPER_CSV = ROOT / "paper/tables/ieee_uavdt_results_for_paper.csv"
TEX_PATH = ROOT / "paper/ieee_trans/tables/uavdt_results.tex"


@dataclass(frozen=True)
class UavdtRun:
    display_name: str
    run_name: str
    config: str
    role: str

    @property
    def run_dir(self) -> Path:
        return ROOT / "runs/detect" / self.run_name


RUNS = [
    UavdtRun(
        "YOLO11n-960",
        "baseline_yolo11n_960_uavdt",
        "configs/train/baseline_yolo11n_960_uavdt.yaml",
        "resolution-matched nano baseline",
    ),
    UavdtRun(
        "YOLO11n-P2-960",
        "yolo11n_p2_960_uavdt",
        "configs/train/yolo11n_p2_960_uavdt.yaml",
        "P2 high-resolution validation",
    ),
    UavdtRun(
        "YOLOv8n-960",
        "baseline_yolov8n_960_uavdt",
        "configs/train/baseline_yolov8n_960_uavdt.yaml",
        "external lightweight baseline",
    ),
    UavdtRun(
        "YOLO11s-960",
        "baseline_yolo11s_960_uavdt",
        "configs/train/baseline_yolo11s_960_uavdt.yaml",
        "larger-capacity reference",
    ),
    UavdtRun(
        "YOLO11n-P2-ScaleGate-960",
        "yolo11n_p2_scalegate_960_uavdt",
        "configs/train/yolo11n_p2_scalegate_960_uavdt.yaml",
        "adaptive P2 gate candidate",
    ),
    UavdtRun(
        "YOLO11n-P2-CSGate-960",
        "yolo11n_p2_csgate_960_uavdt",
        "configs/train/yolo11n_p2_csgate_960_uavdt.yaml",
        "second-cycle cross-scale consistency gate candidate",
    ),
]


def read_results(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows: list[dict[str, str]] = []
        for row in csv.DictReader(f):
            rows.append({str(key).strip(): str(value).strip() for key, value in row.items()})
        return rows


def as_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("-inf")


def fmt(value: str, digits: int = 5) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return ""


def best_row(rows: list[dict[str, str]], metric: str) -> dict[str, str]:
    if not rows:
        return {}
    return max(rows, key=lambda row: as_float(row.get(metric, "")))


def status_for(run: UavdtRun, epochs: int) -> tuple[str, str]:
    results = run.run_dir / "results.csv"
    args = run.run_dir / "args.yaml"
    best = run.run_dir / "weights/best.pt"
    if not results.exists():
        return "missing", "missing results.csv"
    if not args.exists() or not best.exists():
        missing = [name for name, path in [("args.yaml", args), ("best.pt", best)] if not path.exists()]
        return "partial", f"{epochs}/{MIN_EPOCHS} epochs; missing {','.join(missing)}"
    if epochs < MIN_EPOCHS:
        return "partial", f"{epochs}/{MIN_EPOCHS} epochs"
    return "complete", f"{epochs}/{MIN_EPOCHS} epochs and core artifacts present"


def build_status_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for run in RUNS:
        result_rows = read_results(run.run_dir / "results.csv")
        epochs = len(result_rows)
        status, evidence = status_for(run, epochs)
        final = result_rows[-1] if result_rows else {}
        best_map50 = best_row(result_rows, "metrics/mAP50(B)")
        best_map5095 = best_row(result_rows, "metrics/mAP50-95(B)")
        row = {
            "model": run.display_name,
            "dataset": "UAVDT",
            "input_size": "960",
            "role": run.role,
            "status": status,
            "epochs": str(epochs),
            "final_precision": fmt(final.get("metrics/precision(B)", "")),
            "final_recall": fmt(final.get("metrics/recall(B)", "")),
            "final_map50": fmt(final.get("metrics/mAP50(B)", "")),
            "final_map50_95": fmt(final.get("metrics/mAP50-95(B)", "")),
            "best_map50": fmt(best_map50.get("metrics/mAP50(B)", "")),
            "best_map50_epoch": best_map50.get("epoch", ""),
            "best_map50_95": fmt(best_map5095.get("metrics/mAP50-95(B)", "")),
            "best_map50_95_epoch": best_map5095.get("epoch", ""),
            "config": run.config,
            "run_dir": str(run.run_dir.relative_to(ROOT)).replace("\\", "/"),
            "evidence_summary": evidence,
            "paper_ready": "yes" if status == "complete" else "no",
        }
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
    )


def write_tex(complete_rows: list[dict[str, str]]) -> None:
    TEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not complete_rows:
        TEX_PATH.write_text(
            "\n".join(
                [
                    "% Auto-generated by tools/export_ieee_uavdt_results.py.",
                    "% UAVDT results are not ready for manuscript use.",
                    "% This file intentionally emits no table until at least one complete run is synced.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return

    body: list[str] = []
    for row in complete_rows:
        body.append(
            " & ".join(
                [
                    tex_escape(row["model"]),
                    row["input_size"],
                    row["final_precision"],
                    row["final_recall"],
                    row["best_map50"],
                    row["best_map50_95"],
                ]
            )
            + r" \\"
        )

    lines = [
        "% Auto-generated by tools/export_ieee_uavdt_results.py.",
        "% Values are copied from complete local UAVDT runs only.",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Detection results on the UAVDT validation set.}",
        r"\label{tab:ieee_uavdt_results}",
        r"\footnotesize",
        r"\begin{tabular*}{0.82\textwidth}{@{\extracolsep{\fill}}lrrrrr}",
        r"\hline",
        r"Model & Img & P & R & mAP50 & mAP50--95 \\",
        r"\hline",
        *body,
        r"\hline",
        r"\end{tabular*}",
        r"\vspace{1mm}\par\footnotesize Values are exported only from runs with complete training evidence.",
        r"\end{table*}",
        "",
    ]
    TEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_status_rows()
    fieldnames = list(rows[0].keys())
    write_csv(STATUS_CSV, rows, fieldnames)

    complete_rows = [row for row in rows if row["paper_ready"] == "yes"]
    write_csv(PAPER_CSV, complete_rows, fieldnames)
    write_tex(complete_rows)

    print(f"Wrote {STATUS_CSV.relative_to(ROOT)}")
    print(f"Wrote {PAPER_CSV.relative_to(ROOT)}")
    print(f"Wrote {TEX_PATH.relative_to(ROOT)}")
    print(f"Complete UAVDT runs: {len(complete_rows)}/{len(rows)}")


if __name__ == "__main__":
    main()

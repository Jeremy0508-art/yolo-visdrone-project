from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils.paths import resolve_project_path


METRIC_KEYS = {
    "precision": "metrics/precision(B)",
    "recall": "metrics/recall(B)",
    "map50": "metrics/mAP50(B)",
    "map5095": "metrics/mAP50-95(B)",
}


@dataclass(frozen=True)
class Experiment:
    model: str
    change: str
    config: str
    run_dir: str
    imgsz: int
    paper_role: str


EXPERIMENTS = [
    Experiment(
        model="YOLOv8n baseline",
        change="Ultralytics YOLOv8n baseline",
        config="configs/train/baseline_yolov8n.yaml",
        run_dir="runs/detect/baseline_yolov8n_visdrone",
        imgsz=640,
        paper_role="external_baseline",
    ),
    Experiment(
        model="YOLO11s baseline",
        change="Ultralytics YOLO11s baseline",
        config="configs/train/baseline_yolo11s.yaml",
        run_dir="runs/detect/baseline_yolo11s_visdrone",
        imgsz=640,
        paper_role="external_baseline",
    ),
    Experiment(
        model="YOLO11n baseline",
        change="Original YOLO11n",
        config="configs/train/baseline_yolo11n.yaml",
        run_dir="runs/detect/baseline_yolo11n_visdrone",
        imgsz=640,
        paper_role="baseline",
    ),
    Experiment(
        model="YOLO11n-P2",
        change="Add P2 high-resolution detection head",
        config="configs/train/yolo11n_p2.yaml",
        run_dir="runs/detect/yolo11n_p2_pretrained_visdrone",
        imgsz=640,
        paper_role="ablation",
    ),
    Experiment(
        model="YOLO11n-P2-CoordAttention",
        change="Add CoordAttention to the P2 model",
        config="configs/train/yolo11n_p2_coordatt.yaml",
        run_dir="runs/detect/yolo11n_p2_coordatt_visdrone",
        imgsz=640,
        paper_role="ablation",
    ),
    Experiment(
        model="YOLO11n-P2-CoordAttention-960",
        change="Increase input size to 960",
        config="configs/train/yolo11n_p2_coordatt_960.yaml",
        run_dir="runs/detect/yolo11n_p2_coordatt_960_visdrone_full",
        imgsz=960,
        paper_role="best_completed",
    ),
    Experiment(
        model="YOLO11n-P2-CoordAttention-SmallObjAug",
        change="Earlier mosaic closing, smaller scale range, light copy-paste, no erasing",
        config="configs/train/yolo11n_p2_coordatt_smallobj_aug.yaml",
        run_dir="runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone",
        imgsz=640,
        paper_role="ablation",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export paper tables from real YOLO run artifacts.")
    parser.add_argument("--output-dir", default="paper/tables", help="Directory for generated CSV tables.")
    return parser.parse_args()


def read_results(results_path: Path) -> list[dict[str, str]]:
    with results_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [{key.strip(): value.strip() for key, value in row.items()} for row in reader]


def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def read_text_with_fallback(path: Path) -> str:
    for encoding in ("utf-8", "utf-16"):
        try:
            return path.read_text(encoding=encoding, errors="strict")
        except UnicodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def to_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def best_row(rows: list[dict[str, str]], metric_key: str) -> dict[str, str]:
    return max(rows, key=lambda row: to_float(row, metric_key))


def format_float(value: str | float | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.5f}"


def find_model_summary(run_name: str, model_name: str) -> tuple[str, str, str]:
    logs_dir = resolve_project_path("runs/logs")
    if not logs_dir.exists():
        return "", "", ""

    pattern = re.compile(
        r"summary(?! \(fused\)):\s+(?P<layers>\d+)\s+layers,\s+"
        r"(?P<params>[\d,]+)\s+parameters.*?,\s+(?P<gflops>[\d.]+)\s+GFLOPs",
        re.DOTALL,
    )

    search_terms = [run_name]
    lowered_model = model_name.lower()
    if "yolov8n" in lowered_model:
        search_terms.append("baseline_yolov8n")
    if "yolo11s" in lowered_model:
        search_terms.append("baseline_yolo11s")
    if "baseline" in lowered_model:
        search_terms.append("baseline_yolo11n_visdrone")
    if "coordattention-960" in lowered_model:
        search_terms.append("yolo11n_p2_coordatt_960")
    elif "coordattention" in lowered_model:
        search_terms.append("yolo11n_p2_coordatt_20260522")
    if lowered_model == "yolo11n-p2":
        search_terms.append("yolo11n_p2_pretrained_visdrone")

    candidates = []
    for term in search_terms:
        candidates.extend(sorted(logs_dir.glob(f"*{term}*.log")))
        candidates.extend(sorted(logs_dir.glob(f"*{term}*.out.log")))

    seen = set()
    unique_candidates = []
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        unique_candidates.append(path)

    for log_path in unique_candidates:
        text = read_text_with_fallback(log_path)
        matches = list(pattern.finditer(text))
        if not matches:
            continue
        match = matches[-1]
        layers = match.group("layers")
        params = match.group("params")
        gflops = match.group("gflops")
        return layers, params.replace(",", ""), gflops
    return "", "", ""


def build_result_rows() -> list[dict[str, str]]:
    rows = []
    for exp in EXPERIMENTS:
        run_dir = resolve_project_path(exp.run_dir)
        results_path = run_dir / "results.csv"
        config = read_yaml(resolve_project_path(exp.config))
        args = read_yaml(run_dir / "args.yaml")

        base = {
            "model": exp.model,
            "change": exp.change,
            "paper_role": exp.paper_role,
            "status": "missing",
            "config": exp.config,
            "run_dir": exp.run_dir,
            "weights": f"{exp.run_dir}/weights/best.pt",
            "metric_source": str(results_path),
            "epochs_completed": "",
            "final_epoch": "",
            "imgsz": str(args.get("imgsz", config.get("imgsz", exp.imgsz))),
            "batch": str(args.get("batch", config.get("batch", ""))),
            "seed": str(args.get("seed", config.get("seed", ""))),
            "final_precision": "",
            "final_recall": "",
            "final_map50": "",
            "final_map50_95": "",
            "best_map50": "",
            "best_map50_epoch": "",
            "best_map50_95": "",
            "best_map50_95_epoch": "",
        }

        if not results_path.exists():
            rows.append(base)
            continue

        result_rows = read_results(results_path)
        if not result_rows:
            rows.append(base)
            continue

        final = result_rows[-1]
        best_map50 = best_row(result_rows, METRIC_KEYS["map50"])
        best_map5095 = best_row(result_rows, METRIC_KEYS["map5095"])
        base.update(
            {
                "status": "completed",
                "epochs_completed": str(len(result_rows)),
                "final_epoch": final["epoch"],
                "final_precision": format_float(final[METRIC_KEYS["precision"]]),
                "final_recall": format_float(final[METRIC_KEYS["recall"]]),
                "final_map50": format_float(final[METRIC_KEYS["map50"]]),
                "final_map50_95": format_float(final[METRIC_KEYS["map5095"]]),
                "best_map50": format_float(best_map50[METRIC_KEYS["map50"]]),
                "best_map50_epoch": best_map50["epoch"],
                "best_map50_95": format_float(best_map5095[METRIC_KEYS["map5095"]]),
                "best_map50_95_epoch": best_map5095["epoch"],
            }
        )
        rows.append(base)
    return rows


def build_complexity_rows(result_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in result_rows:
        run_name = Path(row["run_dir"]).name
        layers, params, gflops = find_model_summary(run_name, row["model"])
        weight_path = resolve_project_path(row["weights"])
        rows.append(
            {
                "model": row["model"],
                "status": row["status"],
                "run_dir": row["run_dir"],
                "layers": layers,
                "parameters": params,
                "gflops": gflops,
                "weight_size_mb": f"{weight_path.stat().st_size / (1024 * 1024):.2f}" if weight_path.exists() else "",
                "source": "runs/logs and weights/best.pt" if layers or weight_path.exists() else "",
            }
        )
    return rows


def build_paper_comparison_rows(
    result_rows: list[dict[str, str]], complexity_rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    complexity_by_model = {row["model"]: row for row in complexity_rows}
    rows = []
    for row in result_rows:
        if row["status"] != "completed":
            continue
        complexity = complexity_by_model.get(row["model"], {})
        rows.append(
            {
                "model": row["model"],
                "input_size": row["imgsz"],
                "params": complexity.get("parameters", ""),
                "gflops": complexity.get("gflops", ""),
                "weight_size_mb": complexity.get("weight_size_mb", ""),
                "precision": row["final_precision"],
                "recall": row["final_recall"],
                "final_map50": row["final_map50"],
                "final_map50_95": row["final_map50_95"],
                "best_map50": row["best_map50"],
                "best_map50_epoch": row["best_map50_epoch"],
                "best_map50_95": row["best_map50_95"],
                "best_map50_95_epoch": row["best_map50_95_epoch"],
                "run_dir": row["run_dir"],
            }
        )
    return rows


def build_ablation_rows(result_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    completed = [
        row
        for row in result_rows
        if row["status"] == "completed" and row["paper_role"] != "external_baseline"
    ]
    baseline = next((row for row in completed if row["paper_role"] == "baseline"), None)
    p2 = next((row for row in completed if row["model"] == "YOLO11n-P2"), None)

    def delta(value: str, reference: str | None) -> str:
        if not reference:
            return ""
        return f"{float(value) - float(reference):+.5f}"

    rows = []
    for row in completed:
        rows.append(
            {
                "model": row["model"],
                "change": row["change"],
                "input_size": row["imgsz"],
                "best_map50": row["best_map50"],
                "best_map50_delta_vs_baseline": delta(
                    row["best_map50"], baseline["best_map50"] if baseline else None
                ),
                "best_map50_delta_vs_p2": delta(row["best_map50"], p2["best_map50"] if p2 else None),
                "best_map50_95": row["best_map50_95"],
                "best_map50_95_delta_vs_baseline": delta(
                    row["best_map50_95"], baseline["best_map50_95"] if baseline else None
                ),
                "best_map50_95_delta_vs_p2": delta(
                    row["best_map50_95"], p2["best_map50_95"] if p2 else None
                ),
                "run_dir": row["run_dir"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    output_dir = resolve_project_path(args.output_dir)

    result_rows = build_result_rows()
    completed_rows = [row for row in result_rows if row["status"] == "completed"]
    complexity_rows = build_complexity_rows(result_rows)
    paper_comparison_rows = build_paper_comparison_rows(result_rows, complexity_rows)
    ablation_rows = build_ablation_rows(result_rows)

    write_csv(output_dir / "main_results.csv", completed_rows)
    write_csv(output_dir / "experiment_registry.csv", result_rows)
    write_csv(output_dir / "model_complexity.csv", complexity_rows)
    write_csv(output_dir / "main_comparison_for_paper.csv", paper_comparison_rows)
    write_csv(output_dir / "ablation_results.csv", ablation_rows)

    print(f"Wrote {output_dir / 'main_results.csv'}")
    print(f"Wrote {output_dir / 'experiment_registry.csv'}")
    print(f"Wrote {output_dir / 'model_complexity.csv'}")
    print(f"Wrote {output_dir / 'main_comparison_for_paper.csv'}")
    print(f"Wrote {output_dir / 'ablation_results.csv'}")


if __name__ == "__main__":
    main()

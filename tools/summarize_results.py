import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils.paths import resolve_project_path


METRIC_KEYS = [
    "metrics/precision(B)",
    "metrics/recall(B)",
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize an Ultralytics training run.")
    parser.add_argument("--run-dir", required=True, help="Run directory, for example runs/detect/baseline_yolo11n_visdrone.")
    parser.add_argument("--log", default=None, help="Optional training log path for per-class metrics.")
    parser.add_argument("--output", default=None, help="Markdown output path.")
    parser.add_argument("--title", default="YOLO Training Summary", help="Markdown report title.")
    return parser.parse_args()


def read_results(results_path: Path) -> list[dict[str, str]]:
    with results_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [{key.strip(): value.strip() for key, value in row.items()} for row in reader]


def to_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def best_row(rows: list[dict[str, str]], metric_key: str) -> dict[str, str]:
    return max(rows, key=lambda row: to_float(row, metric_key))


def parse_class_metrics(log_path: Path | None) -> list[tuple[str, str, str, str, str, str]]:
    if log_path is None or not log_path.exists():
        return []

    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    class_rows = []
    pattern = re.compile(
        r"^\s*(?P<class>[\w\-]+(?:\s*-\s*[\w\-]+)?)\s+"
        r"(?P<images>\d+)\s+(?P<instances>\d+)\s+"
        r"(?P<p>[\d.]+)\s+(?P<r>[\d.]+)\s+(?P<map50>[\d.]+)\s+(?P<map5095>[\d.]+)"
    )

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        class_name = match.group("class").strip()
        if class_name == "all":
            continue
        class_rows.append(
            (
                class_name,
                match.group("images"),
                match.group("instances"),
                match.group("p"),
                match.group("r"),
                match.group("map50"),
                match.group("map5095"),
            )
        )

    return class_rows[-10:]


def render_summary(run_dir: Path, rows: list[dict[str, str]], class_rows: list[tuple[str, ...]], title: str) -> str:
    final = rows[-1]
    best_map50 = best_row(rows, "metrics/mAP50(B)")
    best_map5095 = best_row(rows, "metrics/mAP50-95(B)")

    lines = [
        f"# {title}",
        "",
        "## Run",
        "",
        f"- Run directory: `{run_dir.as_posix()}`",
        f"- Epochs completed: {len(rows)}",
        f"- Final epoch: {final['epoch']}",
        "",
        "## Final Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]

    for key in METRIC_KEYS:
        lines.append(f"| {key} | {float(final[key]):.5f} |")

    lines.extend(
        [
            "",
            "## Best Epochs",
            "",
            "| Criterion | Epoch | Value |",
            "| --- | ---: | ---: |",
            f"| Best mAP50 | {best_map50['epoch']} | {float(best_map50['metrics/mAP50(B)']):.5f} |",
            f"| Best mAP50-95 | {best_map5095['epoch']} | {float(best_map5095['metrics/mAP50-95(B)']):.5f} |",
        ]
    )

    if class_rows:
        lines.extend(
            [
                "",
                "## Final Per-Class Metrics",
                "",
                "| Class | Images | Instances | Precision | Recall | mAP50 | mAP50-95 |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for class_name, images, instances, precision, recall, map50, map5095 in class_rows:
            lines.append(
                f"| {class_name} | {images} | {instances} | {float(precision):.5f} | "
                f"{float(recall):.5f} | {float(map50):.5f} | {float(map5095):.5f} |"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    run_dir = resolve_project_path(args.run_dir)
    results_path = run_dir / "results.csv"
    if not results_path.exists():
        raise FileNotFoundError(f"Missing results.csv: {results_path}")

    log_path = resolve_project_path(args.log) if args.log else None
    output_path = resolve_project_path(args.output) if args.output else run_dir / "summary.md"

    rows = read_results(results_path)
    class_rows = parse_class_metrics(log_path)
    summary = render_summary(run_dir, rows, class_rows, args.title)
    output_path.write_text(summary, encoding="utf-8")
    print(f"Wrote summary to {output_path}")


if __name__ == "__main__":
    main()

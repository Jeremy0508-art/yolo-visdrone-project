from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils.paths import resolve_project_path


CLASS_NAMES = [
    "pedestrian",
    "people",
    "bicycle",
    "car",
    "van",
    "truck",
    "tricycle",
    "awning-tricycle",
    "bus",
    "motor",
]


@dataclass(frozen=True)
class PerClassTarget:
    model: str
    run_dir: str
    logs: tuple[str, ...]


TARGETS = [
    PerClassTarget(
        model="YOLOv8n baseline",
        run_dir="runs/detect/baseline_yolov8n_visdrone",
        logs=("runs/logs/train_baseline_yolov8n_20260612_194313.log",),
    ),
    PerClassTarget(
        model="YOLO11n baseline",
        run_dir="runs/detect/baseline_yolo11n_visdrone",
        logs=("runs/logs/baseline_yolo11n_visdrone_resume_20260516.log",),
    ),
    PerClassTarget(
        model="YOLO11n-P2",
        run_dir="runs/detect/yolo11n_p2_pretrained_visdrone",
        logs=("runs/logs/yolo11n_p2_pretrained_visdrone_resume.out.log",),
    ),
    PerClassTarget(
        model="YOLO11n-P2-CoordAttention",
        run_dir="runs/detect/yolo11n_p2_coordatt_visdrone",
        logs=("runs/logs/yolo11n_p2_coordatt_20260522_010820.stdout.log",),
    ),
    PerClassTarget(
        model="YOLO11n-P2-CoordAttention-960",
        run_dir="runs/detect/yolo11n_p2_coordatt_960_visdrone_full",
        logs=(
            "runs/logs/val_yolo11n_p2_coordatt_960_20260609_182415.stdout.log",
            "runs/logs/yolo11n_p2_coordatt_960_visdrone_full_resume_20260527.stdout.log",
            "runs/logs/yolo11n_p2_coordatt_960_visdrone_full_resume_20260526.stdout.log",
            "runs/logs/yolo11n_p2_coordatt_960_visdrone_full.stdout.log",
        ),
    ),
    PerClassTarget(
        model="YOLO11n-P2-CoordAttention-SmallObjAug",
        run_dir="runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone",
        logs=("runs/logs/yolo11n_p2_coordatt_smallobj_aug_resume_20260609_072221.stdout.log",),
    ),
]


ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
CLASS_PATTERN = re.compile(
    r"^\s*(?P<class>pedestrian|people|bicycle|car|van|truck|tricycle|awning-tricycle|bus|motor)\s+"
    r"(?P<images>\d+)\s+(?P<instances>\d+)\s+"
    r"(?P<precision>[\d.]+)\s+(?P<recall>[\d.]+)\s+"
    r"(?P<map50>[\d.]+)\s+(?P<map5095>[\d.]+)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect final per-class metrics from YOLO logs.")
    parser.add_argument("--output", default="paper/tables/per_class_results.csv", help="Output CSV path.")
    return parser.parse_args()


def read_text_with_fallback(path: Path) -> str:
    for encoding in ("utf-8", "utf-16"):
        try:
            return path.read_text(encoding=encoding, errors="strict")
        except UnicodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def clean_line(line: str) -> str:
    return ANSI_PATTERN.sub("", line).replace("\r", "")


def parse_log(log_path: Path) -> list[dict[str, str]]:
    text = read_text_with_fallback(log_path)
    rows = []
    for line in text.splitlines():
        clean = clean_line(line)
        match = CLASS_PATTERN.match(clean)
        if not match:
            continue
        rows.append(match.groupdict())
    return rows


def final_class_rows(target: PerClassTarget) -> tuple[list[dict[str, str]], str]:
    for log in target.logs:
        log_path = resolve_project_path(log)
        if not log_path.exists():
            continue
        rows = parse_log(log_path)
        if len(rows) < len(CLASS_NAMES):
            continue
        final_rows = rows[-len(CLASS_NAMES) :]
        if [row["class"] for row in final_rows] == CLASS_NAMES:
            return final_rows, log
    raise FileNotFoundError(f"Could not find complete per-class metrics for {target.model}")


def format_float(value: str) -> str:
    return f"{float(value):.5f}"


def build_rows() -> list[dict[str, str]]:
    output_rows = []
    for target in TARGETS:
        class_rows, log_source = final_class_rows(target)
        for row in class_rows:
            output_rows.append(
                {
                    "model": target.model,
                    "class": row["class"],
                    "images": row["images"],
                    "instances": row["instances"],
                    "precision": format_float(row["precision"]),
                    "recall": format_float(row["recall"]),
                    "map50": format_float(row["map50"]),
                    "map50_95": format_float(row["map5095"]),
                    "run_dir": target.run_dir,
                    "log_source": log_source,
                }
            )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    rows = build_rows()
    output = resolve_project_path(args.output)
    write_csv(output, rows)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

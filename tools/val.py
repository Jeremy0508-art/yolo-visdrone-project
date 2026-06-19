from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.register import register_custom_modules
from src.utils.paths import materialize_absolute_dataset_yaml, resolve_project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a trained YOLO model.")
    parser.add_argument("--weights", required=True, help="Path to model weights.")
    parser.add_argument("--data", default="configs/dataset/visdrone.yaml", help="Dataset yaml path.")
    parser.add_argument("--imgsz", type=int, default=640, help="Validation image size.")
    parser.add_argument("--batch", type=int, default=16, help="Validation batch size.")
    parser.add_argument("--device", default=None, help="Device, for example 0 or cpu.")
    parser.add_argument("--split", default="val", choices=["val", "test"], help="Dataset split to evaluate.")
    parser.add_argument("--project", default="runs/val", help="Output project directory.")
    parser.add_argument("--name", default="baseline_eval", help="Output run name.")
    return parser.parse_args()


def main() -> None:
    register_custom_modules()
    args = parse_args()
    model = YOLO(str(resolve_project_path(args.weights)))
    model.val(
        data=str(materialize_absolute_dataset_yaml(args.data)),
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        split=args.split,
        project=str(resolve_project_path(args.project)),
        name=args.name,
    )


if __name__ == "__main__":
    main()

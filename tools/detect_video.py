from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.register import register_custom_modules
from src.utils.paths import resolve_project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run YOLO inference on a video.")
    parser.add_argument("--weights", required=True, help="Path to model weights.")
    parser.add_argument("--source", required=True, help="Video path.")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size.")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold.")
    parser.add_argument("--device", default=None, help="Device, for example 0 or cpu.")
    parser.add_argument("--project", default="runs/detect_video", help="Output project directory.")
    parser.add_argument("--name", default="predict", help="Output run name.")
    return parser.parse_args()


def main() -> None:
    register_custom_modules()
    args = parse_args()
    model = YOLO(str(resolve_project_path(args.weights)))
    model.predict(
        source=str(resolve_project_path(args.source)),
        imgsz=args.imgsz,
        conf=args.conf,
        device=args.device,
        project=str(resolve_project_path(args.project)),
        name=args.name,
        save=True,
    )


if __name__ == "__main__":
    main()

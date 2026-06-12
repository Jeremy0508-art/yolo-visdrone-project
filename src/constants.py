from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VISDRONE_CLASS_NAMES = [
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

# VisDrone DET annotation category ids:
# 0 ignored region, 1 pedestrian, 2 people, ..., 10 motor, 11 others.
VISDRONE_TO_YOLO_CLASS = {visdrone_id: visdrone_id - 1 for visdrone_id in range(1, 11)}
VISDRONE_IGNORED_CLASSES = {0, 11}

VISDRONE_SPLITS = {
    "train": "VisDrone2019-DET-train",
    "val": "VisDrone2019-DET-val",
    "test": "VisDrone2019-DET-test-dev",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


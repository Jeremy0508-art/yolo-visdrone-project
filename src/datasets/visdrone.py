from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from src.constants import VISDRONE_IGNORED_CLASSES, VISDRONE_TO_YOLO_CLASS


@dataclass(frozen=True)
class VisDroneBox:
    x: float
    y: float
    width: float
    height: float
    score: int
    category_id: int
    truncation: int
    occlusion: int

    @property
    def is_trainable(self) -> bool:
        return self.category_id not in VISDRONE_IGNORED_CLASSES and self.category_id in VISDRONE_TO_YOLO_CLASS

    def to_yolo(self, image_width: int, image_height: int) -> str:
        class_id = VISDRONE_TO_YOLO_CLASS[self.category_id]
        x_center = (self.x + self.width / 2) / image_width
        y_center = (self.y + self.height / 2) / image_height
        width = self.width / image_width
        height = self.height / image_height
        return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


def read_image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def parse_annotation_line(line: str) -> VisDroneBox | None:
    parts = [part.strip() for part in line.split(",")]
    if len(parts) < 8:
        return None

    try:
        x, y, width, height = map(float, parts[:4])
        score = int(float(parts[4]))
        category_id = int(float(parts[5]))
        truncation = int(float(parts[6]))
        occlusion = int(float(parts[7]))
    except ValueError:
        return None

    if width <= 0 or height <= 0:
        return None

    return VisDroneBox(
        x=x,
        y=y,
        width=width,
        height=height,
        score=score,
        category_id=category_id,
        truncation=truncation,
        occlusion=occlusion,
    )


def load_yolo_labels(annotation_path: Path, image_width: int, image_height: int) -> list[str]:
    if not annotation_path.exists():
        return []

    labels = []
    for line in annotation_path.read_text(encoding="utf-8").splitlines():
        box = parse_annotation_line(line)
        if box is None or not box.is_trainable:
            continue
        labels.append(box.to_yolo(image_width, image_height))
    return labels


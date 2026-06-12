from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2


def draw_yolo_labels(image_path: Path, label_path: Path, class_names: list[str]) -> Any:
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Failed to read image: {image_path}")

    height, width = image.shape[:2]
    if not label_path.exists():
        return image

    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 5:
            continue

        class_id = int(parts[0])
        x_center, y_center, box_width, box_height = map(float, parts[1:])
        x1 = int((x_center - box_width / 2) * width)
        y1 = int((y_center - box_height / 2) * height)
        x2 = int((x_center + box_width / 2) * width)
        y2 = int((y_center + box_height / 2) * height)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 180, 255), 2)
        label = class_names[class_id] if class_id < len(class_names) else str(class_id)
        cv2.putText(image, label, (x1, max(0, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 180, 255), 1)

    return image

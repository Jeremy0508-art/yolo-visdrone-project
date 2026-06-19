from __future__ import annotations

import argparse
import logging
import random
import sys
from pathlib import Path

import cv2
import yaml

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS, VISDRONE_CLASS_NAMES
from src.utils.logging import configure_logging
from src.utils.paths import ensure_dir, resolve_project_path
from src.utils.visualization import draw_yolo_labels


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a YOLO-format detection dataset.")
    parser.add_argument("--dataset-root", default="data/processed/visdrone_yolo", help="YOLO dataset root.")
    parser.add_argument("--splits", nargs="+", default=["train", "val", "test"], help="Dataset splits to check.")
    parser.add_argument("--preview-count", type=int, default=0, help="Number of labeled images to preview per split.")
    parser.add_argument("--preview-dir", default="runs/dataset_checks", help="Directory for preview images.")
    parser.add_argument(
        "--data-yaml",
        default=None,
        help="Optional YOLO data YAML. When provided, class names are loaded from this file.",
    )
    return parser.parse_args()


def list_images(image_dir: Path) -> list[Path]:
    if not image_dir.exists():
        return []
    return sorted(path for path in image_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)


def load_class_names(data_yaml: str | None) -> list[str]:
    if not data_yaml:
        return VISDRONE_CLASS_NAMES
    yaml_path = resolve_project_path(data_yaml)
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    names = data.get("names", [])
    if isinstance(names, dict):
        return [str(names[index]) for index in sorted(names, key=lambda key: int(key))]
    if isinstance(names, list):
        return [str(name) for name in names]
    raise ValueError(f"Unsupported names format in {yaml_path}")


def validate_label_file(label_path: Path, class_count: int) -> tuple[int, int]:
    invalid = 0
    boxes = 0

    if not label_path.exists():
        return boxes, invalid

    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 5:
            invalid += 1
            continue

        try:
            class_id = int(parts[0])
            values = [float(value) for value in parts[1:]]
        except ValueError:
            invalid += 1
            continue

        if class_id < 0 or class_id >= class_count or any(value < 0 or value > 1 for value in values):
            invalid += 1
            continue

        boxes += 1

    return boxes, invalid


def check_split(
    dataset_root: Path,
    split: str,
    preview_count: int,
    preview_root: Path,
    class_names: list[str],
) -> dict[str, int]:
    image_dir = dataset_root / "images" / split
    label_dir = dataset_root / "labels" / split
    images = list_images(image_dir)

    stats = {
        "images": len(images),
        "missing_labels": 0,
        "empty_labels": 0,
        "boxes": 0,
        "invalid_lines": 0,
    }

    labeled_images = []
    for image_path in images:
        label_path = label_dir / f"{image_path.stem}.txt"
        if not label_path.exists():
            stats["missing_labels"] += 1
            continue

        boxes, invalid = validate_label_file(label_path, len(class_names))
        stats["boxes"] += boxes
        stats["invalid_lines"] += invalid

        if boxes == 0:
            stats["empty_labels"] += 1
        else:
            labeled_images.append(image_path)

    if preview_count > 0 and labeled_images:
        split_preview_dir = ensure_dir(preview_root / split)
        for image_path in random.sample(labeled_images, min(preview_count, len(labeled_images))):
            label_path = label_dir / f"{image_path.stem}.txt"
            preview = draw_yolo_labels(image_path, label_path, class_names)
            cv2.imwrite(str(split_preview_dir / image_path.name), preview)

    return stats


def main() -> None:
    configure_logging()
    args = parse_args()
    dataset_root = resolve_project_path(args.dataset_root)
    preview_root = resolve_project_path(args.preview_dir)

    if not dataset_root.exists():
        raise FileNotFoundError(f"Dataset root does not exist: {dataset_root}")

    class_names = load_class_names(args.data_yaml)
    for split in args.splits:
        stats = check_split(dataset_root, split, args.preview_count, preview_root, class_names)
        logging.info(
            "%s | images=%d boxes=%d missing_labels=%d empty_labels=%d invalid_lines=%d",
            split,
            stats["images"],
            stats["boxes"],
            stats["missing_labels"],
            stats["empty_labels"],
            stats["invalid_lines"],
        )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS
from src.utils.logging import configure_logging
from src.utils.paths import ensure_dir, resolve_project_path


UAVDT_CLASS_MAP = {
    1: 0,  # car
    2: 1,  # truck
    3: 2,  # bus
}

IMAGE_DIR_NAMES = ("img1", "images", "JPEGImages", "Imgs")
ANNOTATION_NAMES = ("gt_whole.txt", "gt.txt")


@dataclass(frozen=True)
class RawBox:
    frame_id: int
    x: float
    y: float
    width: float
    height: float
    class_id: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert UAVDT annotations to YOLO format.")
    parser.add_argument("--raw-root", default="data/raw/UAVDT", help="Root directory of the raw UAVDT dataset.")
    parser.add_argument(
        "--output-root",
        default="data/processed/uavdt_yolo",
        help="Output root directory for the converted YOLO-format UAVDT dataset.",
    )
    parser.add_argument(
        "--copy-images",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Copy images to the output directory. Disable to only write labels.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Fallback validation ratio when no train/test split can be inferred from folder names.",
    )
    parser.add_argument(
        "--include-unknown-classes",
        action="store_true",
        help="Keep UAVDT categories not present in the official car/truck/bus map by assigning them to car.",
    )
    return parser.parse_args()


def find_image_dir(sequence_dir: Path) -> Path | None:
    for name in IMAGE_DIR_NAMES:
        candidate = sequence_dir / name
        if candidate.exists() and any(candidate.glob("*")):
            return candidate
    if any(path.suffix.lower() in IMAGE_EXTENSIONS for path in sequence_dir.iterdir() if path.is_file()):
        return sequence_dir
    return None


def find_annotation_file(sequence_dir: Path) -> Path | None:
    candidates: list[Path] = []
    for name in ANNOTATION_NAMES:
        candidates.append(sequence_dir / name)
    candidates.extend(sequence_dir.glob("*_gt_whole.txt"))
    candidates.extend(sequence_dir.glob("*_gt.txt"))
    candidates.extend((sequence_dir / "gt").glob("*.txt") if (sequence_dir / "gt").exists() else [])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def infer_split(sequence_dir: Path, fallback_index: int, val_ratio: float) -> str:
    parts = {part.lower() for part in sequence_dir.parts}
    name = sequence_dir.name.lower()
    if "train" in parts or "training" in parts or name.startswith("train"):
        return "train"
    if "val" in parts or "valid" in parts or "validation" in parts or name.startswith("val"):
        return "val"
    if "test" in parts or "testing" in parts or name.startswith("test"):
        return "test"
    return "val" if (fallback_index % max(1, round(1.0 / val_ratio))) == 0 else "train"


def discover_sequences(raw_root: Path) -> list[Path]:
    sequences: list[Path] = []
    for path in sorted(raw_root.rglob("*")):
        if not path.is_dir():
            continue
        image_dir = find_image_dir(path)
        if image_dir is None:
            continue
        annotation_file = find_annotation_file(path)
        if annotation_file is not None:
            sequences.append(path)
    return sequences


def find_frame_image(image_dir: Path, frame_id: int) -> Path | None:
    stems = [
        f"{frame_id:06d}",
        f"{frame_id:05d}",
        f"{frame_id:04d}",
        str(frame_id),
        f"img{frame_id:06d}",
        f"img{frame_id:05d}",
    ]
    for stem in stems:
        for suffix in IMAGE_EXTENSIONS:
            candidate = image_dir / f"{stem}{suffix}"
            if candidate.exists():
                return candidate
    matches = sorted(image_dir.glob(f"*{frame_id:06d}*"))
    for candidate in matches:
        if candidate.suffix.lower() in IMAGE_EXTENSIONS:
            return candidate
    return None


def read_image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def parse_uavdt_line(line: str, include_unknown_classes: bool) -> RawBox | None:
    parts = [part.strip() for part in line.replace(",", " ").split() if part.strip()]
    if len(parts) < 8:
        return None
    try:
        frame_id = int(float(parts[0]))
        x = float(parts[2])
        y = float(parts[3])
        width = float(parts[4])
        height = float(parts[5])
        raw_class = int(float(parts[7]))
    except ValueError:
        return None

    if width <= 0 or height <= 0:
        return None
    if raw_class not in UAVDT_CLASS_MAP:
        if not include_unknown_classes:
            return None
        class_id = 0
    else:
        class_id = UAVDT_CLASS_MAP[raw_class]
    return RawBox(frame_id=frame_id, x=x, y=y, width=width, height=height, class_id=class_id)


def load_annotations(annotation_file: Path, include_unknown_classes: bool) -> dict[int, list[RawBox]]:
    by_frame: dict[int, list[RawBox]] = defaultdict(list)
    for line in annotation_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        box = parse_uavdt_line(line, include_unknown_classes)
        if box is not None:
            by_frame[box.frame_id].append(box)
    return by_frame


def to_yolo_line(box: RawBox, image_width: int, image_height: int) -> str:
    x_center = (box.x + box.width / 2.0) / image_width
    y_center = (box.y + box.height / 2.0) / image_height
    width = box.width / image_width
    height = box.height / image_height
    values = [
        min(1.0, max(0.0, x_center)),
        min(1.0, max(0.0, y_center)),
        min(1.0, max(0.0, width)),
        min(1.0, max(0.0, height)),
    ]
    return f"{box.class_id} " + " ".join(f"{value:.6f}" for value in values)


def convert_sequence(
    sequence_dir: Path,
    split: str,
    output_root: Path,
    copy_images: bool,
    overwrite: bool,
    include_unknown_classes: bool,
) -> dict[str, int]:
    image_dir = find_image_dir(sequence_dir)
    annotation_file = find_annotation_file(sequence_dir)
    if image_dir is None or annotation_file is None:
        return {"images": 0, "labels": 0, "boxes": 0, "missing_images": 0}

    annotations = load_annotations(annotation_file, include_unknown_classes)
    output_image_dir = ensure_dir(output_root / "images" / split)
    output_label_dir = ensure_dir(output_root / "labels" / split)

    stats = {"images": 0, "labels": 0, "boxes": 0, "missing_images": 0}
    for frame_id, boxes in sorted(annotations.items()):
        image_path = find_frame_image(image_dir, frame_id)
        if image_path is None:
            stats["missing_images"] += 1
            continue
        output_stem = f"{sequence_dir.name}_{image_path.stem}"
        output_image_path = output_image_dir / f"{output_stem}{image_path.suffix.lower()}"
        output_label_path = output_label_dir / f"{output_stem}.txt"

        if copy_images and (overwrite or not output_image_path.exists()):
            shutil.copy2(image_path, output_image_path)

        image_width, image_height = read_image_size(image_path)
        lines = [to_yolo_line(box, image_width, image_height) for box in boxes]
        if overwrite or not output_label_path.exists():
            output_label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

        stats["images"] += 1
        stats["labels"] += 1
        stats["boxes"] += len(lines)
    return stats


def main() -> None:
    configure_logging()
    args = parse_args()
    raw_root = resolve_project_path(args.raw_root)
    output_root = resolve_project_path(args.output_root)
    if not raw_root.exists():
        raise FileNotFoundError(f"Raw UAVDT root does not exist: {raw_root}")

    sequences = discover_sequences(raw_root)
    if not sequences:
        raise FileNotFoundError(
            f"No UAVDT sequences with images and annotations were found under {raw_root}. "
            "Check the raw layout and annotation filenames."
        )

    all_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"images": 0, "labels": 0, "boxes": 0, "missing_images": 0})
    logging.info("Discovered %d UAVDT sequences", len(sequences))
    for index, sequence_dir in enumerate(tqdm(sequences, desc="Converting UAVDT sequences")):
        split = infer_split(sequence_dir, index, args.val_ratio)
        stats = convert_sequence(
            sequence_dir=sequence_dir,
            split=split,
            output_root=output_root,
            copy_images=args.copy_images,
            overwrite=args.overwrite,
            include_unknown_classes=args.include_unknown_classes,
        )
        for key, value in stats.items():
            all_stats[split][key] += value

    for split in ("train", "val", "test"):
        stats = all_stats[split]
        logging.info(
            "%s | images=%d labels=%d boxes=%d missing_images=%d",
            split,
            stats["images"],
            stats["labels"],
            stats["boxes"],
            stats["missing_images"],
        )


if __name__ == "__main__":
    main()

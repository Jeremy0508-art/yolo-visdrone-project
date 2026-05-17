import argparse
import logging
import shutil
import sys
from pathlib import Path

from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS, VISDRONE_SPLITS
from src.datasets.visdrone import load_yolo_labels, read_image_size
from src.utils.logging import configure_logging
from src.utils.paths import ensure_dir, resolve_project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert VisDrone DET annotations to YOLO format.")
    parser.add_argument("--raw-root", default="data/raw/VisDrone", help="Root directory of raw VisDrone DET dataset.")
    parser.add_argument(
        "--output-root",
        default="data/processed/visdrone_yolo",
        help="Output root directory for YOLO-format dataset.",
    )
    parser.add_argument(
        "--copy-images",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Copy images to output directory. Disable to only write labels.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing label files and copied images.",
    )
    return parser.parse_args()


def find_images(image_dir: Path) -> list[Path]:
    images = [path for path in image_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS]
    return sorted(images)


def convert_split(split: str, source_root: Path, output_root: Path, copy_images: bool, overwrite: bool) -> dict[str, int]:
    image_dir = source_root / "images"
    annotation_dir = source_root / "annotations"
    output_image_dir = ensure_dir(output_root / "images" / split)
    output_label_dir = ensure_dir(output_root / "labels" / split)

    if not image_dir.exists():
        raise FileNotFoundError(f"Missing image directory: {image_dir}")
    if not annotation_dir.exists():
        logging.warning("Missing annotation directory, empty labels will be created: %s", annotation_dir)

    stats = {
        "images": 0,
        "labels": 0,
        "boxes": 0,
        "missing_annotations": 0,
        "failed_images": 0,
    }

    for image_path in tqdm(find_images(image_dir), desc=f"Converting {split}"):
        label_path = output_label_dir / f"{image_path.stem}.txt"
        output_image_path = output_image_dir / image_path.name
        annotation_path = annotation_dir / f"{image_path.stem}.txt"

        if copy_images and (overwrite or not output_image_path.exists()):
            shutil.copy2(image_path, output_image_path)

        try:
            image_width, image_height = read_image_size(image_path)
        except OSError:
            logging.warning("Failed to read image size: %s", image_path)
            stats["failed_images"] += 1
            continue

        if annotation_dir.exists() and annotation_path.exists():
            labels = load_yolo_labels(annotation_path, image_width, image_height)
        else:
            labels = []
            stats["missing_annotations"] += 1

        if overwrite or not label_path.exists():
            label_path.write_text("\n".join(labels) + ("\n" if labels else ""), encoding="utf-8")

        stats["images"] += 1
        stats["labels"] += 1
        stats["boxes"] += len(labels)

    return stats


def main() -> None:
    configure_logging()
    args = parse_args()

    raw_root = resolve_project_path(args.raw_root)
    output_root = resolve_project_path(args.output_root)

    if not raw_root.exists():
        raise FileNotFoundError(f"Raw dataset root does not exist: {raw_root}")

    logging.info("Raw VisDrone root: %s", raw_root)
    logging.info("YOLO output root: %s", output_root)

    all_stats = {}
    for split, split_dir_name in VISDRONE_SPLITS.items():
        source_root = raw_root / split_dir_name
        if not source_root.exists():
            logging.warning("Skip missing split %s: %s", split, source_root)
            continue
        all_stats[split] = convert_split(split, source_root, output_root, args.copy_images, args.overwrite)

    logging.info("Conversion summary:")
    for split, stats in all_stats.items():
        logging.info(
            "%s | images=%d labels=%d boxes=%d missing_annotations=%d failed_images=%d",
            split,
            stats["images"],
            stats["labels"],
            stats["boxes"],
            stats["missing_annotations"],
            stats["failed_images"],
        )


if __name__ == "__main__":
    main()

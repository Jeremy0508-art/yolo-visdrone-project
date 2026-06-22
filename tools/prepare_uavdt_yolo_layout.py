from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
SPLIT_ALIASES = {
    "train": "train",
    "training": "train",
    "val": "val",
    "valid": "val",
    "validation": "val",
    "test": "test",
}


@dataclass
class SplitStats:
    images: int = 0
    labels: int = 0
    boxes: int = 0
    missing_labels: int = 0
    labels_without_images: int = 0
    empty_labels: int = 0
    invalid_lines: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a YOLO-layout UAVDT mirror for this project. The source is expected "
            "to contain split/images and split/labels folders, e.g. UAVDT/train/images."
        )
    )
    parser.add_argument("--source-root", default="data/raw/UAVDT", help="Extracted UAVDT root or its parent.")
    parser.add_argument("--output-root", default="data/processed/uavdt_yolo", help="Project YOLO dataset root.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output root.")
    parser.add_argument(
        "--summary",
        default=None,
        help="Optional summary JSON path. Defaults to <output-root>/uavdt_prepare_summary.json.",
    )
    return parser.parse_args()


def resolve_root(path: str) -> Path:
    return Path(path).resolve()


def find_split_roots(source_root: Path) -> dict[str, Path]:
    candidates = [source_root]
    candidates.extend(path for path in source_root.iterdir() if path.is_dir())

    split_roots: dict[str, Path] = {}
    for candidate in candidates:
        for child in candidate.iterdir():
            if not child.is_dir():
                continue
            split = SPLIT_ALIASES.get(child.name.lower())
            if split and (child / "images").is_dir() and (child / "labels").is_dir():
                split_roots[split] = child
    return split_roots


def list_images(path: Path) -> list[Path]:
    return sorted(file for file in path.iterdir() if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS)


def list_labels(path: Path) -> list[Path]:
    return sorted(file for file in path.iterdir() if file.is_file() and file.suffix.lower() == ".txt")


def copy_split(source_split_root: Path, output_root: Path, split: str) -> None:
    image_out = output_root / "images" / split
    label_out = output_root / "labels" / split
    image_out.mkdir(parents=True, exist_ok=True)
    label_out.mkdir(parents=True, exist_ok=True)

    for image_path in list_images(source_split_root / "images"):
        shutil.copy2(image_path, image_out / image_path.name)
    for label_path in list_labels(source_split_root / "labels"):
        shutil.copy2(label_path, label_out / label_path.name)


def validate_label_file(label_path: Path) -> tuple[int, int]:
    boxes = 0
    invalid = 0
    for line in label_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if len(parts) != 5:
            invalid += 1
            continue
        try:
            class_id = int(parts[0])
            values = [float(value) for value in parts[1:]]
        except ValueError:
            invalid += 1
            continue
        if class_id not in {0, 1, 2} or any(value < 0.0 or value > 1.0 for value in values):
            invalid += 1
            continue
        boxes += 1
    return boxes, invalid


def audit_output(output_root: Path, splits: list[str]) -> dict[str, SplitStats]:
    report: dict[str, SplitStats] = {}
    for split in splits:
        image_dir = output_root / "images" / split
        label_dir = output_root / "labels" / split
        images = list_images(image_dir)
        labels = list_labels(label_dir)
        image_stems = {path.stem for path in images}
        label_stems = {path.stem for path in labels}

        stats = SplitStats(images=len(images), labels=len(labels))
        stats.missing_labels = len(image_stems - label_stems)
        stats.labels_without_images = len(label_stems - image_stems)

        for label_path in labels:
            boxes, invalid = validate_label_file(label_path)
            stats.boxes += boxes
            stats.invalid_lines += invalid
            if boxes == 0 and invalid == 0:
                stats.empty_labels += 1
        report[split] = stats
    return report


def main() -> None:
    args = parse_args()
    source_root = resolve_root(args.source_root)
    output_root = resolve_root(args.output_root)
    summary_path = resolve_root(args.summary) if args.summary else output_root / "uavdt_prepare_summary.json"

    if not source_root.exists():
        raise FileNotFoundError(f"Source root does not exist: {source_root}")

    split_roots = find_split_roots(source_root)
    required = {"train", "val"}
    missing_required = sorted(required - set(split_roots))
    if missing_required:
        raise FileNotFoundError(
            f"Missing required UAVDT YOLO split folders: {missing_required}; source_root={source_root}"
        )

    if output_root.exists():
        if not args.overwrite:
            raise FileExistsError(f"Output root already exists: {output_root}. Use --overwrite to replace it.")
        shutil.rmtree(output_root)

    for split, split_root in sorted(split_roots.items()):
        copy_split(split_root, output_root, split)

    report = audit_output(output_root, sorted(split_roots))
    summary = {
        "source_root": str(source_root),
        "output_root": str(output_root),
        "splits": {split: str(path) for split, path in sorted(split_roots.items())},
        "stats": {split: asdict(stats) for split, stats in report.items()},
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for split, stats in report.items():
        print(
            f"{split}: images={stats.images} labels={stats.labels} boxes={stats.boxes} "
            f"missing_labels={stats.missing_labels} labels_without_images={stats.labels_without_images} "
            f"empty_labels={stats.empty_labels} invalid_lines={stats.invalid_lines}"
        )
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()

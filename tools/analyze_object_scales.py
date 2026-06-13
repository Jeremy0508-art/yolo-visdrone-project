from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS, VISDRONE_CLASS_NAMES
from src.utils.paths import resolve_project_path


SCALE_BINS = (
    ("small", 0.0, 32.0 * 32.0),
    ("medium", 32.0 * 32.0, 96.0 * 96.0),
    ("large", 96.0 * 96.0, math.inf),
)


@dataclass(frozen=True)
class LabelBox:
    class_id: int
    width_px: float
    height_px: float

    @property
    def area_px2(self) -> float:
        return self.width_px * self.height_px

    @property
    def scale_bin(self) -> str:
        area = self.area_px2
        for name, lower, upper in SCALE_BINS:
            if lower <= area < upper:
                return name
        raise ValueError(f"Unhandled area: {area}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze VisDrone object scale distribution from YOLO-format labels."
    )
    parser.add_argument("--dataset-root", default="data/processed/visdrone_yolo", help="YOLO-format dataset root.")
    parser.add_argument("--splits", nargs="+", default=["train", "val"], help="Dataset splits to analyze.")
    parser.add_argument("--output-dir", default="paper/tables", help="Directory for generated CSV tables.")
    parser.add_argument(
        "--plot-dir",
        default="paper/figures/scale_analysis",
        help="Directory for generated scale-distribution figures.",
    )
    return parser.parse_args()


def image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def find_image(images_dir: Path, stem: str) -> Path | None:
    for suffix in IMAGE_EXTENSIONS:
        candidate = images_dir / f"{stem}{suffix}"
        if candidate.exists():
            return candidate
    return None


def load_boxes(label_path: Path, image_width: int, image_height: int) -> list[LabelBox]:
    boxes: list[LabelBox] = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        try:
            class_id = int(float(parts[0]))
            width_norm = float(parts[3])
            height_norm = float(parts[4])
        except ValueError:
            continue
        if class_id < 0 or class_id >= len(VISDRONE_CLASS_NAMES):
            continue
        if width_norm <= 0 or height_norm <= 0:
            continue
        boxes.append(LabelBox(class_id, width_norm * image_width, height_norm * image_height))
    return boxes


def analyze_split(dataset_root: Path, split: str) -> tuple[Counter[str], dict[int, Counter[str]], int, int]:
    images_dir = dataset_root / "images" / split
    labels_dir = dataset_root / "labels" / split
    if not labels_dir.exists():
        raise FileNotFoundError(f"Missing labels directory: {labels_dir}")
    if not images_dir.exists():
        raise FileNotFoundError(f"Missing images directory: {images_dir}")

    scale_counts: Counter[str] = Counter()
    class_scale_counts: dict[int, Counter[str]] = defaultdict(Counter)
    image_count = 0
    missing_images = 0

    for label_path in sorted(labels_dir.glob("*.txt")):
        image_path = find_image(images_dir, label_path.stem)
        if image_path is None:
            missing_images += 1
            continue
        image_count += 1
        width, height = image_size(image_path)
        for box in load_boxes(label_path, width, height):
            scale_counts[box.scale_bin] += 1
            class_scale_counts[box.class_id][box.scale_bin] += 1

    return scale_counts, class_scale_counts, image_count, missing_images


def write_object_scale_distribution(
    output_path: Path,
    split_counts: dict[str, Counter[str]],
    image_counts: dict[str, int],
    missing_images: dict[str, int],
) -> None:
    fieldnames = ["split", "images", "missing_images", "scale", "instances", "ratio"]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for split, counts in split_counts.items():
            total = sum(counts.values())
            for scale, _, _ in SCALE_BINS:
                instances = counts[scale]
                ratio = instances / total if total else 0.0
                writer.writerow(
                    {
                        "split": split,
                        "images": image_counts[split],
                        "missing_images": missing_images[split],
                        "scale": scale,
                        "instances": instances,
                        "ratio": f"{ratio:.6f}",
                    }
                )


def write_class_scale_distribution(
    output_path: Path,
    class_counts_by_split: dict[str, dict[int, Counter[str]]],
) -> None:
    fieldnames = ["split", "class_id", "class_name", "total", "small", "medium", "large", "small_ratio"]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for split, class_counts in class_counts_by_split.items():
            for class_id, class_name in enumerate(VISDRONE_CLASS_NAMES):
                counts = class_counts.get(class_id, Counter())
                total = sum(counts.values())
                small = counts["small"]
                writer.writerow(
                    {
                        "split": split,
                        "class_id": class_id,
                        "class_name": class_name,
                        "total": total,
                        "small": small,
                        "medium": counts["medium"],
                        "large": counts["large"],
                        "small_ratio": f"{(small / total if total else 0.0):.6f}",
                    }
                )


def write_scale_plot(output_path: Path, split_counts: dict[str, Counter[str]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"Skip plotting because matplotlib is unavailable: {exc}")
        return

    splits = list(split_counts)
    scale_names = [name for name, _, _ in SCALE_BINS]
    colors = {"small": "#4C78A8", "medium": "#F58518", "large": "#54A24B"}
    bottoms = [0.0 for _ in splits]

    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    for scale in scale_names:
        ratios = []
        for split in splits:
            counts = split_counts[split]
            total = sum(counts.values())
            ratios.append(counts[scale] / total if total else 0.0)
        ax.bar(splits, ratios, bottom=bottoms, label=scale, color=colors[scale], width=0.55)
        bottoms = [bottom + ratio for bottom, ratio in zip(bottoms, ratios)]

    ax.set_ylabel("Instance ratio")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.15))
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    dataset_root = resolve_project_path(args.dataset_root)
    output_dir = resolve_project_path(args.output_dir)
    plot_dir = resolve_project_path(args.plot_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    split_counts: dict[str, Counter[str]] = {}
    class_counts_by_split: dict[str, dict[int, Counter[str]]] = {}
    image_counts: dict[str, int] = {}
    missing_images: dict[str, int] = {}

    for split in args.splits:
        counts, class_counts, image_count, missing_count = analyze_split(dataset_root, split)
        split_counts[split] = counts
        class_counts_by_split[split] = class_counts
        image_counts[split] = image_count
        missing_images[split] = missing_count

    write_object_scale_distribution(output_dir / "object_scale_distribution.csv", split_counts, image_counts, missing_images)
    write_class_scale_distribution(output_dir / "class_scale_distribution.csv", class_counts_by_split)
    write_scale_plot(plot_dir / "object_scale_distribution.png", split_counts)

    print(f"Wrote {output_dir / 'object_scale_distribution.csv'}")
    print(f"Wrote {output_dir / 'class_scale_distribution.csv'}")
    print(f"Wrote {plot_dir / 'object_scale_distribution.png'}")


if __name__ == "__main__":
    main()

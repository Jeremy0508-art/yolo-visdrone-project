from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import torch
from PIL import Image
from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS
from src.models.register import register_custom_modules
from src.utils.paths import resolve_project_path


SCALE_BINS = (
    ("small", 0.0, 32.0 * 32.0),
    ("medium", 32.0 * 32.0, 96.0 * 96.0),
    ("large", 96.0 * 96.0, float("inf")),
)


@dataclass(frozen=True)
class EvalTarget:
    model: str
    weights: str
    imgsz: int


@dataclass
class Box:
    cls: int
    xyxy: tuple[float, float, float, float]
    conf: float = 1.0

    @property
    def area(self) -> float:
        x1, y1, x2, y2 = self.xyxy
        return max(0.0, x2 - x1) * max(0.0, y2 - y1)

    @property
    def scale(self) -> str:
        area = self.area
        for name, lower, upper in SCALE_BINS:
            if lower <= area < upper:
                return name
        raise ValueError(f"Unhandled area: {area}")


DEFAULT_TARGETS = [
    EvalTarget(
        model="YOLO11n baseline",
        weights="runs/detect/baseline_yolo11n_visdrone/weights/best.pt",
        imgsz=640,
    ),
    EvalTarget(
        model="YOLO11n-P2-CoordAttention-960",
        weights="runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt",
        imgsz=960,
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate validation detections by GT object scale groups.")
    parser.add_argument("--dataset-root", default="data/processed/visdrone_yolo", help="YOLO-format dataset root.")
    parser.add_argument("--dataset-name", default=None, help="Dataset name written to the output CSV.")
    parser.add_argument("--split", default="val", help="Dataset split to evaluate.")
    parser.add_argument(
        "--targets-csv",
        default=None,
        help="Optional CSV with model,weights,imgsz columns. Rows with enabled=false are skipped.",
    )
    parser.add_argument("--output", default="paper/tables/scale_group_results.csv", help="Output CSV path.")
    parser.add_argument(
        "--plot-output",
        default="paper/figures/scale_analysis/scale_group_recall.png",
        help="Output recall comparison figure path.",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Prediction confidence threshold.")
    parser.add_argument("--iou", type=float, default=0.5, help="IoU threshold for a true positive match.")
    parser.add_argument("--device", default=None, help="Device passed to Ultralytics, for example 0 or cpu.")
    parser.add_argument("--max-det", type=int, default=300, help="Maximum detections per image.")
    parser.add_argument("--limit-images", type=int, default=None, help="Optional image limit for smoke checks.")
    return parser.parse_args()


def load_targets(targets_csv: str | None) -> list[EvalTarget]:
    if targets_csv is None:
        return list(DEFAULT_TARGETS)

    csv_path = resolve_project_path(targets_csv)
    targets: list[EvalTarget] = []
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            enabled = row.get("enabled", "true").strip().lower()
            if enabled in {"0", "false", "no", "n"}:
                continue
            targets.append(
                EvalTarget(
                    model=row["model"],
                    weights=row["weights"],
                    imgsz=int(row["imgsz"]),
                )
            )
    if not targets:
        raise ValueError(f"No enabled targets found in {csv_path}")
    return targets


def image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def find_image(images_dir: Path, stem: str) -> Path | None:
    for suffix in IMAGE_EXTENSIONS:
        path = images_dir / f"{stem}{suffix}"
        if path.exists():
            return path
    return None


def load_gt(label_path: Path, image_width: int, image_height: int) -> list[Box]:
    boxes: list[Box] = []
    if not label_path.exists():
        return boxes
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        try:
            cls = int(float(parts[0]))
            x_center = float(parts[1]) * image_width
            y_center = float(parts[2]) * image_height
            width = float(parts[3]) * image_width
            height = float(parts[4]) * image_height
        except ValueError:
            continue
        x1 = x_center - width / 2.0
        y1 = y_center - height / 2.0
        x2 = x_center + width / 2.0
        y2 = y_center + height / 2.0
        boxes.append(Box(cls=cls, xyxy=(x1, y1, x2, y2)))
    return boxes


def box_iou(first: Box, second: Box) -> float:
    ax1, ay1, ax2, ay2 = first.xyxy
    bx1, by1, bx2, by2 = second.xyxy
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    intersection = inter_w * inter_h
    union = first.area + second.area - intersection
    return intersection / union if union > 0 else 0.0


def predictions_from_result(result) -> list[Box]:
    if result.boxes is None or len(result.boxes) == 0:
        return []
    xyxy = result.boxes.xyxy.detach().cpu().tolist()
    cls = result.boxes.cls.detach().cpu().tolist()
    conf = result.boxes.conf.detach().cpu().tolist()
    predictions = [
        Box(cls=int(class_id), xyxy=tuple(coords), conf=float(score))
        for coords, class_id, score in zip(xyxy, cls, conf)
    ]
    return sorted(predictions, key=lambda box: box.conf, reverse=True)


def evaluate_target(args: argparse.Namespace, target: EvalTarget) -> list[dict[str, str]]:
    dataset_root = resolve_project_path(args.dataset_root)
    images_dir = dataset_root / "images" / args.split
    labels_dir = dataset_root / "labels" / args.split
    weights_path = resolve_project_path(target.weights)
    if not weights_path.exists():
        raise FileNotFoundError(f"Missing weights: {weights_path}")

    model = YOLO(str(weights_path))
    gt_counts: Counter[str] = Counter()
    matched_gt_counts: Counter[str] = Counter()
    pred_counts: Counter[str] = Counter()
    tp_pred_counts: Counter[str] = Counter()
    class_gt_counts: dict[str, Counter[int]] = defaultdict(Counter)
    class_matched_counts: dict[str, Counter[int]] = defaultdict(Counter)

    label_paths = sorted(labels_dir.glob("*.txt"))
    if args.limit_images is not None:
        label_paths = label_paths[: args.limit_images]
    for label_path in label_paths:
        image_path = find_image(images_dir, label_path.stem)
        if image_path is None:
            continue
        width, height = image_size(image_path)
        gt_boxes = load_gt(label_path, width, height)
        for box in gt_boxes:
            gt_counts[box.scale] += 1
            class_gt_counts[box.scale][box.cls] += 1

        result = model.predict(
            source=str(image_path),
            imgsz=target.imgsz,
            conf=args.conf,
            iou=args.iou,
            max_det=args.max_det,
            device=args.device,
            verbose=False,
        )[0]
        pred_boxes = predictions_from_result(result)
        matched_gt: set[int] = set()

        for prediction in pred_boxes:
            pred_counts[prediction.scale] += 1
            best_iou = 0.0
            best_index = None
            for index, gt_box in enumerate(gt_boxes):
                if index in matched_gt or prediction.cls != gt_box.cls:
                    continue
                iou = box_iou(prediction, gt_box)
                if iou > best_iou:
                    best_iou = iou
                    best_index = index
            if best_index is not None and best_iou >= args.iou:
                matched_gt.add(best_index)
                gt_scale = gt_boxes[best_index].scale
                matched_gt_counts[gt_scale] += 1
                tp_pred_counts[prediction.scale] += 1
                class_matched_counts[gt_scale][gt_boxes[best_index].cls] += 1

    rows = []
    for scale, _, _ in SCALE_BINS:
        gt_total = gt_counts[scale]
        matched = matched_gt_counts[scale]
        predictions = pred_counts[scale]
        true_positive_predictions = tp_pred_counts[scale]
        rows.append(
            {
                "model": target.model,
                "dataset": args.dataset_name or dataset_root.name,
                "weights": target.weights,
                "split": args.split,
                "imgsz": target.imgsz,
                "conf": args.conf,
                "iou": args.iou,
                "scale": scale,
                "gt_instances": gt_total,
                "matched_gt": matched,
                "recall": f"{(matched / gt_total if gt_total else 0.0):.6f}",
                "predictions": predictions,
                "true_positive_predictions": true_positive_predictions,
                "precision": f"{(true_positive_predictions / predictions if predictions else 0.0):.6f}",
            }
        )
    return rows


def write_recall_plot(output_path: Path, rows: list[dict[str, str]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"Skip plotting because matplotlib is unavailable: {exc}")
        return

    models = []
    for row in rows:
        if row["model"] not in models:
            models.append(row["model"])
    scales = [name for name, _, _ in SCALE_BINS]
    values = {
        model: [float(next(row["recall"] for row in rows if row["model"] == model and row["scale"] == scale)) for scale in scales]
        for model in models
    }

    x_positions = list(range(len(scales)))
    width = 0.34 if len(models) <= 2 else 0.22
    offsets = [width * (index - (len(models) - 1) / 2.0) for index in range(len(models))]

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200)
    for offset, model in zip(offsets, models):
        ax.bar([x + offset for x in x_positions], values[model], width=width, label=model)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(scales)
    ax.set_ylabel("Recall @ IoU=0.5")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.35)
    ax.legend(frameon=False, fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def main() -> None:
    register_custom_modules()
    args = parse_args()
    output_path = resolve_project_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    targets = load_targets(args.targets_csv)
    for target in targets:
        rows.extend(evaluate_target(args, target))
        if args.device not in (None, "cpu") and torch.cuda.is_available():
            torch.cuda.empty_cache()

    fieldnames = [
        "model",
        "dataset",
        "weights",
        "split",
        "imgsz",
        "conf",
        "iou",
        "scale",
        "gt_instances",
        "matched_gt",
        "recall",
        "predictions",
        "true_positive_predictions",
        "precision",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    write_recall_plot(resolve_project_path(args.plot_output), rows)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

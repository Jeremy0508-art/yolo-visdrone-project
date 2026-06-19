from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils.metrics import ap_per_class, box_iou as ultralytics_box_iou

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


@dataclass(frozen=True)
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
        for name, lower, upper in SCALE_BINS:
            if lower <= self.area < upper:
                return name
        raise ValueError(f"Unhandled area: {self.area}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute local scale-bin AP from YOLO-format labels and model predictions. "
            "This is not an official COCO/VisDrone AP_small evaluator."
        )
    )
    parser.add_argument("--dataset-root", default="data/processed/visdrone_yolo", help="YOLO-format dataset root.")
    parser.add_argument("--dataset-name", default=None, help="Dataset name written to the output CSV.")
    parser.add_argument("--split", default="val", help="Dataset split to evaluate.")
    parser.add_argument(
        "--targets-csv",
        default="paper/tables/ieee_scale_eval_targets.csv",
        help="CSV with model,weights,imgsz columns. Rows with enabled=false are skipped.",
    )
    parser.add_argument("--output", default="paper/tables/ieee_scale_ap_results_visdrone.csv", help="Output CSV path.")
    parser.add_argument(
        "--plot-output",
        default="paper/figures/scale_analysis/ieee_scale_ap50_visdrone.png",
        help="Output AP50 comparison figure path.",
    )
    parser.add_argument("--conf", type=float, default=0.001, help="Prediction confidence threshold for AP curves.")
    parser.add_argument("--nms-iou", type=float, default=0.7, help="NMS IoU threshold passed to model.predict.")
    parser.add_argument("--device", default=None, help="Device passed to Ultralytics, for example 0 or cpu.")
    parser.add_argument("--max-det", type=int, default=300, help="Maximum detections per image.")
    parser.add_argument("--limit-images", type=int, default=None, help="Optional image limit for smoke checks.")
    parser.add_argument(
        "--prediction-scale-policy",
        choices=("same-bin", "all"),
        default="same-bin",
        help=(
            "same-bin filters predictions by predicted box scale before AP computation; "
            "all evaluates all predictions against GT boxes of each scale."
        ),
    )
    return parser.parse_args()


def load_targets(targets_csv: str) -> list[EvalTarget]:
    csv_path = resolve_project_path(targets_csv)
    targets: list[EvalTarget] = []
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            enabled = row.get("enabled", "true").strip().lower()
            if enabled in {"0", "false", "no", "n"}:
                continue
            targets.append(EvalTarget(model=row["model"], weights=row["weights"], imgsz=int(row["imgsz"])))
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


def predictions_from_result(result) -> list[Box]:
    if result.boxes is None or len(result.boxes) == 0:
        return []
    xyxy = result.boxes.xyxy.detach().cpu().tolist()
    cls = result.boxes.cls.detach().cpu().tolist()
    conf = result.boxes.conf.detach().cpu().tolist()
    return [
        Box(cls=int(class_id), xyxy=tuple(coords), conf=float(score))
        for coords, class_id, score in zip(xyxy, cls, conf)
    ]


def to_tensor(boxes: list[Box]) -> torch.Tensor:
    if not boxes:
        return torch.zeros((0, 4), dtype=torch.float32)
    return torch.tensor([box.xyxy for box in boxes], dtype=torch.float32)


def match_predictions(predictions: list[Box], targets: list[Box], iouv: np.ndarray) -> np.ndarray:
    correct = np.zeros((len(predictions), len(iouv)), dtype=bool)
    if not predictions or not targets:
        return correct

    pred_boxes = to_tensor(predictions)
    target_boxes = to_tensor(targets)
    ious = ultralytics_box_iou(target_boxes, pred_boxes).cpu().numpy()
    correct_class = np.array([[target.cls == pred.cls for pred in predictions] for target in targets], dtype=bool)

    for threshold_index, threshold in enumerate(iouv):
        target_indices, pred_indices = np.where((ious >= threshold) & correct_class)
        if len(target_indices) == 0:
            continue
        matches = np.stack((target_indices, pred_indices, ious[target_indices, pred_indices]), axis=1)
        if len(matches) > 1:
            matches = matches[matches[:, 2].argsort()[::-1]]
            _, unique_pred_indices = np.unique(matches[:, 1], return_index=True)
            matches = matches[unique_pred_indices]
            matches = matches[matches[:, 2].argsort()[::-1]]
            _, unique_target_indices = np.unique(matches[:, 0], return_index=True)
            matches = matches[unique_target_indices]
        correct[matches[:, 1].astype(int), threshold_index] = True
    return correct


def summarize_ap(tp: list[np.ndarray], conf: list[float], pred_cls: list[int], target_cls: list[int]) -> dict[str, float]:
    if tp:
        tp_array = np.concatenate(tp, axis=0)
    else:
        tp_array = np.zeros((0, 10), dtype=bool)
    conf_array = np.array(conf, dtype=np.float32)
    pred_cls_array = np.array(pred_cls, dtype=np.int64)
    target_cls_array = np.array(target_cls, dtype=np.int64)

    if len(target_cls_array) == 0:
        return {"precision": 0.0, "recall": 0.0, "ap50": 0.0, "map50_95": 0.0, "classes": 0}

    _, _, precision, recall, _, ap, unique_classes, *_ = ap_per_class(
        tp_array,
        conf_array,
        pred_cls_array,
        target_cls_array,
        plot=False,
    )
    return {
        "precision": float(np.mean(precision)) if len(precision) else 0.0,
        "recall": float(np.mean(recall)) if len(recall) else 0.0,
        "ap50": float(np.mean(ap[:, 0])) if ap.size else 0.0,
        "map50_95": float(np.mean(ap)) if ap.size else 0.0,
        "classes": int(len(unique_classes)),
    }


def evaluate_target(args: argparse.Namespace, target: EvalTarget) -> list[dict[str, str]]:
    dataset_root = resolve_project_path(args.dataset_root)
    images_dir = dataset_root / "images" / args.split
    labels_dir = dataset_root / "labels" / args.split
    weights_path = resolve_project_path(target.weights)
    if not weights_path.exists():
        raise FileNotFoundError(f"Missing weights: {weights_path}")

    model = YOLO(str(weights_path))
    iouv = np.linspace(0.5, 0.95, 10)
    stats: dict[str, dict[str, list]] = {
        scale: {"tp": [], "conf": [], "pred_cls": [], "target_cls": []} for scale, _, _ in SCALE_BINS
    }
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"gt": 0, "pred": 0})

    label_paths = sorted(labels_dir.glob("*.txt"))
    if args.limit_images is not None:
        label_paths = label_paths[: args.limit_images]

    for label_path in label_paths:
        image_path = find_image(images_dir, label_path.stem)
        if image_path is None:
            continue
        width, height = image_size(image_path)
        gt_boxes = load_gt(label_path, width, height)
        result = model.predict(
            source=str(image_path),
            imgsz=target.imgsz,
            conf=args.conf,
            iou=args.nms_iou,
            max_det=args.max_det,
            device=args.device,
            verbose=False,
        )[0]
        pred_boxes = predictions_from_result(result)

        for scale, _, _ in SCALE_BINS:
            scale_targets = [box for box in gt_boxes if box.scale == scale]
            if args.prediction_scale_policy == "same-bin":
                scale_predictions = [box for box in pred_boxes if box.scale == scale]
            else:
                scale_predictions = pred_boxes

            correct = match_predictions(scale_predictions, scale_targets, iouv)
            stats[scale]["tp"].append(correct)
            stats[scale]["conf"].extend(box.conf for box in scale_predictions)
            stats[scale]["pred_cls"].extend(box.cls for box in scale_predictions)
            stats[scale]["target_cls"].extend(box.cls for box in scale_targets)
            counts[scale]["gt"] += len(scale_targets)
            counts[scale]["pred"] += len(scale_predictions)

    rows = []
    for scale, _, _ in SCALE_BINS:
        metric = summarize_ap(
            stats[scale]["tp"],
            stats[scale]["conf"],
            stats[scale]["pred_cls"],
            stats[scale]["target_cls"],
        )
        rows.append(
            {
                "model": target.model,
                "dataset": args.dataset_name or dataset_root.name,
                "weights": target.weights,
                "split": args.split,
                "imgsz": target.imgsz,
                "nms_conf": args.conf,
                "nms_iou": args.nms_iou,
                "max_det": args.max_det,
                "prediction_scale_policy": args.prediction_scale_policy,
                "scale": scale,
                "gt_instances": counts[scale]["gt"],
                "predictions": counts[scale]["pred"],
                "classes_with_gt": metric["classes"],
                "precision_at_max_f1": f"{metric['precision']:.6f}",
                "recall_at_max_f1": f"{metric['recall']:.6f}",
                "ap50": f"{metric['ap50']:.6f}",
                "map50_95": f"{metric['map50_95']:.6f}",
                "metric_note": "Local scale-bin AP; not official COCO/VisDrone AP_small.",
            }
        )
    return rows


def write_ap50_plot(output_path: Path, rows: list[dict[str, str]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"Skip plotting because matplotlib is unavailable: {exc}")
        return

    models: list[str] = []
    for row in rows:
        if row["model"] not in models:
            models.append(row["model"])
    scales = [name for name, _, _ in SCALE_BINS]
    values = {
        model: [float(next(row["ap50"] for row in rows if row["model"] == model and row["scale"] == scale)) for scale in scales]
        for model in models
    }

    x_positions = list(range(len(scales)))
    width = 0.34 if len(models) <= 2 else 0.18
    offsets = [width * (index - (len(models) - 1) / 2.0) for index in range(len(models))]

    fig, ax = plt.subplots(figsize=(7.0, 3.8), dpi=200)
    for offset, model in zip(offsets, models):
        ax.bar([x + offset for x in x_positions], values[model], width=width, label=model)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(scales)
    ax.set_ylabel("Scale-bin AP50")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.35)
    ax.legend(frameon=False, fontsize=7)
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
    for target in load_targets(args.targets_csv):
        rows.extend(evaluate_target(args, target))
        if args.device not in (None, "cpu") and torch.cuda.is_available():
            torch.cuda.empty_cache()

    fieldnames = [
        "model",
        "dataset",
        "weights",
        "split",
        "imgsz",
        "nms_conf",
        "nms_iou",
        "max_det",
        "prediction_scale_policy",
        "scale",
        "gt_instances",
        "predictions",
        "classes_with_gt",
        "precision_at_max_f1",
        "recall_at_max_f1",
        "ap50",
        "map50_95",
        "metric_note",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    write_ap50_plot(resolve_project_path(args.plot_output), rows)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()

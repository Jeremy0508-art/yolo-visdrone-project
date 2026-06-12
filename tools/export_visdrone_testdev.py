from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path

from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.constants import IMAGE_EXTENSIONS
from src.models.register import register_custom_modules
from src.utils.paths import resolve_project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export VisDrone test-dev predictions in official submission format.")
    parser.add_argument(
        "--weights",
        default="runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt",
        help="Model weights used for test-dev prediction.",
    )
    parser.add_argument(
        "--source",
        default="data/processed/visdrone_yolo/images/test",
        help="VisDrone test-dev image directory.",
    )
    parser.add_argument("--imgsz", type=int, default=960, help="Prediction image size.")
    parser.add_argument("--conf", type=float, default=0.001, help="Confidence threshold.")
    parser.add_argument("--iou", type=float, default=0.7, help="NMS IoU threshold.")
    parser.add_argument("--max-det", type=int, default=500, help="Maximum detections per image.")
    parser.add_argument("--device", default="0", help="Device, for example 0 or cpu.")
    parser.add_argument("--output-dir", default="runs/testdev_submit/yolo11n_p2_coordatt_960", help="Output directory.")
    parser.add_argument("--zip-name", default="visdrone_testdev_submit.zip", help="Submission zip filename.")
    return parser.parse_args()


def find_images(source: Path) -> list[Path]:
    if not source.is_dir():
        raise NotADirectoryError(f"Missing image directory: {source}")
    images = sorted(path for path in source.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        raise FileNotFoundError(f"No images found in {source}")
    return images


def format_detection(xyxy, score: float, cls_id: int) -> str:
    left = float(xyxy[0])
    top = float(xyxy[1])
    right = float(xyxy[2])
    bottom = float(xyxy[3])
    width = max(0.0, right - left)
    height = max(0.0, bottom - top)
    visdrone_cls = cls_id + 1
    return f"{left:.2f},{top:.2f},{width:.2f},{height:.2f},{score:.6f},{visdrone_cls},-1,-1"


def write_prediction_file(txt_path: Path, result) -> int:
    lines = []
    boxes = result.boxes
    if boxes is not None and len(boxes) > 0:
        xyxy_values = boxes.xyxy.cpu().numpy()
        score_values = boxes.conf.cpu().numpy()
        cls_values = boxes.cls.cpu().numpy().astype(int)
        for xyxy, score, cls_id in zip(xyxy_values, score_values, cls_values):
            lines.append(format_detection(xyxy, float(score), int(cls_id)))

    txt_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def create_zip(txt_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for txt_path in sorted(txt_dir.glob("*.txt")):
            archive.write(txt_path, arcname=txt_path.name)


def write_manifest(manifest_path: Path, rows: list[dict[str, str]]) -> None:
    with manifest_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    register_custom_modules()
    args = parse_args()

    weights = resolve_project_path(args.weights)
    source = resolve_project_path(args.source)
    output_dir = resolve_project_path(args.output_dir)
    txt_dir = output_dir / "txt"
    zip_path = output_dir / args.zip_name
    manifest_path = output_dir / "manifest.csv"

    if not weights.exists():
        raise FileNotFoundError(f"Missing weights: {weights}")

    images = find_images(source)
    txt_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    for old_txt in txt_dir.glob("*.txt"):
        old_txt.unlink()

    model = YOLO(str(weights))
    results = model.predict(
        source=str(source),
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        device=args.device,
        save=False,
        verbose=False,
        stream=True,
    )

    manifest_rows = []
    total_detections = 0
    seen = set()
    for result in results:
        image_path = Path(result.path)
        txt_path = txt_dir / f"{image_path.stem}.txt"
        detections = write_prediction_file(txt_path, result)
        total_detections += detections
        seen.add(image_path.name)
        manifest_rows.append(
            {
                "image": image_path.name,
                "txt": txt_path.name,
                "detections": str(detections),
                "weights": args.weights,
                "imgsz": str(args.imgsz),
                "conf": str(args.conf),
                "iou": str(args.iou),
                "max_det": str(args.max_det),
            }
        )

    missing = [path for path in images if path.name not in seen]
    for image_path in missing:
        txt_path = txt_dir / f"{image_path.stem}.txt"
        txt_path.write_text("", encoding="utf-8")
        manifest_rows.append(
            {
                "image": image_path.name,
                "txt": txt_path.name,
                "detections": "0",
                "weights": args.weights,
                "imgsz": str(args.imgsz),
                "conf": str(args.conf),
                "iou": str(args.iou),
                "max_det": str(args.max_det),
            }
        )

    manifest_rows = sorted(manifest_rows, key=lambda row: row["image"])
    write_manifest(manifest_path, manifest_rows)
    create_zip(txt_dir, zip_path)

    print(f"Images: {len(images)}")
    print(f"Prediction txt files: {len(list(txt_dir.glob('*.txt')))}")
    print(f"Total detections: {total_detections}")
    print(f"Manifest: {manifest_path}")
    print(f"Submission zip: {zip_path}")


if __name__ == "__main__":
    main()

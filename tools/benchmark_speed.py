from __future__ import annotations

import argparse
import csv
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.register import register_custom_modules
from src.utils.paths import resolve_project_path


@dataclass(frozen=True)
class BenchmarkTarget:
    model: str
    weights: str
    imgsz: int


TARGETS = [
    BenchmarkTarget(
        model="YOLOv8n baseline",
        weights="runs/detect/baseline_yolov8n_visdrone/weights/best.pt",
        imgsz=640,
    ),
    BenchmarkTarget(
        model="YOLO11n baseline",
        weights="runs/detect/baseline_yolo11n_visdrone/weights/best.pt",
        imgsz=640,
    ),
    BenchmarkTarget(
        model="YOLO11n-P2",
        weights="runs/detect/yolo11n_p2_pretrained_visdrone/weights/best.pt",
        imgsz=640,
    ),
    BenchmarkTarget(
        model="YOLO11n-P2-CoordAttention",
        weights="runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt",
        imgsz=640,
    ),
    BenchmarkTarget(
        model="YOLO11n-P2-CoordAttention-SmallObjAug",
        weights="runs/detect/yolo11n_p2_coordatt_smallobj_aug_visdrone/weights/best.pt",
        imgsz=640,
    ),
    BenchmarkTarget(
        model="YOLO11n-P2-CoordAttention-960",
        weights="runs/detect/yolo11n_p2_coordatt_960_visdrone_full/weights/best.pt",
        imgsz=960,
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark YOLO inference speed for paper tables.")
    parser.add_argument("--source", default="data/processed/visdrone_yolo/images/val", help="Image directory.")
    parser.add_argument("--output", default="paper/tables/speed_results.csv", help="Output CSV path.")
    parser.add_argument("--device", default="0", help="Device, for example 0 or cpu.")
    parser.add_argument("--warmup", type=int, default=10, help="Warmup single-image predictions per model.")
    parser.add_argument("--samples", type=int, default=100, help="Timed single-image predictions per model.")
    parser.add_argument("--conf", type=float, default=0.25, help="Prediction confidence threshold.")
    return parser.parse_args()


def collect_images(source: Path, count: int) -> list[Path]:
    if not source.is_dir():
        raise NotADirectoryError(f"Missing source directory: {source}")
    images = sorted(
        path
        for path in source.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    )
    if not images:
        raise FileNotFoundError(f"No images found in {source}")
    repeated = []
    while len(repeated) < count:
        repeated.extend(images)
    return repeated[:count]


def synchronize_if_cuda(device: str) -> None:
    if device == "cpu":
        return
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.synchronize()
    except Exception:
        return


def benchmark_target(
    target: BenchmarkTarget,
    images: list[Path],
    warmup_images: list[Path],
    device: str,
    conf: float,
) -> dict[str, str]:
    weights_path = resolve_project_path(target.weights)
    if not weights_path.exists():
        raise FileNotFoundError(f"Missing weights: {weights_path}")

    model = YOLO(str(weights_path))
    for image_path in warmup_images:
        model.predict(
            source=str(image_path),
            imgsz=target.imgsz,
            conf=conf,
            device=device,
            save=False,
            verbose=False,
        )

    latencies_ms = []
    speed_preprocess = []
    speed_inference = []
    speed_postprocess = []
    for image_path in images:
        synchronize_if_cuda(device)
        start = time.perf_counter()
        results = model.predict(
            source=str(image_path),
            imgsz=target.imgsz,
            conf=conf,
            device=device,
            save=False,
            verbose=False,
        )
        synchronize_if_cuda(device)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        latencies_ms.append(elapsed_ms)

        if results:
            speed = results[0].speed
            speed_preprocess.append(float(speed.get("preprocess", 0.0)))
            speed_inference.append(float(speed.get("inference", 0.0)))
            speed_postprocess.append(float(speed.get("postprocess", 0.0)))

    mean_latency = statistics.mean(latencies_ms)
    median_latency = statistics.median(latencies_ms)
    fps = 1000.0 / mean_latency if mean_latency else 0.0

    return {
        "model": target.model,
        "weights": target.weights,
        "imgsz": str(target.imgsz),
        "device": device,
        "warmup": str(len(warmup_images)),
        "samples": str(len(images)),
        "mean_latency_ms_wall": f"{mean_latency:.3f}",
        "median_latency_ms_wall": f"{median_latency:.3f}",
        "fps_wall": f"{fps:.2f}",
        "mean_preprocess_ms_ultralytics": f"{statistics.mean(speed_preprocess):.3f}" if speed_preprocess else "",
        "mean_inference_ms_ultralytics": f"{statistics.mean(speed_inference):.3f}" if speed_inference else "",
        "mean_postprocess_ms_ultralytics": f"{statistics.mean(speed_postprocess):.3f}" if speed_postprocess else "",
        "source": "single-image model.predict wall-clock timing and Ultralytics result.speed",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    register_custom_modules()
    args = parse_args()

    source = resolve_project_path(args.source)
    images = collect_images(source, args.samples)
    warmup_images = collect_images(source, args.warmup)

    rows = []
    for target in TARGETS:
        print(f"Benchmarking {target.model} at imgsz={target.imgsz}...")
        rows.append(benchmark_target(target, images, warmup_images, args.device, args.conf))

    output = resolve_project_path(args.output)
    write_csv(output, rows)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

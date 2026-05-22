import argparse
import importlib
import importlib.metadata
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils.paths import resolve_project_path


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the YOLO VisDrone project layout and key artifacts.")
    parser.add_argument("--dataset-root", default="data/processed/visdrone_yolo", help="YOLO-format dataset root.")
    parser.add_argument(
        "--weights",
        default="runs/detect/yolo11n_p2_coordatt_visdrone/weights/best.pt",
        help="Primary model weights used for demo.",
    )
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code when warnings exist.")
    return parser.parse_args()


def ok(name: str, detail: str) -> CheckResult:
    return CheckResult(name, "PASS", detail)


def warn(name: str, detail: str) -> CheckResult:
    return CheckResult(name, "WARN", detail)


def fail(name: str, detail: str) -> CheckResult:
    return CheckResult(name, "FAIL", detail)


def check_path(path: str, name: str, kind: str = "file", required: bool = True) -> CheckResult:
    resolved = resolve_project_path(path)
    exists = resolved.is_dir() if kind == "dir" else resolved.is_file()
    if exists:
        return ok(name, str(resolved))
    message = f"Missing {kind}: {resolved}"
    return fail(name, message) if required else warn(name, message)


def check_imports() -> list[CheckResult]:
    results = []
    for module_name in ["ultralytics", "cv2", "flask", "yaml", "PIL"]:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:
            results.append(fail(f"import {module_name}", repr(exc)))
            continue
        package_name = "opencv-python" if module_name == "cv2" else "Pillow" if module_name == "PIL" else module_name
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            version = getattr(module, "__version__", "installed")
        results.append(ok(f"import {module_name}", str(version)))
    return results


def check_dataset_yaml() -> list[CheckResult]:
    yaml_path = resolve_project_path("configs/dataset/visdrone.yaml")
    if not yaml_path.is_file():
        return [fail("dataset yaml", f"Missing file: {yaml_path}")]

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [fail("dataset yaml", f"Cannot parse YAML: {exc}")]

    results = [ok("dataset yaml", str(yaml_path))]
    names = data.get("names", {})
    if len(names) == 10:
        results.append(ok("dataset classes", "10 classes"))
    else:
        results.append(fail("dataset classes", f"Expected 10 classes, got {len(names)}"))

    dataset_root = resolve_project_path(data.get("path", ""))
    if dataset_root.is_dir():
        results.append(ok("dataset yaml path", str(dataset_root)))
    else:
        results.append(fail("dataset yaml path", f"Missing directory: {dataset_root}"))
    return results


def check_dataset_files(dataset_root: Path) -> list[CheckResult]:
    results = []
    expected = {
        "train": 6471,
        "val": 548,
        "test": 1580,
    }
    for split, expected_images in expected.items():
        image_dir = dataset_root / "images" / split
        label_dir = dataset_root / "labels" / split
        if not image_dir.is_dir():
            results.append(fail(f"{split} images", f"Missing directory: {image_dir}"))
            continue
        images = [p for p in image_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]
        status = ok if len(images) == expected_images else warn
        results.append(status(f"{split} image count", f"{len(images)} images, expected {expected_images}"))

        if label_dir.is_dir():
            labels = list(label_dir.glob("*.txt"))
            if split == "test":
                detail = f"{len(labels)} label files; test-dev labels are expected to be empty placeholders"
                results.append(ok(f"{split} labels", detail))
            else:
                status = ok if len(labels) == len(images) else warn
                results.append(status(f"{split} label count", f"{len(labels)} labels for {len(images)} images"))
        else:
            results.append(fail(f"{split} labels", f"Missing directory: {label_dir}"))
    return results


def check_flask_app() -> list[CheckResult]:
    results = [check_path("web/app.py", "flask app")]
    try:
        from web.app import create_app

        app = create_app()
        client = app.test_client()
        response = client.get("/")
        if response.status_code == 200:
            results.append(ok("flask index", "GET / returned 200"))
        else:
            results.append(fail("flask index", f"GET / returned {response.status_code}"))
    except Exception as exc:
        results.append(fail("flask app import", repr(exc)))
    return results


def build_checks(args: argparse.Namespace) -> list[CheckResult]:
    dataset_root = resolve_project_path(args.dataset_root)
    checks: list[CheckResult] = []
    checks.extend(check_imports())
    checks.extend(
        [
            check_path("configs/dataset/visdrone.yaml", "dataset config"),
            check_path("configs/train/baseline_yolo11n.yaml", "baseline train config"),
            check_path("configs/train/yolo11n_eca.yaml", "eca train config"),
            check_path("configs/train/yolo11n_eca_fair.yaml", "eca fair train config"),
            check_path("configs/train/yolo11n_p2.yaml", "p2 train config"),
            check_path("configs/train/yolo11n_p2_coordatt.yaml", "p2 coordatt train config"),
            check_path("configs/models/yolo11n_eca.yaml", "eca model config"),
            check_path("configs/models/yolo11n_p2.yaml", "p2 model config"),
            check_path("configs/models/yolo11n_p2_coordatt.yaml", "p2 coordatt model config"),
            check_path("scripts/convert_visdrone_to_yolo.py", "conversion script"),
            check_path("scripts/check_dataset.py", "dataset check script"),
            check_path("tools/train_baseline.py", "training script"),
            check_path("tools/val.py", "validation script"),
            check_path("tools/detect_image.py", "image detection script"),
            check_path("tools/detect_video.py", "video detection script"),
            check_path(args.weights, "primary weights"),
            check_path("experiments/ablations/ablation_summary.md", "ablation summary"),
            check_path("experiments/presentation_outline.md", "presentation outline"),
            check_path("experiments/demo_checklist.md", "demo checklist"),
            check_path("experiments/cases/p2_case_contact_sheet.jpg", "case contact sheet"),
            check_path("experiments/figures", "figures directory", kind="dir"),
        ]
    )
    checks.extend(check_dataset_yaml())
    checks.extend(check_dataset_files(dataset_root))
    checks.extend(check_flask_app())
    return checks


def print_results(results: list[CheckResult]) -> None:
    width = max(len(result.name) for result in results)
    for result in results:
        print(f"[{result.status}] {result.name:<{width}} {result.detail}")

    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for result in results:
        counts[result.status] += 1
    print()
    print(f"Summary: PASS={counts['PASS']} WARN={counts['WARN']} FAIL={counts['FAIL']}")


def main() -> None:
    args = parse_args()
    results = build_checks(args)
    print_results(results)

    has_fail = any(result.status == "FAIL" for result in results)
    has_warn = any(result.status == "WARN" for result in results)
    if has_fail or (args.strict and has_warn):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

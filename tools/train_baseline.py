from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from ultralytics import YOLO

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.register import register_custom_modules
from src.utils.paths import materialize_absolute_dataset_yaml, resolve_project_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an Ultralytics YOLO baseline on VisDrone.")
    parser.add_argument("--config", default="configs/train/baseline_yolo11n.yaml", help="Training config path.")
    parser.add_argument("--model", default=None, help="Override model checkpoint, for example yolo11n.pt or yolov8n.pt.")
    parser.add_argument("--data", default=None, help="Override dataset yaml path.")
    parser.add_argument("--epochs", type=int, default=None, help="Override training epochs.")
    parser.add_argument("--imgsz", type=int, default=None, help="Override image size.")
    parser.add_argument("--batch", type=int, default=None, help="Override batch size.")
    parser.add_argument("--device", default=None, help="Override device, for example 0 or cpu.")
    parser.add_argument("--workers", type=int, default=None, help="Override dataloader workers.")
    parser.add_argument("--project", default=None, help="Override output project directory.")
    parser.add_argument("--name", default=None, help="Override output run name.")
    parser.add_argument("--fraction", type=float, default=None, help="Use a fraction of training data for smoke tests.")
    parser.add_argument("--resume", default=None, help="Resume from a previous checkpoint, for example runs/detect/exp/weights/last.pt.")
    parser.add_argument(
        "--pretrained-weights",
        default=None,
        help="Partially load YOLO11 weights before training for supported custom YOLO11 variants.",
    )
    parser.add_argument(
        "--pretrained-mode",
        choices=["auto", "p2"],
        default="auto",
        help="Layer remapping mode for --pretrained-weights.",
    )
    parser.add_argument(
        "--init-output",
        default="weights/yolo11n_p2_pretrained_init.pt",
        help="Where to save the remapped initialization checkpoint when --pretrained-weights is used.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    return config


def infer_pretrained_mode(model_name: str, requested_mode: str) -> str:
    if requested_mode != "auto":
        return requested_mode

    lowered = model_name.lower()
    if "p2" in lowered:
        return "p2"
    raise ValueError("Could not infer pretrained mode. Pass --pretrained-mode p2.")


def get_layer_map(mode: str) -> dict[int, int]:
    if mode == "p2":
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            13: 13,
            16: 16,
        }
    raise ValueError(f"Unsupported pretrained mode: {mode}")


def transfer_yolo11_weights(target: YOLO, weights_path: Path, mode: str) -> None:
    source = YOLO(str(weights_path))
    source_layers = source.model.model
    target_layers = target.model.model
    layer_map = get_layer_map(mode)

    transferred = 0
    skipped = []
    for source_idx, target_idx in layer_map.items():
        source_state = source_layers[source_idx].state_dict()
        target_layer = target_layers[target_idx]
        target_state = target_layer.state_dict()
        compatible = {
            key: value
            for key, value in source_state.items()
            if key in target_state and target_state[key].shape == value.shape
        }
        if compatible:
            target_state.update(compatible)
            target_layer.load_state_dict(target_state, strict=False)
            transferred += len(compatible)
        else:
            skipped.append(f"{source_idx}->{target_idx}")

    print(f"Transferred {transferred} tensors from {weights_path} with YOLO11-to-{mode.upper()} remapping.")
    if skipped:
        print(f"Skipped layer mappings without compatible tensors: {', '.join(skipped)}")


def main() -> None:
    register_custom_modules()
    args = parse_args()
    config_path = resolve_project_path(args.config)
    config = load_config(config_path)

    overrides = {
        "model": args.model,
        "data": args.data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "workers": args.workers,
        "project": args.project,
        "name": args.name,
        "fraction": args.fraction,
    }
    config.update({key: value for key, value in overrides.items() if value is not None})

    if args.resume is not None:
        config["resume"] = str(resolve_project_path(args.resume))

    for path_key in ("data", "project"):
        if path_key in config and config[path_key] is not None:
            config[path_key] = str(resolve_project_path(config[path_key]))
    if "data" in config and config["data"] is not None:
        config["data"] = str(materialize_absolute_dataset_yaml(config["data"]))

    model_name = config.pop("model", "yolo11n.pt")
    model = YOLO(model_name)
    if args.pretrained_weights is not None:
        pretrained_mode = infer_pretrained_mode(model_name, args.pretrained_mode)
        transfer_yolo11_weights(model, resolve_project_path(args.pretrained_weights), pretrained_mode)
        init_output = resolve_project_path(args.init_output)
        init_output.parent.mkdir(parents=True, exist_ok=True)
        model.save(init_output)
        print(f"Saved remapped initialization checkpoint to {init_output}")
        model = YOLO(str(init_output))
    model.train(**config)


if __name__ == "__main__":
    main()

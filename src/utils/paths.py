from __future__ import annotations

from pathlib import Path

import yaml

from src.constants import PROJECT_ROOT


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def ensure_dir(path: str | Path) -> Path:
    resolved = Path(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def materialize_absolute_dataset_yaml(path: str | Path, output_dir: str | Path = "runs/generated_configs") -> Path:
    """Create a dataset YAML whose dataset root is absolute.

    Ultralytics may resolve a relative `path` inside a dataset YAML against its
    global datasets directory. This helper preserves the project's convention
    that relative dataset roots are relative to the repository root.
    """
    source_path = resolve_project_path(path)
    config = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
    dataset_root = config.get("path")
    if dataset_root is not None:
        dataset_root_path = Path(dataset_root)
        if not dataset_root_path.is_absolute():
            config["path"] = str(resolve_project_path(dataset_root_path))

    generated_dir = resolve_project_path(output_dir)
    generated_dir.mkdir(parents=True, exist_ok=True)
    generated_path = generated_dir / f"{source_path.stem}_absolute.yaml"
    generated_path.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return generated_path

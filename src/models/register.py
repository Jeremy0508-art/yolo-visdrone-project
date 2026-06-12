from __future__ import annotations

from ultralytics.nn import tasks

from src.models.attention import CoordAttention


def register_custom_modules() -> None:
    """Register project modules for Ultralytics YAML parsing."""
    tasks.CoordAttention = CoordAttention

from ultralytics.nn import tasks

from src.models.attention import CoordAttention, ECAAttention


def register_custom_modules() -> None:
    """Register project modules for Ultralytics YAML parsing."""
    tasks.CoordAttention = CoordAttention
    tasks.ECAAttention = ECAAttention

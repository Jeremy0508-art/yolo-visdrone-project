from ultralytics.nn import tasks

from src.models.attention import ECAAttention


def register_custom_modules() -> None:
    """Register project modules for Ultralytics YAML parsing."""
    tasks.ECAAttention = ECAAttention


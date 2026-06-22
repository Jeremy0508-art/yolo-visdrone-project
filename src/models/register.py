from __future__ import annotations

from ultralytics.nn import tasks

from src.models.attention import (
    CoordAttention,
    CrossScaleP2P3ConsistencyGate,
    ScaleAwareP2Gate,
    TinyObjectFeatureCalibration,
)


def register_custom_modules() -> None:
    """Register project modules for Ultralytics YAML parsing."""
    tasks.CoordAttention = CoordAttention
    tasks.CrossScaleP2P3ConsistencyGate = CrossScaleP2P3ConsistencyGate
    tasks.ScaleAwareP2Gate = ScaleAwareP2Gate
    tasks.TinyObjectFeatureCalibration = TinyObjectFeatureCalibration

from __future__ import annotations

import torch
from torch import nn


class TinyObjectFeatureCalibration(nn.Module):
    """Lightweight residual calibration block for high-resolution small-object features."""

    def __init__(self, channels: int, reduction: int = 4) -> None:
        super().__init__()
        hidden_channels = max(8, channels // reduction)
        self.local = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1, groups=channels, bias=False),
            nn.BatchNorm2d(channels),
            nn.SiLU(),
            nn.Conv2d(channels, channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(channels),
            nn.SiLU(),
        )
        self.channel_gate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(channels, hidden_channels, kernel_size=1, stride=1, padding=0),
            nn.SiLU(),
            nn.Conv2d(hidden_channels, channels, kernel_size=1, stride=1, padding=0),
            nn.Sigmoid(),
        )
        self.spatial_gate = nn.Sequential(
            nn.Conv2d(2, 1, kernel_size=7, stride=1, padding=3, bias=False),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        local = self.local(x)
        avg_map = local.mean(dim=1, keepdim=True)
        max_map = local.amax(dim=1, keepdim=True)
        spatial_weight = self.spatial_gate(torch.cat([avg_map, max_map], dim=1))
        channel_weight = self.channel_gate(local)
        return x + local * spatial_weight * channel_weight

from __future__ import annotations

import torch
from torch import nn


class ScaleAwareP2Gate(nn.Module):
    """Identity-initialized gate for high-resolution P2 features.

    The block is designed for the P2 branch in lightweight UAV detectors. It
    keeps the initial network behavior close to the plain P2 head, then learns
    a bounded local/channel modulation so the shallow branch can emphasize
    useful fine details without forcing every dataset to rely on them equally.
    """

    def __init__(self, channels: int, reduction: int = 4, max_delta: float = 0.5) -> None:
        super().__init__()
        hidden_channels = max(8, channels // reduction)
        self.max_delta = float(max_delta)
        self.local_context = nn.Sequential(
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
            nn.Conv2d(2, 1, kernel_size=5, stride=1, padding=2, bias=False),
            nn.Sigmoid(),
        )
        self.gain = nn.Parameter(torch.zeros(1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        context = self.local_context(x)
        avg_map = context.mean(dim=1, keepdim=True)
        max_map = context.amax(dim=1, keepdim=True)
        spatial_weight = self.spatial_gate(torch.cat([avg_map, max_map], dim=1))
        channel_weight = self.channel_gate(context)
        modulation = spatial_weight * channel_weight
        bounded_gain = torch.tanh(self.gain) * self.max_delta
        return x + bounded_gain * context * modulation

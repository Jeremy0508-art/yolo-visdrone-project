from __future__ import annotations

import torch
from torch import nn


class CoordAttention(nn.Module):
    """Coordinate Attention block for feature maps with fixed channels."""

    def __init__(self, channels: int, reduction: int = 32) -> None:
        super().__init__()
        reduced_channels = max(8, channels // reduction)
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))
        self.conv1 = nn.Conv2d(channels, reduced_channels, kernel_size=1, stride=1, padding=0)
        self.bn1 = nn.BatchNorm2d(reduced_channels)
        self.act = nn.SiLU()
        self.conv_h = nn.Conv2d(reduced_channels, channels, kernel_size=1, stride=1, padding=0)
        self.conv_w = nn.Conv2d(reduced_channels, channels, kernel_size=1, stride=1, padding=0)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        _, _, height, width = x.size()

        x_h = self.pool_h(x)
        x_w = self.pool_w(x).permute(0, 1, 3, 2)
        y = torch.cat([x_h, x_w], dim=2)
        y = self.act(self.bn1(self.conv1(y)))

        x_h, x_w = torch.split(y, [height, width], dim=2)
        x_w = x_w.permute(0, 1, 3, 2)

        attention_h = self.sigmoid(self.conv_h(x_h))
        attention_w = self.sigmoid(self.conv_w(x_w))
        return identity * attention_h * attention_w

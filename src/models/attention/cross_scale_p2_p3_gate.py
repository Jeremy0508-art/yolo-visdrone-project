from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn


class CrossScaleP2P3ConsistencyGate(nn.Module):
    """Identity-initialized P2 gate conditioned on neighboring P3 context.

    ScaleAwareP2Gate only modulates the P2 feature itself. This block is a
    second-cycle response to mixed ScaleGate evidence: it compares local P2
    detail with upsampled P3 semantic context, then applies a bounded residual
    correction to P2. The learnable gain is initialized to zero, so the module
    starts from the plain P2 path and cannot create a paper claim without
    completed training evidence.
    """

    def __init__(
        self,
        p2_channels: int,
        p3_channels: int,
        reduction: int = 4,
        max_delta: float = 0.5,
    ) -> None:
        super().__init__()
        self.p2_channels = int(p2_channels)
        self.p3_channels = int(p3_channels)
        hidden_channels = max(8, p2_channels // reduction)
        self.max_delta = float(max_delta)
        self.p2_context = nn.Sequential(
            nn.Conv2d(p2_channels, p2_channels, kernel_size=3, stride=1, padding=1, groups=p2_channels, bias=False),
            nn.BatchNorm2d(p2_channels),
            nn.SiLU(),
            nn.Conv2d(p2_channels, p2_channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(p2_channels),
            nn.SiLU(),
        )
        self.p3_projection = nn.Sequential(
            nn.Conv2d(p3_channels, p2_channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(p2_channels),
            nn.SiLU(),
        )
        self.consistency_gate = nn.Sequential(
            nn.Conv2d(p2_channels * 2, hidden_channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(hidden_channels),
            nn.SiLU(),
            nn.Conv2d(hidden_channels, p2_channels, kernel_size=5, stride=1, padding=2, bias=False),
            nn.Sigmoid(),
        )
        self.gain = nn.Parameter(torch.zeros(1))

    def forward(self, inputs: torch.Tensor | list[torch.Tensor] | tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
        if isinstance(inputs, torch.Tensor):
            expected_channels = self.p2_channels + self.p3_channels
            if inputs.shape[1] != expected_channels:
                raise ValueError(
                    "CrossScaleP2P3ConsistencyGate expected "
                    f"{expected_channels} concatenated channels, got {inputs.shape[1]}."
                )
            p2 = inputs[:, : self.p2_channels]
            p3 = inputs[:, self.p2_channels :]
            return_concat = True
        elif isinstance(inputs, (list, tuple)) and len(inputs) == 2:
            p2, p3 = inputs
            return_concat = False
        else:
            raise TypeError("CrossScaleP2P3ConsistencyGate expects a concatenated tensor or [p2_feature, p3_feature].")

        p2_context = self.p2_context(p2)
        p3_context = self.p3_projection(p3)
        if p3_context.shape[-2:] != p2_context.shape[-2:]:
            p3_context = F.interpolate(p3_context, size=p2_context.shape[-2:], mode="nearest")
        gate = self.consistency_gate(torch.cat([p2_context, p3_context], dim=1))
        bounded_gain = torch.tanh(self.gain) * self.max_delta
        adapted_p2 = p2 + bounded_gain * gate * (p2_context - p3_context)
        if return_concat:
            return torch.cat([adapted_p2, p3], dim=1)
        return adapted_p2

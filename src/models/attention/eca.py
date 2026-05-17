import torch
from torch import nn


class ECAAttention(nn.Module):
    """Efficient Channel Attention block.

    This implementation keeps the input shape unchanged, so it can be inserted
    between YOLO feature layers and the detection head.
    """

    def __init__(self, kernel_size: int = 3) -> None:
        super().__init__()
        if kernel_size % 2 == 0:
            raise ValueError("ECA kernel_size must be odd.")
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.conv = nn.Conv1d(1, 1, kernel_size=kernel_size, padding=(kernel_size - 1) // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        weights = self.avg_pool(x)
        weights = self.conv(weights.squeeze(-1).transpose(-1, -2))
        weights = self.sigmoid(weights.transpose(-1, -2).unsqueeze(-1))
        return x * weights.expand_as(x)


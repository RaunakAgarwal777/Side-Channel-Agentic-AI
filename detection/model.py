"""
model.py - CNN classifier for side-channel attack detection.
A 1D-CNN over trace segments; swap for a Transformer encoder later
without touching predict.py/metrics.py (same interface).
"""

import torch
import torch.nn as nn


class SideChannelCNN(nn.Module):
    def __init__(self, input_length: int, num_classes: int = 2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=7, padding=3),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch, trace_length) -> add channel dim
        if x.dim() == 2:
            x = x.unsqueeze(1)
        x = self.features(x)
        return self.classifier(x)


def build_model(input_length: int, num_classes: int = 2, device: str = "cpu") -> SideChannelCNN:
    model = SideChannelCNN(input_length=input_length, num_classes=num_classes)
    return model.to(device)

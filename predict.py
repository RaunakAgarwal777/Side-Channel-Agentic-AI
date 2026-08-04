"""
predict.py - Training loop, checkpointing, and inference for SideChannelCNN.
"""

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np

from model import build_model


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 20,
    batch_size: int = 32,
    lr: float = 1e-3,
    device: str = "cpu",
    checkpoint_path: str = "sidechannel_cnn.pt",
):
    model = build_model(input_length=X_train.shape[1], device=device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    train_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)

    val_X = torch.tensor(X_val, dtype=torch.float32).to(device)
    val_y = torch.tensor(y_val, dtype=torch.long).to(device)

    best_val_acc = 0.0

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        model.eval()
        with torch.no_grad():
            val_preds = model(val_X).argmax(dim=1)
            val_acc = (val_preds == val_y).float().mean().item()

        print(f"Epoch {epoch+1}/{epochs} - loss: {total_loss/len(train_loader):.4f} - val_acc: {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), checkpoint_path)

    print(f"Best val_acc: {best_val_acc:.4f}. Checkpoint saved to {checkpoint_path}")
    return model


def load_model(checkpoint_path: str, input_length: int, device: str = "cpu"):
    model = build_model(input_length=input_length, device=device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model


def predict(model, X: np.ndarray, device: str = "cpu") -> dict:
    """Returns verdict, confidence, and raw probabilities for a batch of traces."""
    model.eval()
    with torch.no_grad():
        xb = torch.tensor(X, dtype=torch.float32).to(device)
        logits = model(xb)
        probs = torch.softmax(logits, dim=1)
        preds = probs.argmax(dim=1)
        confidences = probs.max(dim=1).values

    return {
        "verdicts": ["yes" if p == 1 else "no" for p in preds.tolist()],
        "confidences": confidences.tolist(),
        "probabilities": probs.tolist(),
    }

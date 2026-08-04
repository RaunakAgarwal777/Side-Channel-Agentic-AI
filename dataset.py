"""
dataset.py - Loads and splits side-channel trace datasets (e.g., ASCAD-style).
Expects raw traces as .npy/.h5 or CSV with columns: trace vector + label.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple
from sklearn.model_selection import train_test_split


@dataclass
class SideChannelDataset:
    X: np.ndarray  # shape (n_samples, trace_length)
    y: np.ndarray  # shape (n_samples,) — 0 = benign, 1 = attack


def load_npy_dataset(traces_path: str, labels_path: str) -> SideChannelDataset:
    X = np.load(traces_path)
    y = np.load(labels_path)
    if X.shape[0] != y.shape[0]:
        raise ValueError(f"Mismatched samples: X={X.shape[0]} y={y.shape[0]}")
    return SideChannelDataset(X=X, y=y)


def load_csv_dataset(csv_path: str, label_col: str = "label") -> SideChannelDataset:
    import pandas as pd

    df = pd.read_csv(csv_path)
    y = df[label_col].to_numpy()
    X = df.drop(columns=[label_col]).to_numpy()
    return SideChannelDataset(X=X, y=y)


def split_dataset(
    dataset: SideChannelDataset, test_size: float = 0.2, val_size: float = 0.1, seed: int = 42
) -> Tuple[SideChannelDataset, SideChannelDataset, SideChannelDataset]:
    """Returns (train, val, test) splits, stratified on label."""
    X_train, X_temp, y_train, y_temp = train_test_split(
        dataset.X, dataset.y, test_size=(test_size + val_size), stratify=dataset.y, random_state=seed
    )
    relative_val = val_size / (test_size + val_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=(1 - relative_val), stratify=y_temp, random_state=seed
    )
    return (
        SideChannelDataset(X_train, y_train),
        SideChannelDataset(X_val, y_val),
        SideChannelDataset(X_test, y_test),
    )

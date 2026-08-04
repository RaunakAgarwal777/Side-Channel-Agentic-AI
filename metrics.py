"""
metrics.py - Standard ML evaluation metrics for the detection model:
accuracy, precision, recall, F1, AUROC, confusion matrix.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


def evaluate(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> dict:
    """
    y_true: ground truth labels (0/1)
    y_pred: predicted labels (0/1)
    y_prob: predicted probability of the positive class (for AUROC), optional
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }

    if y_prob is not None:
        try:
            metrics["auroc"] = roc_auc_score(y_true, y_prob)
        except ValueError:
            metrics["auroc"] = None  # e.g., only one class present

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (None, None, None, None)
    metrics["confusion_matrix"] = cm.tolist()
    metrics["fpr"] = fp / (fp + tn) if fp is not None and (fp + tn) > 0 else None
    metrics["fnr"] = fn / (fn + tp) if fn is not None and (fn + tp) > 0 else None

    return metrics


def print_report(metrics: dict):
    print("=== Detection Metrics ===")
    for k, v in metrics.items():
        if k == "confusion_matrix":
            print(f"Confusion Matrix:\n{np.array(v)}")
        else:
            print(f"{k}: {v}")

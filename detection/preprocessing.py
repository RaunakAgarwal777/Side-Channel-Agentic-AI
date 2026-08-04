"""
preprocessing.py - Filtering, normalization, denoising, and segmentation
for raw side-channel traces before feature extraction / model input.
"""

import numpy as np
from scipy.signal import butter, filtfilt


def normalize(X: np.ndarray) -> np.ndarray:
    """Z-score normalize each trace independently."""
    mean = X.mean(axis=1, keepdims=True)
    std = X.std(axis=1, keepdims=True) + 1e-8
    return (X - mean) / std


def bandpass_filter(X: np.ndarray, low_hz: float, high_hz: float, fs: float, order: int = 4) -> np.ndarray:
    """Apply a Butterworth bandpass filter to remove noise outside the band of interest."""
    nyquist = 0.5 * fs
    low = low_hz / nyquist
    high = high_hz / nyquist
    b, a = butter(order, [low, high], btype="band")
    return np.array([filtfilt(b, a, trace) for trace in X])


def denoise_moving_average(X: np.ndarray, window: int = 5) -> np.ndarray:
    """Simple moving-average smoothing to reduce high-frequency noise."""
    kernel = np.ones(window) / window
    return np.array([np.convolve(trace, kernel, mode="same") for trace in X])


def segment_traces(X: np.ndarray, segment_length: int, stride: int = None) -> np.ndarray:
    """Split long traces into fixed-length overlapping/non-overlapping segments."""
    stride = stride or segment_length
    segments = []
    for trace in X:
        for start in range(0, len(trace) - segment_length + 1, stride):
            segments.append(trace[start:start + segment_length])
    return np.array(segments)


def preprocess_pipeline(
    X: np.ndarray, fs: float = 1000.0, low_hz: float = 1.0, high_hz: float = 400.0
) -> np.ndarray:
    """Standard pipeline: bandpass filter -> denoise -> normalize."""
    X = bandpass_filter(X, low_hz, high_hz, fs)
    X = denoise_moving_average(X)
    X = normalize(X)
    return X

"""
latency.py
Tracks per-query latency across the pipeline for observability and
harness reporting.
"""

import statistics
from typing import List, Dict


class LatencyTracker:
    def __init__(self):
        self._samples: List[float] = []

    def record(self, seconds: float):
        self._samples.append(seconds)

    def summary(self) -> Dict[str, float]:
        if not self._samples:
            return {}
        sorted_samples = sorted(self._samples)
        n = len(sorted_samples)
        return {
            "count": n,
            "mean_ms": statistics.mean(sorted_samples) * 1000,
            "p50_ms": sorted_samples[int(n * 0.50)] * 1000,
            "p95_ms": sorted_samples[min(int(n * 0.95), n - 1)] * 1000,
            "p99_ms": sorted_samples[min(int(n * 0.99), n - 1)] * 1000,
            "max_ms": max(sorted_samples) * 1000,
            "min_ms": min(sorted_samples) * 1000,
        }

    def reset(self):
        self._samples = []

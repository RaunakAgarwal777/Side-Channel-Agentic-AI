"""
benchmark.py
The evaluation harness entry point: runs the detector + RAG pipeline
against a held-out dataset and produces accuracy, RAGAS, and latency
results in one shot.
"""

import time
from typing import List, Dict, Any, Callable

from .ragas import run_ragas_eval, summarize_ragas
from .latency import LatencyTracker
from .results import ResultsWriter


class Benchmark:
    def __init__(self, pipeline_fn: Callable[[str], Dict[str, Any]], output_dir: str = "./results"):
        """
        pipeline_fn: callable(query: str) -> {
            "answer": str, "contexts": List[str], "ground_truth": str,
            "predicted_label": Any, "true_label": Any
        }
        """
        self.pipeline_fn = pipeline_fn
        self.latency = LatencyTracker()
        self.writer = ResultsWriter(output_dir)

    def run(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        queries, answers, contexts, ground_truths = [], [], [], []
        preds, trues = [], []

        for item in dataset:
            start = time.perf_counter()
            out = self.pipeline_fn(item["query"])
            elapsed = time.perf_counter() - start
            self.latency.record(elapsed)

            queries.append(item["query"])
            answers.append(out["answer"])
            contexts.append(out["contexts"])
            ground_truths.append(out.get("ground_truth", ""))
            preds.append(out.get("predicted_label"))
            trues.append(item.get("true_label"))

        ragas_scores = run_ragas_eval(queries, answers, contexts, ground_truths)
        detection_scores = self._detection_metrics(preds, trues)
        latency_stats = self.latency.summary()

        report = {
            "ragas": ragas_scores,
            "detection": detection_scores,
            "latency": latency_stats,
        }
        self.writer.write(report)
        print(summarize_ragas(ragas_scores))
        return report

    @staticmethod
    def _detection_metrics(preds: List[Any], trues: List[Any]) -> Dict[str, float]:
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        valid = [(p, t) for p, t in zip(preds, trues) if p is not None and t is not None]
        if not valid:
            return {}
        p, t = zip(*valid)
        return {
            "accuracy": accuracy_score(t, p),
            "precision": precision_score(t, p, average="weighted", zero_division=0),
            "recall": recall_score(t, p, average="weighted", zero_division=0),
            "f1": f1_score(t, p, average="weighted", zero_division=0),
        }

"""
ragas.py
Wraps the RAGAS library to score the RAG pipeline on context precision,
context recall, faithfulness, and answer relevance.
"""

from typing import List, Dict, Any


def build_ragas_dataset(queries: List[str], answers: List[str],
                         contexts: List[List[str]], ground_truths: List[str]) -> "Dataset":
    from datasets import Dataset
    return Dataset.from_dict({
        "question": queries,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })


def run_ragas_eval(queries: List[str], answers: List[str],
                    contexts: List[List[str]], ground_truths: List[str]) -> Dict[str, float]:
    from ragas import evaluate
    from ragas.metrics import (
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    )

    dataset = build_ragas_dataset(queries, answers, contexts, ground_truths)
    result = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
    )
    return dict(result)


def summarize_ragas(scores: Dict[str, float]) -> str:
    lines = ["RAGAS Evaluation Summary", "-" * 30]
    for metric, value in scores.items():
        lines.append(f"{metric:20s}: {value:.3f}")
    return "\n".join(lines)

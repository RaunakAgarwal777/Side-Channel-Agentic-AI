"""
grader.py
Grades retrieved documents for relevance, and generated answers for
hallucination / grounding, matching the two decision diamonds in the
adaptive RAG workflow diagram.
"""

from typing import List, Dict, Any
from .prompts import RELEVANCE_GRADE_PROMPT, HALLUCINATION_GRADE_PROMPT, ANSWER_QUALITY_PROMPT


class Grader:
    def __init__(self, llm_client):
        self.llm = llm_client

    def grade_relevance(self, query: str, documents: List[Dict[str, Any]]) -> bool:
        """Returns True if at least one retrieved doc is relevant enough to proceed."""
        if not documents:
            return False
        joined = "\n---\n".join(d["text"][:500] for d in documents[:5])
        prompt = RELEVANCE_GRADE_PROMPT.format(query=query, documents=joined)
        verdict = self.llm.generate(prompt).strip().lower()
        return verdict.startswith("yes")

    def grade_hallucination(self, answer: str, documents: List[Dict[str, Any]]) -> bool:
        """Returns True if the answer is grounded in the retrieved context."""
        context = "\n---\n".join(d["text"][:500] for d in documents[:5])
        prompt = HALLUCINATION_GRADE_PROMPT.format(answer=answer, context=context)
        verdict = self.llm.generate(prompt).strip().lower()
        return verdict.startswith("yes")

    def grade_answer_quality(self, query: str, answer: str) -> bool:
        """Returns True if the answer fully addresses the original question."""
        prompt = ANSWER_QUALITY_PROMPT.format(query=query, answer=answer)
        verdict = self.llm.generate(prompt).strip().lower()
        return verdict.startswith("yes")

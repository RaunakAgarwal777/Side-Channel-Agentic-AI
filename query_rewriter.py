"""
query_rewriter.py
Rewrites/refines the user query when retrieved documents are graded
as low relevance, enabling the self-reflective retry loop.
"""

from typing import List
from .prompts import QUERY_REWRITE_PROMPT


class QueryRewriter:
    def __init__(self, llm_client):
        """
        llm_client: any object exposing .generate(prompt: str) -> str
        (see detection/predict.py or backend for a shared LLM client pattern)
        """
        self.llm = llm_client

    def rewrite(self, original_query: str, history: List[str] = None) -> str:
        history = history or []
        prompt = QUERY_REWRITE_PROMPT.format(
            query=original_query,
            history="\n".join(history) if history else "None",
        )
        rewritten = self.llm.generate(prompt).strip()
        return rewritten or original_query

    def expand(self, original_query: str, n_variants: int = 3) -> List[str]:
        """Generate multiple phrasings for broader recall on retry."""
        prompt = (
            f"Generate {n_variants} alternative phrasings of this security-analysis "
            f"query, one per line, no numbering:\n{original_query}"
        )
        raw = self.llm.generate(prompt)
        variants = [v.strip("-• ").strip() for v in raw.splitlines() if v.strip()]
        return variants[:n_variants] or [original_query]

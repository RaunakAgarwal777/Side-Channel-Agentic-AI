"""
retriever.py
Adaptive retrieval: embeds the query, hits the vector store, and returns
ranked, deduplicated chunks ready for grading.
"""

from typing import List, Dict, Any, Optional
from .embeddings import Embedder
from .vectorstore import VectorStore


class Retriever:
    def __init__(self, embedder: Optional[Embedder] = None, store: Optional[VectorStore] = None,
                 top_k: int = 5):
        self.embedder = embedder or Embedder()
        self.store = store or VectorStore()
        self.top_k = top_k

    def retrieve(self, query: str, filters: Optional[Dict[str, Any]] = None,
                 top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        query_vec = self.embedder.embed_query(query)
        hits = self.store.query(query_vec, top_k=top_k or self.top_k, filters=filters)
        return self._dedupe(hits)

    @staticmethod
    def _dedupe(hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen, unique = set(), []
        for h in hits:
            key = h["text"][:200]
            if key not in seen:
                seen.add(key)
                unique.append(h)
        return unique

    def hybrid_retrieve(self, query: str, keyword_boost_terms: List[str] = None,
                         top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Simple hybrid: dense retrieval + keyword re-rank boost."""
        hits = self.retrieve(query, top_k=top_k)
        if not keyword_boost_terms:
            return hits
        for h in hits:
            text_lower = h["text"].lower()
            boost = sum(1 for term in keyword_boost_terms if term.lower() in text_lower)
            h["score"] += 0.05 * boost
        return sorted(hits, key=lambda x: x["score"], reverse=True)

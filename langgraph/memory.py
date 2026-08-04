"""
memory.py - Short-term (conversation) and long-term (vector) memory helpers.
Matches Module 4 "Memory Layer" in the architecture: short-term memory +
vector database, kept intentionally to just two memory types.
"""

from typing import List, Dict
from collections import defaultdict


class ShortTermMemory:
    """In-process conversation memory, keyed by session id.
    Swap this for Redis in production if you need multi-instance persistence.
    """

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._store: Dict[str, List[dict]] = defaultdict(list)

    def add(self, session_id: str, role: str, content: str):
        self._store[session_id].append({"role": role, "content": content})
        self._store[session_id] = self._store[session_id][-self.max_turns:]

    def get(self, session_id: str) -> List[dict]:
        return self._store.get(session_id, [])

    def clear(self, session_id: str):
        self._store.pop(session_id, None)


class VectorMemory:
    """Thin wrapper around the vector store client (Qdrant/Chroma).
    Actual embedding + upsert logic lives in rag/vectorstore.py — this
    class just exposes a memory-shaped interface for LangGraph nodes.
    """

    def __init__(self, vectorstore_client=None):
        self.client = vectorstore_client  # injected, avoids circular import with rag/

    def remember(self, text: str, metadata: dict):
        if self.client is None:
            raise RuntimeError("VectorMemory has no client attached. Inject one from rag/vectorstore.py")
        self.client.upsert(text=text, metadata=metadata)

    def recall(self, query: str, top_k: int = 5):
        if self.client is None:
            raise RuntimeError("VectorMemory has no client attached. Inject one from rag/vectorstore.py")
        return self.client.search(query=query, top_k=top_k)


short_term_memory = ShortTermMemory()

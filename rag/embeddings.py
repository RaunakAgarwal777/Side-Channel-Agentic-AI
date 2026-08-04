"""
embeddings.py
Wraps the embedding model so it's swappable (local via Ollama, or sentence-transformers).
"""

import os
from typing import List

EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "sentence_transformers")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


class Embedder:
    def __init__(self, backend: str = EMBEDDING_BACKEND, model_name: str = EMBEDDING_MODEL):
        self.backend = backend
        self.model_name = model_name
        self._model = self._load_model()

    def _load_model(self):
        if self.backend == "ollama":
            import ollama
            return ollama  # uses ollama.embeddings(model=..., prompt=...)
        else:
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(self.model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if self.backend == "ollama":
            return [self._model.embeddings(model=self.model_name, prompt=t)["embedding"] for t in texts]
        return self._model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]

"""
vectorstore.py
Handles connection and operations against the vector database (Qdrant or Chroma).
"""

import os
from typing import List, Dict, Any, Optional

VECTOR_DB_BACKEND = os.getenv("VECTOR_DB_BACKEND", "chroma")  # "chroma" or "qdrant"
COLLECTION_NAME = os.getenv("VECTOR_COLLECTION", "sidechannel_knowledge")


class VectorStore:
    """
    Thin wrapper so the rest of the app doesn't care whether we're
    running Chroma locally or Qdrant.
    """

    def __init__(self, backend: str = VECTOR_DB_BACKEND, collection: str = COLLECTION_NAME):
        self.backend = backend
        self.collection = collection
        self.client = self._init_client()

    def _init_client(self):
        if self.backend == "qdrant":
            from qdrant_client import QdrantClient
            client = QdrantClient(
                url=os.getenv("QDRANT_URL", "http://localhost:6333")
            )
            return client
        else:
            import chromadb
            client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", "./chroma_db"))
            return client

    def get_or_create_collection(self):
        if self.backend == "chroma":
            return self.client.get_or_create_collection(self.collection)
        # Qdrant collections are created explicitly; see embeddings.py init step
        return self.collection

    def upsert(self, ids: List[str], embeddings: List[List[float]],
               documents: List[str], metadatas: List[Dict[str, Any]]):
        if self.backend == "chroma":
            col = self.get_or_create_collection()
            col.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
        else:
            from qdrant_client.models import PointStruct
            points = [
                PointStruct(id=i, vector=emb, payload={"text": doc, **meta})
                for i, emb, doc, meta in zip(ids, embeddings, documents, metadatas)
            ]
            self.client.upsert(collection_name=self.collection, points=points)

    def query(self, query_embedding: List[float], top_k: int = 5,
              filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.backend == "chroma":
            col = self.get_or_create_collection()
            results = col.query(query_embeddings=[query_embedding], n_results=top_k, where=filters)
            hits = []
            for doc, meta, dist, doc_id in zip(
                results["documents"][0], results["metadatas"][0],
                results["distances"][0], results["ids"][0]
            ):
                hits.append({"id": doc_id, "text": doc, "metadata": meta, "score": 1 - dist})
            return hits
        else:
            results = self.client.search(
                collection_name=self.collection,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=filters,
            )
            return [
                {"id": r.id, "text": r.payload.get("text"), "metadata": r.payload, "score": r.score}
                for r in results
            ]

    def delete(self, ids: List[str]):
        if self.backend == "chroma":
            self.get_or_create_collection().delete(ids=ids)
        else:
            self.client.delete(collection_name=self.collection, points_selector=ids)

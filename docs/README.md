# SideChannel Sentinel OS

Enterprise Adaptive Agentic RAG Framework for Side-Channel Threat Detection in UAVs.

## Modules
- `backend/` — API, auth, DB
- `langgraph/` — multi-agent orchestration
- `rag/` — adaptive RAG pipeline
- `detection/` — side-channel detection model
- `evaluation/` — RAGAS + benchmarking harness
- `frontend/` — dashboard
- `docs/` — architecture & paper notes

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # fill in QDRANT_URL / CHROMA_PATH, etc.
```

## Run
```bash
python backend/main.py
```

See `docs/architecture.md` for the full system design.

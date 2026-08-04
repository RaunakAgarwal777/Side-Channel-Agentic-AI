# SideChannel Sentinel OS — Architecture

**Enterprise Adaptive Agentic RAG Framework for Side-Channel Threat Detection in UAVs**

## Scope Decision

This project targets one flagship capability — side-channel attack detection —
built on a reusable multi-agent RAG framework. The architecture is designed so
future attack-detection modules (GPS spoofing, RF jamming, firmware attacks)
can be added later without redesign; only side-channel detection is implemented now.

## Module Map

| Module | Responsibility |
|---|---|
| `backend/` | API layer, auth, config, DB models |
| `langgraph/` | Multi-agent orchestration (Supervisor, Detector, Retriever, Reporter) |
| `rag/` | Adaptive RAG: vectorstore, embeddings, retriever, query rewriter, grader, prompts |
| `detection/` | Side-channel dataset, preprocessing, model, inference, metrics |
| `evaluation/` | RAGAS scoring, benchmarking harness, latency, results persistence |
| `frontend/` | Dashboard UI |
| `docs/` | This documentation |

## Agent Roles

1. **Supervisor** — routes requests, maintains shared state, decides workflow depth.
2. **Detector** — runs the side-channel detection model, classifies attack type, produces confidence scores.
3. **Retriever** — executes the adaptive RAG loop (rewrite → retrieve → grade → generate → verify).
4. **Reporter** — turns detector + retriever outputs into an explanation, mitigation, and incident report.

## Adaptive RAG Loop

```
Query → Rewrite (if needed) → Retrieve → Grade Relevance
  → [No: rewrite & retry, max 2-3 iterations]
  → [Yes] Generate → Hallucination Check
  → [No: retry generate] → [Yes] Answer Quality Check
  → [No: retry] → [Yes] Final Answer
```

## Memory

Two memory types only:
- **Short-term**: conversation/session state, held in LangGraph state.
- **Vector database**: long-term knowledge (attack signatures, MITRE data, papers, playbooks).

## Guardrails

Single `guardrails.py` handles input validation/prompt-injection detection,
content filtering, and output hallucination/policy checks.

## Tech Stack (free tier)

Python · LangGraph · Ollama (local LLM) · Qdrant/Chroma (vector DB) · FastAPI · RAGAS · LangSmith (free tier) · Streamlit/Next.js (UI)

## Deployment Tiers

- **Edge (UAV)**: lightweight feature extraction + light detector, local cache, offline mode.
- **Ground station/server**: full multi-agent system, RAG + reasoning, memory & database, reporting.
- **Cloud (optional)**: long-term storage, model registry, fleet analytics, sync.

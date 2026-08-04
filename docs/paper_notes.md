# Paper Notes

## Target Framing
Position this as a **framework**, not a finished multi-attack platform:
> "We implement one use case (side-channel attacks) on an architecture
> designed so future attack detectors can be added."
This supports a scalability discussion without needing to implement
GPS spoofing, RF jamming, or firmware-attack detectors.

## Implementation Scope (BCA research project, achievable)
- 4 agents: Supervisor, Detector, Retriever, Reporter
- 1 LangGraph with conditional routing + single adaptive RAG loop
- 1 side-channel dataset (e.g., ASCAD)
- 1 vector database (Qdrant or Chroma)
- 1 local LLM via Ollama
- 1 embedding model
- RAGAS for RAG evaluation
- Standard ML metrics (accuracy, precision, recall, F1, AUROC) for the detector
- One polished web dashboard

## Sections to Draft
1. Introduction & motivation (UAV side-channel threats)
2. Related work (side-channel detection, agentic RAG)
3. System architecture (see architecture.md)
4. Detection pipeline & dataset
5. Adaptive RAG design
6. Evaluation methodology (RAGAS + ML metrics + latency)
7. Results
8. Limitations & future work (extension to other attack types)

## Open Questions / TODO
- Confirm dataset licensing (ASCAD).
- Decide local LLM model size vs. latency budget.
- Define risk-scoring rubric for the Reporter agent.

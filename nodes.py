"""
nodes.py - Agent node implementations for the LangGraph workflow.
Each function takes the SentinelState, does its job, and returns
a partial state update. Wire real LLM/tool calls in where marked TODO.
"""

import time
from state import SentinelState


def _log(state: SentinelState, agent_name: str, summary: str, confidence: float = None):
    return {
        "agent_outputs": [{"agent_name": agent_name, "summary": summary, "confidence": confidence}]
    }


# ---------- Supervisor ----------
def supervisor_node(state: SentinelState) -> dict:
    """Classifies intent and decides which agent handles the query next."""
    query = state["user_query"].lower()

    if any(k in query for k in ["detect", "attack", "leakage", "spoofing", "anomaly"]):
        next_agent = "detector"
        risk = "high"
    elif any(k in query for k in ["explain", "why", "mitigation", "report"]):
        next_agent = "reporter"
        risk = "normal"
    else:
        next_agent = "retriever"
        risk = "low"

    return {
        "next_agent": next_agent,
        "risk_level": risk,
        **_log(state, "supervisor", f"Routed to {next_agent} (risk={risk})"),
    }


# ---------- Detector ----------
def detector_node(state: SentinelState) -> dict:
    """Runs side-channel detection. TODO: call detection/predict.py here."""
    # Placeholder logic — replace with real model inference call
    verdict = "unknown"
    confidence = 0.0
    attack_type = None

    return {
        "detection_verdict": verdict,
        "detection_confidence": confidence,
        "attack_type": attack_type,
        **_log(state, "detector", f"Verdict={verdict}", confidence),
    }


# ---------- Retriever (adaptive RAG loop) ----------
def query_rewrite_node(state: SentinelState) -> dict:
    rewritten = state.get("rewritten_query") or state["user_query"]
    return {
        "rewritten_query": rewritten,
        **_log(state, "retriever.rewrite", f"Rewritten query: {rewritten}"),
    }


def retrieve_node(state: SentinelState) -> dict:
    """TODO: call rag/retriever.py to hit the vector store."""
    query = state.get("rewritten_query") or state["user_query"]
    docs = []  # placeholder for retrieved chunks
    return {
        "retrieved_docs": docs,
        **_log(state, "retriever.retrieve", f"Retrieved {len(docs)} docs for: {query}"),
    }


def grade_node(state: SentinelState) -> dict:
    """TODO: call rag/grader.py (LLM-as-judge relevance grading)."""
    relevant = len(state.get("retrieved_docs", [])) > 0
    return {
        "grade_relevant": relevant,
        "retrieval_attempts": state.get("retrieval_attempts", 0) + 1,
        **_log(state, "retriever.grade", f"Relevant={relevant}"),
    }


def generate_node(state: SentinelState) -> dict:
    """TODO: call the LLM to draft an answer from retrieved context."""
    generation = f"[draft answer for: {state['user_query']}]"
    return {
        "generation": generation,
        **_log(state, "generator", "Draft answer generated"),
    }


def hallucination_check_node(state: SentinelState) -> dict:
    """TODO: verify generation is grounded in retrieved_docs."""
    ok = True
    return {
        "hallucination_ok": ok,
        **_log(state, "verifier.hallucination", f"Grounded={ok}"),
    }


def answer_quality_node(state: SentinelState) -> dict:
    """TODO: verify generation actually answers the user query."""
    ok = True
    return {
        "answer_quality_ok": ok,
        **_log(state, "verifier.quality", f"AnswersQuery={ok}"),
    }


# ---------- Reporter ----------
def reporter_node(state: SentinelState) -> dict:
    """Produces the final explanation, mitigation, and report."""
    verdict = state.get("detection_verdict", "unknown")
    generation = state.get("generation", "")
    final = generation or f"No detection run yet. Verdict: {verdict}."

    return {
        "final_answer": final,
        "explanation": final,
        **_log(state, "reporter", "Final report composed"),
    }

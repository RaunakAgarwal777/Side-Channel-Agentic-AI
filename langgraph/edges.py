"""
edges.py - Conditional routing logic between nodes.
These functions inspect state and return the name of the next node,
implementing the diamond decision points in the architecture diagram
(Supervisor routing, Grade -> Generate, Hallucination Check, Answer Quality Check).
"""

from state import SentinelState

MAX_RETRIEVAL_ATTEMPTS = 3


def route_from_supervisor(state: SentinelState) -> str:
    """Supervisor -> Detector / Retriever / Reporter."""
    return state.get("next_agent", "retriever")


def route_after_grade(state: SentinelState) -> str:
    """Grade Relevance: Yes -> generate, No -> rewrite & retry (bounded)."""
    if state.get("grade_relevant"):
        return "generate"
    if state.get("retrieval_attempts", 0) >= MAX_RETRIEVAL_ATTEMPTS:
        # give up gracefully rather than looping forever
        return "generate"
    return "rewrite"


def route_after_hallucination_check(state: SentinelState) -> str:
    """Hallucination Check: Yes (grounded) -> answer quality check, No -> retry retrieval."""
    if state.get("hallucination_ok"):
        return "answer_quality"
    if state.get("retrieval_attempts", 0) >= MAX_RETRIEVAL_ATTEMPTS:
        return "answer_quality"  # avoid infinite loop, flag downstream
    return "rewrite"


def route_after_answer_quality(state: SentinelState) -> str:
    """Answer Quality Check: Yes -> final answer / reporter, No -> rewrite & retry."""
    if state.get("answer_quality_ok"):
        return "reporter"
    if state.get("retrieval_attempts", 0) >= MAX_RETRIEVAL_ATTEMPTS:
        return "reporter"
    return "rewrite"

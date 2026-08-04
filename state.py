"""
state.py - Shared state schema for the LangGraph multi-agent workflow.
This is the "Shared State & Memory" object passed between all agents
(Supervisor, Detector, Retriever, Reporter) in the architecture diagram.
"""

from typing import TypedDict, List, Optional, Literal
from typing_extensions import Annotated
import operator


class AgentOutput(TypedDict):
    agent_name: str
    summary: str
    confidence: Optional[float]


class SentinelState(TypedDict):
    # Conversation
    user_query: str
    conversation_history: Annotated[List[dict], operator.add]

    # Routing
    risk_level: Optional[Literal["low", "normal", "high"]]
    next_agent: Optional[str]

    # RAG loop
    retrieved_docs: List[str]
    rewritten_query: Optional[str]
    grade_relevant: Optional[bool]
    generation: Optional[str]
    hallucination_ok: Optional[bool]
    answer_quality_ok: Optional[bool]
    retrieval_attempts: int

    # Detection
    detection_verdict: Optional[Literal["yes", "no", "unknown"]]
    attack_type: Optional[str]
    detection_confidence: Optional[float]
    risk_score: Optional[float]

    # Outputs
    explanation: Optional[str]
    evidence: List[str]
    final_answer: Optional[str]

    # Trace
    agent_outputs: Annotated[List[AgentOutput], operator.add]
    error: Optional[str]


def new_state(user_query: str) -> SentinelState:
    """Factory for a fresh state at the start of a run."""
    return SentinelState(
        user_query=user_query,
        conversation_history=[],
        risk_level=None,
        next_agent=None,
        retrieved_docs=[],
        rewritten_query=None,
        grade_relevant=None,
        generation=None,
        hallucination_ok=None,
        answer_quality_ok=None,
        retrieval_attempts=0,
        detection_verdict=None,
        attack_type=None,
        detection_confidence=None,
        risk_score=None,
        explanation=None,
        evidence=[],
        final_answer=None,
        agent_outputs=[],
        error=None,
    )

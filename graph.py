"""
graph.py - Assembles the LangGraph StateGraph wiring together supervisor,
detector, retriever (adaptive RAG loop), and reporter agents.
Run directly for a quick smoke test: python graph.py
"""

from langgraph.graph import StateGraph, END

from state import SentinelState, new_state
from nodes import (
    supervisor_node,
    detector_node,
    query_rewrite_node,
    retrieve_node,
    grade_node,
    generate_node,
    hallucination_check_node,
    answer_quality_node,
    reporter_node,
)
from edges import (
    route_from_supervisor,
    route_after_grade,
    route_after_hallucination_check,
    route_after_answer_quality,
)


def build_graph():
    graph = StateGraph(SentinelState)

    # Register nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("detector", detector_node)
    graph.add_node("rewrite", query_rewrite_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("generate", generate_node)
    graph.add_node("hallucination_check", hallucination_check_node)
    graph.add_node("answer_quality", answer_quality_node)
    graph.add_node("reporter", reporter_node)

    graph.set_entry_point("supervisor")

    # Supervisor routes to detector, retriever entrypoint (rewrite), or straight to reporter
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {"detector": "detector", "retriever": "rewrite", "reporter": "reporter"},
    )

    # Detector flows into reporter for explanation
    graph.add_edge("detector", "reporter")

    # Adaptive RAG loop
    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("retrieve", "grade")
    graph.add_conditional_edges(
        "grade", route_after_grade, {"generate": "generate", "rewrite": "rewrite"}
    )
    graph.add_edge("generate", "hallucination_check")
    graph.add_conditional_edges(
        "hallucination_check",
        route_after_hallucination_check,
        {"answer_quality": "answer_quality", "rewrite": "rewrite"},
    )
    graph.add_conditional_edges(
        "answer_quality",
        route_after_answer_quality,
        {"reporter": "reporter", "rewrite": "rewrite"},
    )

    graph.add_edge("reporter", END)

    return graph.compile()


sentinel_graph = build_graph()


if __name__ == "__main__":
    result = sentinel_graph.invoke(new_state("Is there evidence of side-channel leakage in this trace?"))
    print("Final answer:", result["final_answer"])
    print("\n--- Agent trace ---")
    for step in result["agent_outputs"]:
        print(f"[{step['agent_name']}] {step['summary']}")

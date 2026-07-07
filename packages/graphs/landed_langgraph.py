from langgraph.graph import END, START, StateGraph

from packages.graphs.state import LandedGraphState
from packages.graphs.nodes import (
    knowledge_node,
    orchestrator_node,
    recommendation_node,
)


def build_landed_graph():
    graph = StateGraph(LandedGraphState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("recommendation", recommendation_node)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", "knowledge")
    graph.add_edge("knowledge", "recommendation")
    graph.add_edge("recommendation", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_landed_graph()

    result = app.invoke(
        {
            "session_id": "local-session-001",
            "user_id": "luis-local",
            "user_message": "Qué audífonos recomiendas para música clásica y gaming competitivo?",
            "messages": [],
            "country": "Colombia",
        }
    )

    print(result.get("final_answer", "No final answer produced."))

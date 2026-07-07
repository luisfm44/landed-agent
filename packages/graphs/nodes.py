from typing import Any

from packages.graphs.state import LandedGraphState, require_user_message
from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge


def graph_orchestrator_node(state: LandedGraphState) -> dict[str, Any]:
    """Initialize graph state, routing metadata, and short-term memory.

    This node coordinates workflow and session state. It is not the ADK
    business orchestrator (`landed_orchestrator` root_agent).
    """
    user_message = require_user_message(state)

    return {
        "current_intent": "audio_recommendation",
        "product_type": "headphones",
        "country": state.get("country", "Colombia"),
        "constraints": {
            "needs_grounding": True,
            "domain": "audio",
        },
        "orchestrator_output": {
            "route": "knowledge_then_recommendation",
            "reason": "User is asking for audio/product guidance",
        },
        "messages": state.get("messages", [])
        + [{"role": "user", "content": user_message}],
    }


def knowledge_node(state: LandedGraphState) -> dict[str, Any]:
    query = require_user_message(state)

    tool_response = retrieve_knowledge(query=query)

    data = tool_response.get("data", {}) if isinstance(tool_response, dict) else {}

    return {
        "knowledge_result": tool_response,
        "grounded": bool(data.get("grounded", False)),
        "grounded_answer": data.get("grounded_answer"),
        "sources": data.get("sources", []),
    }


def recommendation_node(state: LandedGraphState) -> dict[str, Any]:
    grounded = state.get("grounded", False)
    grounded_answer = state.get("grounded_answer")

    if not grounded or not grounded_answer:
        final_answer = (
            "No tengo suficiente evidencia local para darte una recomendación confiable. "
            "Necesito más documentos en la base de conocimiento de Landed."
        )
    else:
        final_answer = f"""
Recomendación basada en grounding local:

{grounded_answer}
""".strip()

    return {
        "recommendation_output": {
            "used_grounding": grounded,
            "sources_count": len(state.get("sources", [])),
        },
        "final_answer": final_answer,
        "messages": state.get("messages", [])
        + [{"role": "assistant", "content": final_answer}],
    }
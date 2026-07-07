from typing import Any

from packages.graphs.adk_runner import run_adk_orchestrator
from packages.graphs.state import LandedGraphState, require_user_message
from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge


def graph_orchestrator_node(state: LandedGraphState) -> dict[str, Any]:
    """Initialize graph state, routing metadata, and short-term memory.

    This node coordinates workflow and session state. It is not the ADK
    business orchestrator (`landed_orchestrator` root_agent).
    """
    user_message = require_user_message(state)

    return {
        "current_intent": "commerce_assistance",
        "country": state.get("country", "Colombia"),
        "constraints": {
            "needs_grounding": True,
            "domain": "audio",
        },
        "orchestrator_output": {
            "route": "adk_orchestrator",
            "reason": "Delegate business orchestration to ADK specialists",
        },
        "messages": state.get("messages", [])
        + [{"role": "user", "content": user_message}],
    }


def adk_orchestrator_node(state: LandedGraphState) -> dict[str, Any]:
    """Run ADK `landed_orchestrator`, which delegates to specialist agents and tools."""
    user_message = require_user_message(state)
    session_id = state.get("session_id") or "default-session"
    user_id = state.get("user_id") or "default-user"

    adk_result = run_adk_orchestrator(
        user_id=user_id,
        session_id=session_id,
        user_message=user_message,
    )
    final_answer = adk_result.get("final_answer") or (
        "No pude generar una respuesta con el orquestador ADK."
    )

    return {
        "orchestrator_output": adk_result,
        "final_answer": final_answer,
        "messages": state.get("messages", [])
        + [{"role": "assistant", "content": final_answer}],
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
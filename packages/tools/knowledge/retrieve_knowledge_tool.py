from packages.rag.grounding_service import answer_with_local_grounding
from packages.shared.logging import new_trace_id
from packages.shared.schemas.agent_response_schema import ToolResponse
from packages.tools.knowledge.rag_search_tool import search_knowledge


def retrieve_knowledge(query: str, limit: int = 4) -> dict:
    """Agent-facing knowledge tool with retrieval and local grounding."""
    trace_id = new_trace_id()
    synthesis_error = None

    try:
        retrieval = search_knowledge(query=query, limit=limit)
        ok = True
        error = None
    except Exception as exc:
        retrieval = {
            "query": query,
            "sources": [],
            "grounded": False,
            "backend": "unavailable",
        }
        ok = False
        error = str(exc)

    try:
        grounded_result = answer_with_local_grounding(
            question=query,
            limit=limit,
            retrieval=retrieval,
        )
    except Exception as exc:
        synthesis_error = str(exc)
        grounded_result = {
            "grounded": bool(retrieval.get("grounded")),
            "answer": None,
            "sources": retrieval.get("sources", []),
            "synthesis_available": False,
            "model": None,
        }

    backend = retrieval.get("backend", "unknown")
    has_sources = bool(retrieval.get("grounded"))

    response = ToolResponse(
        ok=ok,
        trace_id=trace_id,
        source=f"landed_rag:{backend}",
        data={
            "tool": "retrieve_knowledge",
            "query": retrieval.get("query", query),
            "sources": retrieval.get("sources", []),
            "grounded": has_sources,
            "backend": backend,
            "grounded_answer": grounded_result.get("answer"),
            "grounding_model": grounded_result.get("model"),
            "synthesis_available": grounded_result.get("synthesis_available", False),
            "message": (
                f"Knowledge retrieved using {backend}."
                if has_sources
                else "No relevant knowledge found."
            ),
            "synthesis_error": synthesis_error,
        },
        error=error,
    )

    return response.model_dump()

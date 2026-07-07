from packages.shared.logging import new_trace_id
from packages.shared.schemas.agent_response_schema import ToolResponse
from packages.tools.knowledge.rag_search_tool import search_knowledge


def retrieve_knowledge(query: str) -> dict:
    """Agent-facing knowledge tool with normalized ToolResponse envelope."""
    trace_id = new_trace_id()

    try:
        result = search_knowledge(query=query, limit=4)
        ok = True
        error = None
    except Exception as exc:
        result = {
            "query": query,
            "sources": [],
            "grounded": False,
            "backend": "unavailable",
        }
        ok = False
        error = str(exc)

    backend = result.get("backend", "unknown")
    grounded = bool(result.get("grounded"))

    response = ToolResponse(
        ok=ok,
        trace_id=trace_id,
        source=f"landed_rag:{backend}",
        data={
            "tool": "retrieve_knowledge",
            "query": result.get("query", query),
            "sources": result.get("sources", []),
            "grounded": grounded,
            "backend": backend,
            "message": (
                f"Knowledge retrieved using {backend}."
                if grounded
                else "No relevant knowledge found."
            ),
        },
        error=error,
    )

    return response.model_dump()

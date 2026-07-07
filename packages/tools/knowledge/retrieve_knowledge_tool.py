from packages.rag.retriever import retrieve_local_knowledge
from packages.shared.logging import new_trace_id
from packages.shared.schemas.agent_response_schema import ToolResponse


def retrieve_knowledge(query: str) -> dict:
    """Retrieve grounded product knowledge from the local Landed RAG corpus.

    This implementation is local and does not call an LLM.
    """
    trace_id = new_trace_id()
    matches = retrieve_local_knowledge(query=query, limit=3)

    response = ToolResponse(
        ok=True,
        trace_id=trace_id,
        source="local_landed_rag",
        data={
            "tool": "retrieve_knowledge",
            "query": query,
            "matches": matches,
            "grounded": bool(matches),
            "message": (
                "Knowledge retrieved from local Landed corpus."
                if matches
                else "No relevant local knowledge found."
            ),
        },
        error=None,
    )

    return response.model_dump()
from packages.shared.schemas.agent_response_schema import ToolResponse
from packages.shared.logging import new_trace_id


def retrieve_knowledge(query: str) -> dict:
    """Retrieve product knowledge from the local RAG corpus.

    The RAG pipeline is not wired yet, so this returns an explicit empty result.
    """
    trace_id = new_trace_id()

    response = ToolResponse(
        ok=True,
        trace_id=trace_id,
        source="local_rag_placeholder",
        data={
            "tool": "retrieve_knowledge",
            "query": query,
            "results": [],
            "message": "RAG knowledge retrieval is not configured yet.",
        },
        error=None,
    )

    return response.model_dump()
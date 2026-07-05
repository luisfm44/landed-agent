from packages.shared.schemas.agent_response_schema import ToolResponse


def retrieve_knowledge(query: str, trace_id: str) -> ToolResponse:
    """Retrieve product knowledge from the local RAG corpus.

    The RAG pipeline is not wired yet, so this returns an explicit empty result.
    """
    return ToolResponse(
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

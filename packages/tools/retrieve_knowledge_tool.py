def retrieve_knowledge(query: str) -> dict:
    """Retrieve product knowledge from the local RAG corpus.

    The RAG pipeline is not wired yet, so this returns an explicit empty result.
    """
    return {
        "query": query,
        "results": [],
        "message": "RAG knowledge retrieval is not configured yet.",
    }

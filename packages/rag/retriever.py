from typing import Any

from packages.tools.knowledge.vector_store import get_collection


def _first_query_row(results: Any, key: str) -> list[Any]:
    """Safely read the first result row from a Chroma query response."""
    values = results.get(key)
    if not values:
        return []

    first_row = values[0]
    return first_row if first_row is not None else []


def retrieve_context(
    query: str,
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Retrieve grounded context using ChromaDB + Ollama embeddings.

    This is the semantic retriever for the Landed RAG layer.
    It does not depend on agents directly.
    """
    if not query or not query.strip():
        return []

    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=limit,
        include=["documents", "metadatas", "distances"],
    )

    documents = _first_query_row(results, "documents")
    metadatas = _first_query_row(results, "metadatas")
    distances = _first_query_row(results, "distances")

    retrieved: list[dict[str, Any]] = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append(
            {
                "content": document,
                "metadata": metadata or {},
                "distance": float(distance) if distance is not None else None,
            }
        )

    return retrieved


def retrieve_knowledge(
    query: str,
    limit: int = 4,
) -> dict[str, Any]:
    """Stable contract for tools and agents.

    Agents should call this contract indirectly through tools,
    not ChromaDB directly.
    """
    sources = retrieve_context(query=query, limit=limit)

    return {
        "query": query,
        "sources": sources,
        "grounded": bool(sources),
    }


if __name__ == "__main__":
    result = retrieve_knowledge(
        "What headphones are good for classical music and competitive gaming?"
    )

    for index, source in enumerate(result["sources"], start=1):
        print(f"\n--- Source {index} ---")
        print("Metadata:", source["metadata"])
        print("Distance:", source["distance"])
        print(str(source["content"])[:500])

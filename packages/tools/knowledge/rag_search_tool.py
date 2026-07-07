from typing import Any

from packages.rag.local_retriever import retrieve_local_knowledge
from packages.rag.retriever import retrieve_knowledge as retrieve_semantic_knowledge


def _normalize_local_matches(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "content": f"{match.get('title', '')}\n{match.get('content', '')}".strip(),
            "metadata": {
                "source": match.get("source"),
                "title": match.get("title"),
            },
            "distance": None,
            "score": match.get("score"),
            "matched_terms": match.get("matched_terms"),
        }
        for match in matches
    ]


def search_knowledge(
    query: str,
    limit: int = 4,
) -> dict[str, Any]:
    """Knowledge search used by Landed tools and agents.

    Current backend:
    - ChromaDB
    - Ollama embeddings
    - nomic-embed-text

    Fallback backend:
    - local lexical search over markdown corpora

    Future backend:
    - Vertex AI Vector Search
    - Gemini embeddings
    """
    try:
        semantic_result = retrieve_semantic_knowledge(query=query, limit=limit)
        if semantic_result.get("grounded"):
            return {
                **semantic_result,
                "backend": "chroma_ollama",
            }
    except Exception:
        pass

    local_matches = retrieve_local_knowledge(query=query, limit=limit)
    sources = _normalize_local_matches(local_matches)

    return {
        "query": query,
        "sources": sources,
        "grounded": bool(sources),
        "backend": "local_lexical",
    }

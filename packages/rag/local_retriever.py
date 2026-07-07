from typing import Any

from packages.knowledge_base.loader import load_knowledge_sections

DEFAULT_MIN_LEXICAL_SCORE = 0.35

STOP_WORDS = {
    "about",
    "and",
    "are",
    "best",
    "can",
    "como",
    "con",
    "cual",
    "de",
    "del",
    "el",
    "en",
    "for",
    "has",
    "how",
    "is",
    "la",
    "las",
    "los",
    "not",
    "para",
    "por",
    "que",
    "the",
    "this",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
    "you",
}


def _tokenize(text: str) -> set[str]:
    """Tokenize text into normalized lowercase terms."""
    return {
        token.strip(".,:;!?()[]{}\"'").lower()
        for token in text.split()
        if len(token.strip(".,:;!?()[]{}\"'")) > 2
        and token.strip(".,:;!?()[]{}\"'").lower() not in STOP_WORDS
    }


def retrieve_local_knowledge(
    query: str,
    limit: int = 3,
    min_score: float = DEFAULT_MIN_LEXICAL_SCORE,
) -> list[dict[str, Any]]:
    """Retrieve grounded local knowledge using lexical overlap.

    Uses the same markdown corpus as semantic ingest in packages/knowledge_base.
    """
    query_tokens = _tokenize(query)

    if not query_tokens:
        return []

    documents = load_knowledge_sections()
    scored: list[dict[str, Any]] = []

    for document in documents:
        searchable_text = f"{document['title']} {document['content']}"
        document_tokens = _tokenize(searchable_text)

        overlap = query_tokens.intersection(document_tokens)
        score = len(overlap) / max(len(query_tokens), 1)

        if score >= min_score:
            scored.append(
                {
                    "title": document["title"],
                    "content": document["content"],
                    "source": document["source"],
                    "score": round(score, 3),
                    "matched_terms": sorted(overlap),
                }
            )

    return sorted(
        scored,
        key=lambda item: item["score"],
        reverse=True,
    )[:limit]

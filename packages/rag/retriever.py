from pathlib import Path
from typing import Any


RAG_ROOT = Path(__file__).resolve().parent

SEARCH_DIRECTORIES = [
    RAG_ROOT / "buying_guides",
    RAG_ROOT / "product_knowledge",
    RAG_ROOT / "reviews",
]


def _read_text_file(file_path: Path) -> str:
    """Read text files defensively across common encodings."""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return file_path.read_text(encoding="utf-8", errors="replace")


def _tokenize(text: str) -> set[str]:
    """Tokenize text into normalized lowercase terms."""
    return {
        token.strip(".,:;!?()[]{}\"'").lower()
        for token in text.split()
        if len(token.strip(".,:;!?()[]{}\"'")) > 2
    }


def _split_markdown_sections(content: str) -> list[tuple[str, str]]:
    """Split markdown content into sections using headings.

    Supports:
    - # Main title
    - ## Section title

    Each section is returned as:
    (section_title, section_content)
    """
    sections: list[tuple[str, str]] = []
    current_title = "General"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append(
                    (
                        current_title,
                        "\n".join(current_lines).strip(),
                    )
                )

            current_title = line.replace("## ", "").strip()
            current_lines = []

        elif line.startswith("# "):
            current_title = line.replace("# ", "").strip()

        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            (
                current_title,
                "\n".join(current_lines).strip(),
            )
        )

    return [
        (title, body)
        for title, body in sections
        if body
    ]


def _load_documents() -> list[dict[str, str]]:
    """Load markdown documents from the local RAG directories."""
    documents: list[dict[str, str]] = []

    for directory in SEARCH_DIRECTORIES:
        if not directory.exists():
            continue

        for file_path in directory.glob("*.md"):
            content = _read_text_file(file_path)
            sections = _split_markdown_sections(content)

            for section_title, section_content in sections:
                documents.append(
                    {
                        "source": str(file_path.relative_to(RAG_ROOT)),
                        "title": section_title,
                        "content": section_content,
                    }
                )

    return documents


def retrieve_local_knowledge(
    query: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Retrieve grounded local knowledge using lexical overlap.

    This is a lightweight local grounding layer.

    It searches markdown files in:
    - buying_guides
    - product_knowledge
    - reviews

    Later this can be replaced with embeddings/vector search without changing
    the retrieve_knowledge tool contract.
    """
    query_tokens = _tokenize(query)

    if not query_tokens:
        return []

    documents = _load_documents()
    scored: list[dict[str, Any]] = []

    for document in documents:
        searchable_text = f"{document['title']} {document['content']}"
        document_tokens = _tokenize(searchable_text)

        overlap = query_tokens.intersection(document_tokens)
        score = len(overlap) / max(len(query_tokens), 1)

        if score > 0:
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
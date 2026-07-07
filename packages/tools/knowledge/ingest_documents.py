from pathlib import Path
from typing import TypedDict

from packages.knowledge_base.loader import KNOWLEDGE_BASE_DIR, load_knowledge_sections
from packages.tools.knowledge.vector_store import get_collection


class KnowledgeChunk(TypedDict):
    id: str
    document: str
    metadata: dict[str, str]


def _load_markdown_chunks(
    knowledge_dir: Path | None = None,
) -> list[KnowledgeChunk]:
    base_dir = knowledge_dir or KNOWLEDGE_BASE_DIR
    chunks: list[KnowledgeChunk] = []

    for section in load_knowledge_sections(base_dir):
        chunk_id = f"{section['source']}:{section['title']}".replace(" ", "_")
        chunks.append(
            {
                "id": chunk_id,
                "document": f"{section['title']}\n{section['content']}",
                "metadata": {
                    "source": section["source"],
                    "title": section["title"],
                },
            }
        )

    return chunks


def ingest_documents(knowledge_dir: Path | str | None = None) -> int:
    """Load markdown knowledge files and upsert them into the Chroma collection."""
    target_dir = Path(knowledge_dir) if knowledge_dir else KNOWLEDGE_BASE_DIR
    chunks = _load_markdown_chunks(target_dir)

    if not chunks:
        return 0

    collection = get_collection()
    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["document"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
    )
    return len(chunks)


if __name__ == "__main__":
    ingested = ingest_documents()
    print(f"Ingested {ingested} knowledge chunks into Chroma.")

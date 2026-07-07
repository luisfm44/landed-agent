from pathlib import Path
from typing import TypedDict

from packages.rag.retriever import _read_text_file, _split_markdown_sections
from packages.tools.knowledge.vector_store import KNOWLEDGE_BASE_DIR, get_collection


class KnowledgeChunk(TypedDict):
    id: str
    document: str
    metadata: dict[str, str]


def _load_markdown_chunks(
    knowledge_dir: Path | None = None,
) -> list[KnowledgeChunk]:
    base_dir = knowledge_dir or KNOWLEDGE_BASE_DIR
    chunks: list[KnowledgeChunk] = []

    if not base_dir.exists():
        return chunks

    for file_path in sorted(base_dir.rglob("*.md")):
        if file_path.name.startswith("._"):
            continue

        content = _read_text_file(file_path)
        rel_source = str(file_path.relative_to(base_dir.parent))

        for title, body in _split_markdown_sections(content):
            chunk_id = f"{rel_source}:{title}".replace(" ", "_")
            chunks.append(
                {
                    "id": chunk_id,
                    "document": f"{title}\n{body}",
                    "metadata": {
                        "source": rel_source,
                        "title": title,
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

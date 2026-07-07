from pathlib import Path
from typing import cast

import chromadb
from chromadb.api.client import Client
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PACKAGE_ROOT / "knowledge_base"
CHROMA_PERSIST_DIR = PACKAGE_ROOT / "rag" / "embeddings" / "chroma"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_COLLECTION = "landed_knowledge"


def get_embedding_function(
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> OllamaEmbeddingFunction:
    return OllamaEmbeddingFunction(model_name=model)


def get_chroma_client(
    persist_directory: Path | str | None = None,
) -> Client:
    persist_path = Path(persist_directory or CHROMA_PERSIST_DIR)
    persist_path.mkdir(parents=True, exist_ok=True)
    return cast(Client, chromadb.PersistentClient(path=str(persist_path)))


def get_collection(
    collection_name: str = DEFAULT_COLLECTION,
    persist_directory: Path | str | None = None,
) -> chromadb.Collection:
    client = get_chroma_client(persist_directory)
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=cast(EmbeddingFunction, get_embedding_function()),
    )

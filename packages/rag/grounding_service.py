from typing import Any

from ollama import Client

from packages.rag.prompts import LOCAL_GROUNDING_SYSTEM_PROMPT, NO_EVIDENCE_ANSWER
from packages.shared.config import OLLAMA_GROUNDING_MODEL, OLLAMA_HOST
from packages.tools.knowledge.rag_search_tool import search_knowledge

MAX_CONTEXT_CHARS = 6000


def _build_grounded_context(sources: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    total_chars = 0

    for index, source in enumerate(sources, start=1):
        metadata = source.get("metadata") or {}
        content = source.get("content", "")
        distance = source.get("distance")
        score = source.get("score")

        source_name = metadata.get("source") or metadata.get("title") or "unknown"
        title = metadata.get("title") or "Untitled"

        block = f"""
[Source {index}]
Source: {source_name}
Title: {title}
Distance: {distance}
Score: {score}
Content:
{content}
"""

        if total_chars + len(block) > MAX_CONTEXT_CHARS:
            break

        blocks.append(block)
        total_chars += len(block)

    return "\n".join(blocks)


def _call_ollama(system_prompt: str, user_prompt: str) -> str:
    client = Client(host=OLLAMA_HOST)
    response = client.chat(
        model=OLLAMA_GROUNDING_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"]


def _build_user_prompt(question: str, context: str) -> str:
    return f"""
User question:
{question}

Retrieved local context:
{context}

Instructions:
Answer the user question using ONLY the retrieved local context.

Required output:
1. Direct answer
2. Reasoning based on the provided sources
3. Missing information, if any
4. Sources used
"""


def answer_with_local_grounding(
    question: str,
    limit: int = 4,
    retrieval: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Retrieve local knowledge and synthesize a constrained answer."""
    if not question or not question.strip():
        raise ValueError("question cannot be empty")

    search_result = retrieval or search_knowledge(query=question, limit=limit)
    sources = search_result.get("sources", [])
    backend = search_result.get("backend", "unknown")
    has_evidence = bool(search_result.get("grounded") and sources)

    if not has_evidence:
        return {
            "provider": "ollama",
            "model": OLLAMA_GROUNDING_MODEL,
            "backend": backend,
            "grounded": False,
            "question": question,
            "answer": NO_EVIDENCE_ANSWER,
            "sources": sources,
            "synthesis_available": False,
        }

    context = _build_grounded_context(sources)
    answer = _call_ollama(
        system_prompt=LOCAL_GROUNDING_SYSTEM_PROMPT,
        user_prompt=_build_user_prompt(question, context),
    )

    return {
        "provider": "ollama",
        "model": OLLAMA_GROUNDING_MODEL,
        "backend": backend,
        "grounded": True,
        "question": question,
        "answer": answer,
        "sources": sources,
        "synthesis_available": True,
    }


if __name__ == "__main__":
    result = answer_with_local_grounding(
        "What headphones are good for classical music and competitive gaming?"
    )

    print(result["answer"])

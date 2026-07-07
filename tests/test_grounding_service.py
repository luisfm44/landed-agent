from packages.rag.grounding_service import answer_with_local_grounding


def test_grounding_returns_no_evidence_for_unknown_domain():
    result = answer_with_local_grounding(
        "zzzz qqqq unknown nonexistent product category"
    )

    assert result["grounded"] is False
    assert result["synthesis_available"] is False
    assert "evidencia local" in result["answer"].lower()
    assert result["sources"] == []


def test_grounding_accepts_preloaded_retrieval_without_evidence():
    result = answer_with_local_grounding(
        question="random unknown topic",
        retrieval={
            "query": "random unknown topic",
            "sources": [],
            "grounded": False,
            "backend": "local_lexical",
        },
    )

    assert result["grounded"] is False
    assert result["backend"] == "local_lexical"

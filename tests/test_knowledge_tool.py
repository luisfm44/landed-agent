from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge


def test_retrieve_knowledge_returns_grounded_matches():
    result = retrieve_knowledge("Beyerdynamic DT 770 Pro closed back mixing")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"].startswith("landed_rag:")
    assert result["data"] is not None
    assert result["data"]["tool"] == "retrieve_knowledge"
    assert result["data"]["grounded"] is True
    assert len(result["data"]["sources"]) > 0
    assert result["error"] is None


def test_retrieve_knowledge_handles_unknown_query():
    result = retrieve_knowledge("zzzz qqqq unknown nonexistent product")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"].startswith("landed_rag:")
    assert result["data"] is not None
    assert result["data"]["tool"] == "retrieve_knowledge"
    assert result["data"]["grounded"] is False
    assert result["data"]["sources"] == []
    assert result["error"] is None

from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge


def test_retrieve_knowledge_returns_grounded_matches():
    result = retrieve_knowledge("Beyerdynamic DT 770 Pro closed back mixing")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "local_landed_rag"
    assert result["data"] is not None
    assert result["data"]["tool"] == "retrieve_knowledge"
    assert result["data"]["grounded"] is True
    assert len(result["data"]["matches"]) > 0
    assert result["error"] is None


def test_retrieve_knowledge_handles_unknown_query():
    result = retrieve_knowledge("zzzz qqqq unknown nonexistent product")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "local_landed_rag"
    assert result["data"] is not None
    assert result["data"]["tool"] == "retrieve_knowledge"
    assert result["error"] is None
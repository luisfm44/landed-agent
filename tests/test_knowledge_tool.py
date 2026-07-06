from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge


def test_retrieve_knowledge_returns_tool_response():
    result = retrieve_knowledge("dt 770 pro")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "local_rag_placeholder"
    assert result["data"] is not None
    assert result["data"]["tool"] == "retrieve_knowledge"
    assert result["error"] is None
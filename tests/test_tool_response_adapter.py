from packages.tools.tool_response_adapter import to_tool_response


def test_to_tool_response_success():
    raw_response = {
        "ok": True,
        "data": {
            "products": [
                {"name": "Beyerdynamic DT 770 Pro"}
            ]
        },
        "tool": "search_products",
    }

    result = to_tool_response(
        raw_response=raw_response,
        trace_id="trace-test",
        source="landed_backend:/search",
    )

    assert result.ok is True
    assert result.trace_id == "trace-test"
    assert result.source == "landed_backend:/search"
    assert result.error is None
    assert result.data is not None
    assert result.data["tool"] == "search_products"


def test_to_tool_response_error():
    raw_response = {
        "ok": False,
        "error": "LANDED_TIMEOUT",
        "message": "Backend timeout",
    }

    result = to_tool_response(
        raw_response=raw_response,
        trace_id="trace-test",
        source="landed_backend:/search",
    )

    assert result.ok is False
    assert result.trace_id == "trace-test"
    assert result.data is None
    assert result.error is not None
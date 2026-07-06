from packages.shared.logging import new_trace_id
from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response


def get_local_price(query: str) -> dict:
    """Get Colombian local-market price and availability context.

    Tries q first for compatibility. If backend requires query, retries with query.
    """
    trace_id = new_trace_id()

    raw_response = call_landed_api(
        "/compare",
        {"q": query},
        trace_id=trace_id,
    )

    response_body = raw_response.get("response_body") or {}
    message = str(response_body.get("message", "")) if isinstance(response_body, dict) else ""

    if not raw_response.get("ok") and "query param is required" in message:
        raw_response = call_landed_api(
            "/compare",
            {"query": query},
            trace_id=trace_id,
        )

    raw_response["tool"] = "get_local_price"

    tool_response = to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/compare",
    )

    return tool_response.model_dump()
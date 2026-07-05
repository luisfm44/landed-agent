from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.logging import new_trace_id


def get_local_price(query: str) -> dict:
    """Get Colombian local-market price context for a product query."""
    
    trace_id = new_trace_id()
    raw_response = call_landed_api("/compare", {"q": query}, trace_id=trace_id)
    raw_response["tool"] = "get_local_price"
    

    tool_response = to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/compare",
    )

    return tool_response.model_dump()
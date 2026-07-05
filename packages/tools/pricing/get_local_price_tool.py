from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.schemas.agent_response_schema import ToolResponse


def get_local_price(query: str, trace_id: str) -> ToolResponse:
    """Get Colombian local-market price context for a product query."""
    raw_response = call_landed_api("/compare", {"q": query}, trace_id=trace_id)
    raw_response["tool"] = "get_local_price"
    
    return to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/compare",
    )

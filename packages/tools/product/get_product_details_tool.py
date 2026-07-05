from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.schemas.agent_response_schema import ToolResponse

def get_product_details(query: str, trace_id: str) -> dict:
    """Resolve a query to canonical product details when possible.

    Use this before pricing or recommendations so downstream agents receive a
    stable product identity instead of only free text.
    """
    raw_response = call_landed_api("/products/resolve/preview", {"q": query}, trace_id=trace_id)
    raw_response["tool"] = "get_product_details"
    
    return to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/products/resolve/preview",
    )

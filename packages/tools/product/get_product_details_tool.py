from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.logging import new_trace_id

def get_product_details(query: str) -> dict:
    """Resolve a query to canonical product details when possible.

    Use this before pricing or recommendations so downstream agents receive a
    stable product identity instead of only free text.
    """

    trace_id = new_trace_id()

    raw_response = call_landed_api("/products/resolve/preview", {"q": query}, trace_id=trace_id)
    raw_response["tool"] = "get_product_details"
    
    tool_response = to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/products/resolve/preview",
    )

    return tool_response.model_dump()
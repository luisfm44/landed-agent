from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.logging import new_trace_id

def search_products(query: str) -> dict:
    """Search imported and local product offers.
    
    Input contract:
    - query: natural-language product request or normalized search phrase.
    - trace_id: correlation id for observability.
    
    Output contract:
    - ToolResponse with backend search payload in data.
    """
    trace_id = new_trace_id()

    raw_response = call_landed_api("/search", {"q": query}, trace_id=trace_id)
    raw_response["tool"] = "search_products"
    
    tool_response = to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/search",
    )

    return tool_response.model_dump()
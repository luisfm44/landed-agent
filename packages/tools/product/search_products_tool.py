from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.schemas.agent_response_schema import ToolResponse

def search_products(query: str, trace_id:str) -> ToolResponse:
    """Search imported and local product offers.
    
    Input contract:
    - query: natural-language product request or normalized search phrase.
    - trace_id: correlation id for observability.
    
    Output contract:
    - ToolResponse with backend search payload in data.
    """
    raw_response = call_landed_api("/search", {"q": query})
    raw_response["tool"] = "search_products"
    
    return to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/search",
    )

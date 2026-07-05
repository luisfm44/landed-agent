from packages.tools.landed_api_client import call_landed_api
from packages.tools.tool_response_adapter import to_tool_response
from packages.shared.schemas.agent_response_schema import ToolResponse

def calculate_import_cost(query: str, trace_id: str) -> ToolResponse:
    """Calculate landed import cost context for a product query.

    This currently reuses the comparison endpoint. Keep this tool boundary so
    a dedicated import-cost service can replace it later without agent changes.
    """
    raw_response = call_landed_api("/compare", {"q": query})
    raw_response["tool"] = "calculate_import_cost"
    
    return to_tool_response(
        raw_response=raw_response,
        trace_id=trace_id,
        source="landed_backend:/compare",
    )

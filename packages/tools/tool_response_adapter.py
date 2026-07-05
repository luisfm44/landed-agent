from typing import Any
from packages.shared.schemas.agent_response_schema import ToolResponse

def to_tool_response(
    *,
    raw_response: dict[str, Any],
    trace_id: str,
    source: str,
) -> ToolResponse:
    """Normalize a raw backend response into the standar ToolResponse schema."""

    ok = bool(raw_response.get("ok", True))

    if not ok:
        return ToolResponse(
            ok = False,
            trace_id = trace_id,
            source = source,
            data = None,
            error=(
                raw_response.get("error")
                or raw_response.get("message")
                or "Tool call failed"
            ),
        )

    return ToolResponse(
        ok = True,
        trace_id = trace_id,
        source = source,
        data = raw_response,
        error = None,
    )
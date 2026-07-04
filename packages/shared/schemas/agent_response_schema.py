from pydantic import BaseModel, Field
from typing import Any


class ToolResponse(BaseModel):
    ok: bool
    trace_id: str
    source: str
    data: dict[str, Any] | None = None
    error: str | None = None

class AgentResponse(BaseModel):
    agent_name: str
    ok: bool
    confidence: float | None = Field(default=None, ge=0, le=1)
    output: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

class AgentTask(BaseModel):
    trace_id: str
    task_type: str
    payload: dict[str, Any]

class AgentResult(BaseModel):
    ok: bool
    trace_id: str
    agent_name: str
    dtat: dict[str, Any] | None = None
    error: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)

from typing import Any

from pydantic import BaseModel, Field


class ToolResponse(BaseModel):
    ok: bool
    trace_id: str
    source: str
    data: dict[str, Any] | None = None
    error: str | None = None


class AgentResponse(BaseModel):
    ok: bool
    trace_id: str
    agent_name: str
    confidence: float | None = Field(default=None, ge=0, le=1)
    output: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class AgentTask(BaseModel):
    trace_id: str
    task_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    ok: bool
    trace_id: str
    agent_name: str
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0, le=1)
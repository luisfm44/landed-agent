from pydantic import BaseModel, Field


class AgentTask(BaseModel):
    trace_id: str | None = None
    agent_name: str
    input: dict = Field(default_factory=dict)
    context: dict = Field(default_factory=dict)


class AgentResult(BaseModel):
    trace_id: str | None = None
    agent_name: str
    ok: bool
    output: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

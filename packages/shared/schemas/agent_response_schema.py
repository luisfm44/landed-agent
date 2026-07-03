from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    agent_name: str
    ok: bool
    confidence: float | None = Field(default=None, ge=0, le=1)
    output: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

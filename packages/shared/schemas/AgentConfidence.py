from pydantic import BaseModel, Field

class AgentConfidence(BaseModel):
    score: float = Field(ge=0, le=1)
    reason: str
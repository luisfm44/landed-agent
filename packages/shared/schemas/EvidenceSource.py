from pydantic import BaseModel, Field


class EvidenceSource(BaseModel):
    source: str
    description: str
    confidence: float = Field(ge=0, le=1)
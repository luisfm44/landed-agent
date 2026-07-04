from pydantic import BaseModel, Field

from packages.shared.schemas import EvidenceSource


class RecommendationResult(BaseModel):
    top_pick: str | None = None
    alternatives: list[str] = Field(default_factory=list)
    recomendation: str
    evidence: list[EvidenceSource] = Field(default_factory=list)
    uncertainty_factors: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
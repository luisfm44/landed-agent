from typing import Literal
from pydantic import BaseModel, Field


class UserShoppingIntent(BaseModel):
    query: str
    product_name: str | None = None
    category: str | None = None
    use_case: str | None = None
    budget: float | None = None
    currency: str = "USD"
    country: str = "Colombia"
    constraints: list[str] = Field(default_factory=list)


class ProductCandidate(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    estimated_price_usd: float | None = None
    availability: str | None = None


class TechnicalAnalysis(BaseModel):
    product_id: str
    use_case_fit: Literal["poor", "acceptable", "good", "excellent"]
    pros: list[str]
    cons: list[str]
    notes: str
    confidence: float = Field(ge=0, le=1)


class PricingResult(BaseModel):
    product_id: str
    local_price_cop: float | None = None
    local_price_usd: float | None = None
    source: str
    confidence: float = Field(ge=0, le=1)


class ImportCostResult(BaseModel):
    product_id: str
    base_price_usd: float
    shipping_usd: float
    taxes_usd: float
    total_landed_cost_usd: float
    confidence: float = Field(ge=0, le=1)


class EvidenceSource(BaseModel):
    source: str
    description: str
    confidence: float = Field(ge=0, le=1)


class AgentConfidence(BaseModel):
    score: float = Field(ge=0, le=1)
    reason: str


class DealAssessmentResult(BaseModel):
    product_id: str
    is_good_deal: bool
    reason: str
    risk_factors: list[str]
    confidence: float = Field(ge=0, le=1)


class RecommendationResult(BaseModel):
    top_pick: str | None
    alternatives: list[str] = Field(default_factory=list)
    recommendation: str
    evidence: list[EvidenceSource] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
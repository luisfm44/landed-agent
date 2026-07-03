from typing import Literal

from pydantic import BaseModel, Field


RecommendationVerdict = Literal[
    "Importar",
    "Comprar local",
    "Esperar",
    "Revisar manualmente",
]


class EvidenceSource(BaseModel):
    source_id: str | None = None
    source_type: str = Field(description="Origin type, such as api, rag, user, seller, or estimate.")
    name: str
    url: str | None = None
    retrieved_at: str | None = None
    is_estimated: bool = False


class AgentConfidence(BaseModel):
    score: float = Field(ge=0, le=1)
    rationale: str
    missing_evidence: list[str] = Field(default_factory=list)
    uncertainty_notes: list[str] = Field(default_factory=list)


class UserShoppingIntent(BaseModel):
    query: str = Field(description="Original user request.")
    category: str | None = Field(default=None, description="Product category.")
    use_case: str | None = Field(default=None, description="Primary user use case.")
    budget: float | None = Field(default=None, description="Maximum budget amount.")
    currency: str = Field(default="USD", description="Budget currency.")
    country: str = Field(default="Colombia", description="Destination/local market.")
    constraints: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)


class ProductCandidate(BaseModel):
    product_id: str | None = None
    name: str
    brand: str | None = None
    category: str | None = None
    price: float | None = None
    currency: str | None = None
    source: str | None = None
    url: str | None = None
    is_accessory: bool = False
    confidence: float | None = Field(default=None, ge=0, le=1)


class TechnicalAnalysis(BaseModel):
    product_id: str | None = None
    product_name: str
    use_case_fit: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0, le=1)


class PricingResult(BaseModel):
    product_id: str | None = None
    product_name: str
    local_price: float | None = None
    currency: str = "COP"
    seller: str | None = None
    availability: str | None = None
    source: str | None = None
    fetched_at: str | None = None
    is_estimated: bool = True


class ImportCostResult(BaseModel):
    product_id: str | None = None
    product_name: str
    base_price: float | None = None
    shipping: float | None = None
    taxes: float | None = None
    total_landed_cost: float | None = None
    currency: str = "COP"
    assumptions: list[str] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)
    is_estimated: bool = True


class DealAssessmentResult(BaseModel):
    product_id: str | None = None
    product_name: str
    verdict: RecommendationVerdict
    rationale: str
    evidence: list[EvidenceSource] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    confidence: AgentConfidence | None = None


class RecommendationItem(BaseModel):
    product_id: str | None = None
    product_name: str
    verdict: RecommendationVerdict
    rank: int
    rationale: str
    tradeoffs: list[str] = Field(default_factory=list)


class RecommendationResult(BaseModel):
    verdict: RecommendationVerdict
    summary: str
    items: list[RecommendationItem] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)

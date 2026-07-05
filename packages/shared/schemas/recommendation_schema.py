from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import (
    UserShoppingIntent,
    ProductCandidate,
    RecommendationResult,
    TechnicalAnalysis,
    PricingResult,
    ImportCostResult,
    DealAssessmentResult,
    UserShoppingIntent,
)


class RecommendationRequest(BaseModel):
    intent: UserShoppingIntent
    candidates: list[ProductCandidate] = Field(default_factory=list)
    technical_analysis: list[TechnicalAnalysis] = Field(default_factory=list)
    pricing_results: list[PricingResult] = Field(default_factory=list)
    import_cost_results: list[ImportCostResult] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    recommendation: RecommendationResult

from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import (
    ImportCostResult,
    PricingResult,
    ProductCandidate,
    RecommendationResult,
    TechnicalAnalysis,
    UserShoppingIntent,
)


class RecommendationRequest(BaseModel):
    user_intent: UserShoppingIntent
    candidate_products: list[ProductCandidate] = Field(default_factory=list)
    technical_analysis: list[TechnicalAnalysis] = Field(default_factory=list)
    pricing: list[PricingResult] = Field(default_factory=list)
    import_cost: list[ImportCostResult] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    recommendation: RecommendationResult

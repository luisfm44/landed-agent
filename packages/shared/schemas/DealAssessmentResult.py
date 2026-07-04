from pydantic import BaseModel, Field


class DealAssessmentResult(BaseModel):
    product_id: str
    is_good_deal: bool
    reason: str
    risk_factors: list[str]
    confidence: float = Field(ge=0, le=1)
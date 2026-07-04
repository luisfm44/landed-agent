from pydantic import BaseModel, Field


class PricingResult(BaseModel):
    product_id: str
    local_price_cop: float | None = None
    local_price_usd: float | None = None
    source: str
    confidence: float = Field(ge=0, le=1)
from pydantic import BaseModel, Field


class ImportCostResult(BaseModel):
    product_id: str
    base_price_usd: float
    shipping_usd: float
    taxes_usd: float
    total_landed_cost_usd: float
    confidence: float = Field(ge=0, le=1)
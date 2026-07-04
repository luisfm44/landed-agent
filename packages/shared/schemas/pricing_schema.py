from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import ImportCostResult, PricingResult


class LocalPriceRequest(BaseModel):
    product_id: str
    country: str = "Colombia"
    currency: str = "COP"

class LocalPriceResponse(BaseModel):
    pricing: PricingResult

class ImportCostRequest(BaseModel):
    product_id: str
    base_price_usd: float = Field(gt=0)
    destination_country: str = "Colombia"

class ImportCostResponse(BaseModel):
    import_cost: ImportCostResult

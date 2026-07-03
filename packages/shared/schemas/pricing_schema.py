from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import ImportCostResult, PricingResult


class PricingRequest(BaseModel):
    product_ids: list[str] = Field(default_factory=list)
    product_names: list[str] = Field(default_factory=list)
    country: str = "Colombia"
    currency: str = "COP"


class PricingBundle(BaseModel):
    local_prices: list[PricingResult] = Field(default_factory=list)
    import_costs: list[ImportCostResult] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)

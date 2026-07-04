from pydantic import BaseModel


class ProductCandidate(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    country: str = "Colombia"
    estimated_price_usd: float | None = None
    availability: str | None = None
    
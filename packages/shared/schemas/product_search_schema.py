from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import ProductCandidate


class ProductSearchRequest(BaseModel):
    query: str
    category: str | None = None
    budget: float | None = None
    currency: str = "USD"
    country: str = "Colombia"
    constraints: list[str] = Field(default_factory=list)


class ProductSearchResult(BaseModel):
    products: list[ProductCandidate] = Field(default_factory=list)
    source: str
    confidence: float | None = Field(default=None, ge=0, le=1)

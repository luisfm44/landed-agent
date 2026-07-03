from pydantic import BaseModel, Field

from packages.shared.schemas.commerce import ProductCandidate


class ProductSearchRequest(BaseModel):
    category: str | None = None
    budget: float | None = None
    currency: str = "USD"
    use_case: str | None = None
    preferences: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class ProductSearchResult(BaseModel):
    candidates: list[ProductCandidate] = Field(default_factory=list)
    missing_filters: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0, le=1)

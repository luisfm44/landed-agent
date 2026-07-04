from locale import currency

from pydantic import Field


class UserShoppingIntent(BaseModel):
    query: str
    product_name: str | None = None
    category: str | None = None
    use_case: str | None = None
    budget: float | None = None
    currency: str = "USD"
    country: str = "Colombia"
    constraints: list[str] = Field(default_factory=list)
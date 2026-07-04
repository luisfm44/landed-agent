from pydantic import BaseModel, Field
from typing import Literal

class TechnicalAnalysis(BaseModel):
    product_id: str
    use_case_fit: Literal["poor", "acceptable", "good", "excellent"]
    pros: list[str]
    cons: list[str]
    notes: str
    confidence: float = Field(ge=0, le=1)
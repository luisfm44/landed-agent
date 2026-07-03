class ToolError(Exception):
    """Base error for tool execution failures."""


class PricingUnavailableError(ToolError):
    """Raised when local pricing data cannot be retrieved."""


class ImportCostCalculationError(ToolError):
    """Raised when landed import cost cannot be calculated."""


class KnowledgeRetrievalError(ToolError):
    """Raised when product knowledge retrieval fails."""

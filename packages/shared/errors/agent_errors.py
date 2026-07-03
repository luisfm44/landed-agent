class AgentError(Exception):
    """Base error for specialist agent failures."""


class LowConfidenceRecommendationError(AgentError):
    """Raised when evidence is too weak for a confident recommendation."""


class ProductNotFoundError(AgentError):
    """Raised when a product cannot be resolved or found."""

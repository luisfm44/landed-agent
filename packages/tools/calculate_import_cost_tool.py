from packages.tools.landed_api_client import call_landed_api


def calculate_import_cost(query: str) -> dict:
    """Calculate landed import cost context for a product query."""
    return call_landed_api("/compare", {"q": query})

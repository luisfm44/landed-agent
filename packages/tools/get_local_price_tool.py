from packages.tools.landed_api_client import call_landed_api


def get_local_price(query: str) -> dict:
    """Get local Colombian market price context for a product query."""
    return call_landed_api("/compare", {"q": query})

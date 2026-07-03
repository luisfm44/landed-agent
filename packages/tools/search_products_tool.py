from packages.tools.landed_api_client import call_landed_api


def search_products(query: str) -> dict:
    """Search imported and local offers in Landed."""
    return call_landed_api("/search", {"q": query})

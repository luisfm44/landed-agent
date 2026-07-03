from packages.tools.landed_api_client import call_landed_api


def get_product_details(query: str) -> dict:
    """Resolve a user search query to a canonical Landed product."""
    return call_landed_api("/products/resolve/preview", {"q": query})

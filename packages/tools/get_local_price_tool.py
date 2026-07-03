from packages.tools.landed_api_client import call_landed_api


def get_local_price(query: str) -> dict:
    """Get Colombian local-market price context for a product query."""
    response = call_landed_api("/compare", {"q": query})
    response["tool"] = "get_local_price"
    return response

from packages.tools.landed_api_client import call_landed_api


def get_product_details(query: str) -> dict:
    """Resolve a query to canonical product details when possible.

    Use this before pricing or recommendations so downstream agents receive a
    stable product identity instead of only free text.
    """
    response = call_landed_api("/products/resolve/preview", {"q": query})
    response["tool"] = "get_product_details"
    return response

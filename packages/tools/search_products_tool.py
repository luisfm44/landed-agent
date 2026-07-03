from packages.tools.landed_api_client import call_landed_api


def search_products(query: str) -> dict:
    """Search imported and local product offers.

    Input contract:
    - query: natural-language product request or normalized search phrase.

    Output contract:
    - ok: whether the backend call succeeded.
    - data: backend search payload with candidate offers.
    """
    response = call_landed_api("/search", {"q": query})
    response["tool"] = "search_products"
    return response

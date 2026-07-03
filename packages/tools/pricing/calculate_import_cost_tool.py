from packages.tools.landed_api_client import call_landed_api


def calculate_import_cost(query: str) -> dict:
    """Calculate landed import cost context for a product query.

    This currently reuses the comparison endpoint. Keep this tool boundary so
    a dedicated import-cost service can replace it later without agent changes.
    """
    response = call_landed_api("/compare", {"q": query})
    response["tool"] = "calculate_import_cost"
    return response

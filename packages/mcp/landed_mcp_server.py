from typing import Any

from mcp.server.fastmcp import FastMCP

from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge
from packages.tools.pricing.calculate_import_cost_tool import calculate_import_cost
from packages.tools.pricing.get_local_price_tool import get_local_price
from packages.tools.product.get_product_details_tool import get_product_details
from packages.tools.product.search_products_tool import search_products

mcp = FastMCP("landed-domain-mcp")


@mcp.tool()
def retrieve_landed_knowledge(query: str, limit: int = 4) -> dict[str, Any]:
    """Retrieve grounded local knowledge from the Landed knowledge base.

    Use for evidence-backed guidance about audio products, headphones, DACs,
    amplifiers, local vs import purchase reasoning, and Colombia import context.

    Returns grounded_answer, sources, backend, and grounding status.
    """
    return retrieve_knowledge(query=query, limit=limit)


@mcp.tool()
def search_landed_products(query: str) -> dict[str, Any]:
    """Search imported and local product offers from the Landed backend."""
    return search_products(query=query)


@mcp.tool()
def get_landed_product_details(query: str) -> dict[str, Any]:
    """Resolve a product query to canonical product details when possible.

    The query can be a product title, model name, or identifier understood by
    the Landed backend resolver.
    """
    return get_product_details(query=query)


@mcp.tool()
def get_landed_local_price(query: str) -> dict[str, Any]:
    """Get Colombian local-market price and availability context."""
    return get_local_price(query=query)


@mcp.tool()
def calculate_landed_import_cost(query: str) -> dict[str, Any]:
    """Calculate landed import cost context for a product query in Colombia."""
    return calculate_import_cost(query=query)


if __name__ == "__main__":
    mcp.run()

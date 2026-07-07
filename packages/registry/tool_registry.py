from dataclasses import dataclass
from typing import Literal

ToolCategory = Literal["knowledge", "product", "pricing", "import_cost"]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    category: ToolCategory
    description: str
    mcp_name: str | None
    requires_auth: bool
    allowed_agents: frozenset[str]
    backend_path: str | None = None


TOOL_REGISTRY: dict[str, ToolDefinition] = {
    "retrieve_knowledge": ToolDefinition(
        name="retrieve_knowledge",
        category="knowledge",
        description="Retrieve grounded local knowledge with sources.",
        mcp_name="retrieve_landed_knowledge",
        requires_auth=False,
        allowed_agents=frozenset(
            {"audio_expert", "recommendation", "deal_advisor"}
        ),
    ),
    "search_products": ToolDefinition(
        name="search_products",
        category="product",
        description="Search imported and local product offers.",
        mcp_name="search_landed_products",
        requires_auth=True,
        allowed_agents=frozenset({"product_search"}),
        backend_path="/search",
    ),
    "get_product_details": ToolDefinition(
        name="get_product_details",
        category="product",
        description="Resolve a product query to canonical product details.",
        mcp_name="get_landed_product_details",
        requires_auth=True,
        allowed_agents=frozenset({"product_search"}),
        backend_path="/products/resolve/preview",
    ),
    "get_local_price": ToolDefinition(
        name="get_local_price",
        category="pricing",
        description="Get Colombian local-market price and availability context.",
        mcp_name="get_landed_local_price",
        requires_auth=True,
        allowed_agents=frozenset({"pricing", "deal_advisor"}),
        backend_path="/compare",
    ),
    "calculate_import_cost": ToolDefinition(
        name="calculate_import_cost",
        category="import_cost",
        description="Calculate landed import cost context for a product query.",
        mcp_name="calculate_landed_import_cost",
        requires_auth=True,
        allowed_agents=frozenset({"import_cost", "deal_advisor"}),
        backend_path="/compare",
    ),
}


def get_tool(name: str) -> ToolDefinition | None:
    return TOOL_REGISTRY.get(name)


def list_tools() -> list[ToolDefinition]:
    return list(TOOL_REGISTRY.values())


def list_mcp_tools() -> list[ToolDefinition]:
    return [tool for tool in TOOL_REGISTRY.values() if tool.mcp_name]


def resolve_tool_by_mcp_name(mcp_name: str) -> ToolDefinition | None:
    for tool in TOOL_REGISTRY.values():
        if tool.mcp_name == mcp_name:
            return tool
    return None

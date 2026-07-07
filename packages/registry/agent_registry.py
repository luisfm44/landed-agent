from dataclasses import dataclass
from typing import Literal

AgentRuntime = Literal["ADK", "LangGraph", "MCP"]


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    role: str
    runtime: AgentRuntime
    exposed_via_a2a: bool
    allowed_tools: frozenset[str]
    is_orchestrator: bool = False


AGENT_REGISTRY: dict[str, AgentDefinition] = {
    "landed_orchestrator": AgentDefinition(
        name="landed_orchestrator",
        role="Supervisor: plan, delegate, synthesize.",
        runtime="ADK",
        exposed_via_a2a=False,
        allowed_tools=frozenset(),
        is_orchestrator=True,
    ),
    "product_search": AgentDefinition(
        name="product_search",
        role="Resolve products and find candidate offers.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset({"search_products", "get_product_details"}),
    ),
    "audio_expert": AgentDefinition(
        name="audio_expert",
        role="Technical audio fit and buying guidance.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset({"retrieve_knowledge"}),
    ),
    "pricing": AgentDefinition(
        name="pricing",
        role="Colombian local price context.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset({"get_local_price"}),
    ),
    "import_cost": AgentDefinition(
        name="import_cost",
        role="Landed import cost analysis.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset({"calculate_import_cost"}),
    ),
    "deal_advisor": AgentDefinition(
        name="deal_advisor",
        role="Assess whether a concrete buying opportunity is worth it.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset(
            {"get_local_price", "calculate_import_cost", "retrieve_knowledge"}
        ),
    ),
    "recommendation": AgentDefinition(
        name="recommendation",
        role="Final buying recommendation from grounded evidence.",
        runtime="ADK",
        exposed_via_a2a=True,
        allowed_tools=frozenset({"retrieve_knowledge"}),
    ),
}

ORCHESTRATOR_DELEGATES: frozenset[str] = frozenset(
    {
        "product_search",
        "audio_expert",
        "pricing",
        "import_cost",
        "deal_advisor",
        "recommendation",
    }
)


def get_agent(name: str) -> AgentDefinition | None:
    return AGENT_REGISTRY.get(name)


def list_agents() -> list[AgentDefinition]:
    return list(AGENT_REGISTRY.values())


def list_a2a_agents() -> list[AgentDefinition]:
    return [
        agent
        for agent in AGENT_REGISTRY.values()
        if agent.exposed_via_a2a and not agent.is_orchestrator
    ]

from __future__ import annotations

from typing import Any

from packages.registry.agent_registry import (
    AGENT_REGISTRY,
    ORCHESTRATOR_DELEGATES,
    AgentDefinition,
)
from packages.registry.tool_registry import TOOL_REGISTRY, ToolDefinition

MCP_TOOL_NAMES: frozenset[str] = frozenset(
    {
        "retrieve_landed_knowledge",
        "search_landed_products",
        "get_landed_product_details",
        "get_landed_local_price",
        "calculate_landed_import_cost",
    }
)


def _tool_names_from_agent(agent: Any) -> set[str]:
    names: set[str] = set()

    for tool in getattr(agent, "tools", []) or []:
        tool_name = getattr(tool, "__name__", None)
        if tool_name:
            names.add(tool_name)

    return names


def _delegated_agent_names(orchestrator: Any) -> set[str]:
    names: set[str] = set()

    for tool in getattr(orchestrator, "tools", []) or []:
        wrapped_agent = getattr(tool, "agent", None)
        if wrapped_agent is None:
            continue

        agent_name = getattr(wrapped_agent, "name", None)
        if agent_name:
            names.add(agent_name)

    return names


def validate_registry_internal_consistency() -> list[str]:
    """Ensure tool and agent registries agree with each other."""
    errors: list[str] = []

    for tool_name, tool in TOOL_REGISTRY.items():
        if tool.name != tool_name:
            errors.append(
                f"Tool registry key '{tool_name}' does not match definition name '{tool.name}'."
            )

        for agent_name in tool.allowed_agents:
            agent = AGENT_REGISTRY.get(agent_name)
            if agent is None:
                errors.append(
                    f"Tool '{tool_name}' allows unknown agent '{agent_name}'."
                )
                continue

            if tool_name not in agent.allowed_tools:
                errors.append(
                    f"Tool '{tool_name}' allows agent '{agent_name}', but agent registry does not list the tool."
                )

    for agent_name, agent in AGENT_REGISTRY.items():
        if agent.name != agent_name:
            errors.append(
                f"Agent registry key '{agent_name}' does not match definition name '{agent.name}'."
            )

        for tool_name in agent.allowed_tools:
            tool = TOOL_REGISTRY.get(tool_name)
            if tool is None:
                errors.append(
                    f"Agent '{agent_name}' allows unknown tool '{tool_name}'."
                )
                continue

            if agent_name not in tool.allowed_agents:
                errors.append(
                    f"Agent '{agent_name}' allows tool '{tool_name}', but tool registry does not list the agent."
                )

        if agent.is_orchestrator and agent.allowed_tools:
            errors.append(
                f"Orchestrator '{agent_name}' must not declare direct tool permissions."
            )

    return errors


def validate_orchestrator_delegates() -> list[str]:
    errors: list[str] = []

    if ORCHESTRATOR_DELEGATES != frozenset(
        name
        for name, agent in AGENT_REGISTRY.items()
        if not agent.is_orchestrator and agent.runtime == "ADK"
    ):
        errors.append(
            "ORCHESTRATOR_DELEGATES must match all non-orchestrator ADK agents."
        )

    return errors


def validate_adk_agents_against_registry() -> list[str]:
    """Compare live ADK agent definitions with the registry."""
    from packages.agents.audio_expert.audio_expert_agent import audio_expert_agent
    from packages.agents.deal_advisor.deal_advisor_agent import deal_advisor_agent
    from packages.agents.import_cost.import_cost_agent import import_cost_agent
    from packages.agents.orchestrator.landed_orchestrator_agent import root_agent
    from packages.agents.pricing.pricing_agent import pricing_agent
    from packages.agents.product_search.product_search_agent import product_search_agent
    from packages.agents.recommendation.recommendation_agent import recommendation_agent

    errors: list[str] = []

    live_specialists = {
        "product_search": product_search_agent,
        "audio_expert": audio_expert_agent,
        "pricing": pricing_agent,
        "import_cost": import_cost_agent,
        "deal_advisor": deal_advisor_agent,
        "recommendation": recommendation_agent,
    }

    for agent_name, live_agent in live_specialists.items():
        registry_agent = AGENT_REGISTRY.get(agent_name)
        if registry_agent is None:
            errors.append(f"Live ADK agent '{agent_name}' is missing from AGENT_REGISTRY.")
            continue

        if live_agent.name != registry_agent.name:
            errors.append(
                f"ADK agent name mismatch for '{agent_name}': live='{live_agent.name}' registry='{registry_agent.name}'."
            )

        live_tools = _tool_names_from_agent(live_agent)
        if live_tools != set(registry_agent.allowed_tools):
            errors.append(
                f"ADK agent '{agent_name}' tools {sorted(live_tools)} do not match registry {sorted(registry_agent.allowed_tools)}."
            )

    if root_agent.name != AGENT_REGISTRY["landed_orchestrator"].name:
        errors.append("Root orchestrator name does not match registry.")

    delegated = _delegated_agent_names(root_agent)
    if delegated != set(ORCHESTRATOR_DELEGATES):
        errors.append(
            f"Orchestrator delegates {sorted(delegated)} do not match registry {sorted(ORCHESTRATOR_DELEGATES)}."
        )

    return errors


def validate_mcp_against_registry() -> list[str]:
    """Ensure MCP server exposes exactly the registry-backed MCP tools."""
    import packages.mcp.landed_mcp_server as mcp_server

    errors: list[str] = []
    exposed = {
        name
        for name in dir(mcp_server)
        if name in MCP_TOOL_NAMES and callable(getattr(mcp_server, name))
    }

    if exposed != set(MCP_TOOL_NAMES):
        errors.append(
            f"MCP exposed tools {sorted(exposed)} do not match expected {sorted(MCP_TOOL_NAMES)}."
        )

    for mcp_name in MCP_TOOL_NAMES:
        tool = next(
            (item for item in TOOL_REGISTRY.values() if item.mcp_name == mcp_name),
            None,
        )
        if tool is None:
            errors.append(f"MCP tool '{mcp_name}' is not registered in TOOL_REGISTRY.")

    return errors


def validate_registry() -> list[str]:
    """Run all registry consistency checks."""
    errors: list[str] = []
    errors.extend(validate_registry_internal_consistency())
    errors.extend(validate_orchestrator_delegates())
    errors.extend(validate_adk_agents_against_registry())
    errors.extend(validate_mcp_against_registry())
    return errors


def assert_registry_is_valid() -> None:
    errors = validate_registry()
    if errors:
        joined = "\n - ".join(errors)
        raise RuntimeError(f"Registry validation failed:\n - {joined}")

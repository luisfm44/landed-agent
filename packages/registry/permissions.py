from packages.registry.agent_registry import AGENT_REGISTRY, get_agent
from packages.registry.tool_registry import (
    TOOL_REGISTRY,
    get_tool,
    list_mcp_tools,
    resolve_tool_by_mcp_name,
)


def can_agent_use_tool(agent_name: str, tool_name: str) -> bool:
    agent = get_agent(agent_name)
    if agent is None:
        return False

    if agent.is_orchestrator:
        return False

    return tool_name in agent.allowed_tools


def assert_agent_can_use_tool(agent_name: str, tool_name: str) -> None:
    if not can_agent_use_tool(agent_name, tool_name):
        raise PermissionError(
            f"Agent '{agent_name}' is not allowed to use tool '{tool_name}'."
        )


def can_mcp_call_tool(mcp_name: str) -> bool:
    tool = resolve_tool_by_mcp_name(mcp_name)
    return tool is not None and tool.mcp_name is not None


def get_tools_for_agent(agent_name: str) -> list[str]:
    agent = get_agent(agent_name)
    if agent is None:
        return []

    return sorted(agent.allowed_tools)


def get_agents_for_tool(tool_name: str) -> list[str]:
    tool = get_tool(tool_name)
    if tool is None:
        return []

    return sorted(tool.allowed_agents)


def get_mcp_exposure_map() -> dict[str, str]:
    """Map internal tool names to MCP tool names."""
    return {
        tool.name: tool.mcp_name
        for tool in list_mcp_tools()
        if tool.mcp_name is not None
    }


def registry_summary() -> dict[str, int]:
    return {
        "tools": len(TOOL_REGISTRY),
        "agents": len(AGENT_REGISTRY),
        "mcp_tools": len(list_mcp_tools()),
        "a2a_agents": len(
            [agent for agent in AGENT_REGISTRY.values() if agent.exposed_via_a2a]
        ),
    }

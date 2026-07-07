from packages.registry.bootstrap import (
    assert_registry_is_valid,
    validate_adk_agents_against_registry,
    validate_mcp_against_registry,
    validate_registry,
    validate_registry_internal_consistency,
)
from packages.registry.permissions import (
    can_agent_use_tool,
    can_mcp_call_tool,
    get_mcp_exposure_map,
    get_tools_for_agent,
    registry_summary,
)


def test_registry_internal_consistency_has_no_errors():
    assert validate_registry_internal_consistency() == []


def test_orchestrator_delegates_match_specialists():
    from packages.registry.agent_registry import ORCHESTRATOR_DELEGATES

    assert len(ORCHESTRATOR_DELEGATES) == 6


def test_adk_agents_match_registry():
    assert validate_adk_agents_against_registry() == []


def test_mcp_tools_match_registry():
    assert validate_mcp_against_registry() == []


def test_validate_registry_passes():
    assert validate_registry() == []


def test_assert_registry_is_valid():
    assert_registry_is_valid()


def test_permissions_allow_expected_tools():
    assert can_agent_use_tool("audio_expert", "retrieve_knowledge") is True
    assert can_agent_use_tool("audio_expert", "calculate_import_cost") is False
    assert can_agent_use_tool("deal_advisor", "get_local_price") is True
    assert can_agent_use_tool("product_search", "search_products") is True


def test_mcp_permissions():
    assert can_mcp_call_tool("retrieve_landed_knowledge") is True
    assert can_mcp_call_tool("search_landed_products") is True
    assert can_mcp_call_tool("unknown_tool") is False


def test_registry_summary():
    summary = registry_summary()

    assert summary["tools"] == 5
    assert summary["agents"] == 7
    assert summary["mcp_tools"] == 5
    assert summary["a2a_agents"] == 6


def test_get_tools_for_agent():
    assert get_tools_for_agent("pricing") == ["get_local_price"]
    assert get_tools_for_agent("recommendation") == ["retrieve_knowledge"]


def test_mcp_exposure_map():
    exposure = get_mcp_exposure_map()

    assert exposure["retrieve_knowledge"] == "retrieve_landed_knowledge"
    assert exposure["search_products"] == "search_landed_products"
    assert len(exposure) == 5

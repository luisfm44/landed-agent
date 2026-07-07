from packages.agents.orchestrator.landed_orchestrator_agent import root_agent


def test_adk_root_agent_is_configured():
    assert root_agent.name == "landed_orchestrator"
    assert root_agent.model is not None
    assert root_agent.instruction is not None
    assert len(root_agent.tools) == 6
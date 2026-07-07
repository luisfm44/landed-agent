import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from packages.agents.orchestrator.landed_orchestrator_agent import root_agent
from packages.shared.config import LLM_RUNTIME


if __name__ == "__main__":
    print("=== LANDED ADK MULTI-AGENT ORCHESTRATOR ===")
    print(f"Runtime: {LLM_RUNTIME}")
    print(f"Agent name: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Tools/AgentTools: {len(root_agent.tools)}")

    for tool in root_agent.tools:
        print(f"- {getattr(tool, 'name', tool.__class__.__name__)}")
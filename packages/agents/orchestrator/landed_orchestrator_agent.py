from google.adk.agents import Agent
from google.adk.tools import AgentTool

from packages.agents.audio_expert.audio_expert_agent import audio_expert_agent
from packages.agents.deal_advisor.deal_advisor_agent import deal_advisor_agent
from packages.agents.import_cost.import_cost_agent import import_cost_agent
from packages.agents.orchestrator.prompts import ORCHESTRATOR_INSTRUCTIONS
from packages.agents.pricing.pricing_agent import pricing_agent
from packages.agents.product_search.product_search_agent import product_search_agent
from packages.agents.recommendation.recommendation_agent import recommendation_agent
from packages.shared.config import ORCHESTRATOR_MODEL, resolve_agent_model


root_agent = Agent(
    name="landed_orchestrator",
    model=resolve_agent_model(ORCHESTRATOR_MODEL),
    instruction=ORCHESTRATOR_INSTRUCTIONS,
    tools=[
        AgentTool(agent=product_search_agent),
        AgentTool(agent=audio_expert_agent),
        AgentTool(agent=pricing_agent),
        AgentTool(agent=import_cost_agent),
        AgentTool(agent=deal_advisor_agent),
        AgentTool(agent=recommendation_agent),
    ],
)
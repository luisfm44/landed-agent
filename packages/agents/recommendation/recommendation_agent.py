from google.adk.agents import Agent

from packages.agents.recommendation.prompts import RECOMMENDATION_INSTRUCTIONS
from packages.shared.config import REASONING_AGENT_MODEL, resolve_agent_model
from packages.tools import retrieve_knowledge

recommendation_agent = Agent(
    name="recommendation",
    model=resolve_agent_model(REASONING_AGENT_MODEL),
    instruction=RECOMMENDATION_INSTRUCTIONS,
    tools=[retrieve_knowledge],
)

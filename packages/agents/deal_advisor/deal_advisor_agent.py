from google.adk.agents import Agent

from packages.agents.deal_advisor.prompts import DEAL_ADVISOR_INSTRUCTIONS
from packages.shared.config import REASONING_AGENT_MODEL
from packages.tools import calculate_import_cost, get_local_price, retrieve_knowledge

deal_advisor_agent = Agent(
    name="deal_advisor",
    model=REASONING_AGENT_MODEL,
    instruction=DEAL_ADVISOR_INSTRUCTIONS,
    tools=[get_local_price, calculate_import_cost, retrieve_knowledge],
)

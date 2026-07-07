from google.adk.agents import Agent

from packages.agents.pricing.prompts import PRICING_INSTRUCTIONS
from packages.shared.config import FAST_AGENT_MODEL, resolve_agent_model
from packages.tools import get_local_price

pricing_agent = Agent(
    name="pricing",
    model=resolve_agent_model(FAST_AGENT_MODEL),
    instruction=PRICING_INSTRUCTIONS,
    tools=[get_local_price],
)

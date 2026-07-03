from google.adk.agents import Agent

from packages.agents.import_cost.prompts import IMPORT_COST_INSTRUCTIONS
from packages.shared.config import FAST_AGENT_MODEL
from packages.tools import calculate_import_cost

import_cost_agent = Agent(
    name="import_cost",
    model=FAST_AGENT_MODEL,
    instruction=IMPORT_COST_INSTRUCTIONS,
    tools=[calculate_import_cost],
)

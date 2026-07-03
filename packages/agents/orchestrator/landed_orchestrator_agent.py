from google.adk.agents import Agent

from packages.agents.orchestrator.prompts import ORCHESTRATOR_INSTRUCTIONS
from packages.shared.config import ORCHESTRATOR_MODEL
from packages.tools import (
    calculate_import_cost,
    get_local_price,
    get_product_details,
    retrieve_knowledge,
    search_products,
)

root_agent = Agent(
    name="landed_orchestrator",
    model=ORCHESTRATOR_MODEL,
    instruction=ORCHESTRATOR_INSTRUCTIONS,
    tools=[
        get_product_details,
        search_products,
        retrieve_knowledge,
        get_local_price,
        calculate_import_cost,
    ],
)

from google.adk.agents import Agent

from packages.agents.product_search.prompts import PRODUCT_SEARCH_INSTRUCTIONS
from packages.shared.config import FAST_AGENT_MODEL, resolve_agent_model
from packages.tools import get_product_details, search_products

product_search_agent = Agent(
    name="product_search",
    model=resolve_agent_model(FAST_AGENT_MODEL),
    instruction=PRODUCT_SEARCH_INSTRUCTIONS,
    tools=[get_product_details, search_products],
)

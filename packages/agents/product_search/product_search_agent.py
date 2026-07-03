from google.adk.agents import Agent

from packages.tools import get_product_details, search_products

product_search_agent = Agent(
    name="product_search",
    model="gemini-2.5-flash",
    instruction="""
You find and resolve products for Landed commerce workflows.
Always answer in Spanish and distinguish main products from accessories.
""",
    tools=[get_product_details, search_products],
)

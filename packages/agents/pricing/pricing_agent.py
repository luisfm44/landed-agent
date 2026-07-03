from google.adk.agents import Agent

from packages.tools import get_local_price

pricing_agent = Agent(
    name="pricing",
    model="gemini-2.5-flash",
    instruction="""
You analyze Colombian local market prices for Landed commerce workflows.
Always answer in Spanish and state when price data is estimated or incomplete.
""",
    tools=[get_local_price],
)

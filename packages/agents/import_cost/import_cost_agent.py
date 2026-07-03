from google.adk.agents import Agent

from packages.tools import calculate_import_cost

import_cost_agent = Agent(
    name="import_cost",
    model="gemini-2.5-flash",
    instruction="""
You estimate landed import costs, including shipping, taxes, and risk.
Always answer in Spanish and make assumptions explicit.
""",
    tools=[calculate_import_cost],
)

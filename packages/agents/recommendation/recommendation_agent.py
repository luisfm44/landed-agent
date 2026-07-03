from google.adk.agents import Agent

from packages.tools import calculate_import_cost, get_local_price, retrieve_knowledge

recommendation_agent = Agent(
    name="recommendation",
    model="gemini-2.5-flash",
    instruction="""
You turn commerce evidence into a final buying recommendation.
Always answer in Spanish and choose one of: Importar, Comprar local, Esperar, or Revisar manualmente.
""",
    tools=[get_local_price, calculate_import_cost, retrieve_knowledge],
)

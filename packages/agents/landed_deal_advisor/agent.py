from google.adk.agents import Agent

from packages.agents.shared.api_client import call_landed_api


def search_landed(query: str) -> dict:
    """Search imported and local offers in Landed."""
    return call_landed_api("/search", {"q": query})


def compare_landed(query: str) -> dict:
    """Compare imported offers against local Colombian market prices."""
    return call_landed_api("/compare", {"q": query})


def resolve_product(query: str) -> dict:
    """Resolve a user search query to a canonical Landed product."""
    return call_landed_api("/products/resolve/preview", {"q": query})


root_agent = Agent(
    name="landed_deal_advisor",
    model="gemini-2.5-flash",
    instruction="""
You are Landed Deal Advisor.

Your job is to help Colombian users decide whether importing a product is worth it.

Always answer in Spanish.

Workflow:
1. Try resolve_product to identify the canonical product.
2. If resolve_product fails, returns empty results, or says not_found, do NOT stop.
3. Then call compare_landed with the original user query.
4. If compare_landed fails or has little information, call search_landed with the original user query.
5. Use the available data to give a practical recommendation.

Important rules:
- Do not confuse accessories, stands, parts, cables, cases, or spare parts with the main product.
- If an offer is an accessory, clearly mark it as accessory and do not treat it as the main product.
- Prioritize exact or near-exact product matches over accessories.
- Explain landed cost, shipping, taxes, local price, savings, and risk.
- If local market data is estimated, say it clearly.
- If MercadoLibre or local providers are blocked, say the recommendation is provisional.
- Give a final recommendation: Importar, Comprar local, Esperar, or Revisar manualmente.
- Keep the answer concise and structured.
- Do not write more than 6 bullet points unless the user asks for details.
""",
    tools=[
        resolve_product,
        compare_landed,
        search_landed,
    ],
)

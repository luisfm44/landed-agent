# Architecture

`landed-ai-commerce-platform` is organized as a monorepo for commerce-focused AI agents.

## Packages

- `packages/agents/landed_deal_advisor`: Google ADK agent that helps Colombian users decide whether importing a product is worth it.
- `packages/agents/shared`: shared utilities for agents, starting with the Landed backend API client.

## Runtime Flow

1. A user asks the agent about a product.
2. The agent resolves the query to a canonical product when possible.
3. The agent compares imported offers with local Colombian market prices.
4. The agent falls back to search results when comparison data is incomplete.
5. The agent returns a concise recommendation in Spanish.

## External Dependencies

- Landed backend API, configured with `LANDED_API_BASE_URL`.
- Google ADK for agent runtime.

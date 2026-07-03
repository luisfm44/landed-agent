# Architecture

`landed-ai-commerce-platform` is organized as a monorepo for commerce-focused AI agents.

## Packages

- `packages/agents/orchestrator`: entry-point agent that coordinates the commerce workflow.
- `packages/agents/product_search`: agent focused on product resolution and offer discovery.
- `packages/agents/audio_expert`: domain expert agent for audio product buying guidance.
- `packages/agents/pricing`: agent focused on Colombian local market price context.
- `packages/agents/import_cost`: agent focused on landed import cost analysis.
- `packages/agents/recommendation`: agent focused on final buying recommendations.
- `packages/tools`: reusable tools for backend API calls, pricing, import cost, search, and retrieval.
- `packages/rag`: local knowledge collections for product knowledge, buying guides, reviews, and embeddings.
- `packages/shared`: shared schemas, DTOs, logging, and configuration.

## Runtime Flow

1. A user asks the agent about a product.
2. The orchestrator resolves the query to a canonical product when possible.
3. The orchestrator gathers local price and import cost evidence through tools.
4. The orchestrator falls back to product search or knowledge retrieval when information is incomplete.
5. Specialized agents can own narrower workflows as the platform grows.
6. The orchestrator returns a concise recommendation in Spanish.

## External Dependencies

- Landed backend API, configured with `LANDED_API_BASE_URL`.
- Google ADK for agent runtime.

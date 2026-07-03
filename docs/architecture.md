# Architecture

`landed-ai-commerce-platform` is organized as a monorepo for commerce-focused AI agents.

## Packages

- `packages/agents/orchestrator`: entry-point agent that coordinates the commerce workflow.
- `packages/agents/product_search`: agent focused on product resolution and offer discovery.
- `packages/agents/audio_expert`: domain expert agent for audio product buying guidance.
- `packages/agents/pricing`: agent focused on Colombian local market price context.
- `packages/agents/import_cost`: agent focused on landed import cost analysis.
- `packages/agents/recommendation`: agent focused on final buying recommendations.
- `packages/agents/deal_advisor`: specialist agent that evaluates whether a specific buying opportunity is worth it.
- `packages/tools`: reusable tools grouped by product, pricing, and knowledge domains.
- `packages/rag`: local knowledge collections for product knowledge, buying guides, reviews, embeddings, and ingestion.
- `packages/shared`: shared schemas, DTOs, logging, configuration, errors, and observability.

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

## Chapter 14 Pattern Mapping

The initial implementation follows a flat supervisor architecture:

- `LandedOrchestratorAgent` is the supervisor. It plans, delegates, handles fallbacks, and synthesizes the final answer.
- Specialist agents own narrow domains: product search, deal assessment, audio expertise, pricing, import cost, and recommendation.
- Tools perform concrete actions such as backend API calls, product search, price lookup, import cost lookup, and knowledge retrieval.
- Shared schemas define the contracts that agents should exchange as the platform matures.

`DealAdvisorAgent` is intentionally a specialist, not a second orchestrator. Use it when the user asks whether a concrete listing, used product, import opportunity, or local offer is a good deal.

The orchestrator prompt uses the RECAP / REASON / VERIFY loop as an internal reasoning discipline:

- RECAP: identify the user goal, budget, country, constraints, and missing data.
- REASON: choose the smallest useful set of specialist capabilities.
- VERIFY: ensure the recommendation respects constraints and states uncertainty.

## Data Contracts

The first shared contracts live in `packages/shared/schemas/commerce.py`:

- `UserShoppingIntent`
- `ProductCandidate`
- `TechnicalAnalysis`
- `PricingResult`
- `ImportCostResult`
- `RecommendationResult`

Domain-specific schema modules provide narrower contracts for agent work:

- `product_search_schema.py`
- `pricing_schema.py`
- `recommendation_schema.py`
- `agent_response_schema.py`

The lightweight agent transport DTOs live in `packages/shared/dto/agent_io.py`:

- `AgentTask`
- `AgentResult`

These contracts are intentionally small. They give each agent a stable vocabulary without forcing a full workflow engine too early.

## Fault Tolerance

Tools return normalized dictionaries with:

- `ok`
- `trace_id`
- `source`
- `data` or `error`

The API client includes configurable timeout, retry count, and exponential backoff. The orchestrator is instructed to continue with partial evidence when pricing, import cost, product search, or RAG retrieval are unavailable.

## Next Architecture Step

Today the orchestrator calls specialist capabilities as tools. The next step is to wrap specialist agents with ADK `AgentTool`, so the system follows the full Agent Delegates to Agent pattern:

```text
LandedOrchestratorAgent
  -> ProductSearchAgent
  -> DealAdvisorAgent
  -> AudioExpertAgent
  -> PricingAgent
  -> ImportCostAgent
  -> RecommendationAgent
```

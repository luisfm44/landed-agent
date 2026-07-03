# Architecture

`landed-ai-commerce-platform` is organized as a monorepo for commerce-focused AI agents. The architecture follows a flat supervisor model inspired by hierarchical multi-agent systems: one orchestrator coordinates the workflow, while specialist agents and tools handle narrow, well-defined responsibilities.

## Packages

- `packages/agents/orchestrator`: entry-point agent that coordinates the commerce workflow, manages fallbacks, and synthesizes the final answer.
- `packages/agents/product_search`: specialist agent focused on product resolution, candidate discovery, and offer search.
- `packages/agents/audio_expert`: specialist agent for audio product analysis, technical fit, and buying guidance.
- `packages/agents/pricing`: specialist agent focused on Colombian local market price context.
- `packages/agents/import_cost`: specialist agent focused on landed import cost analysis.
- `packages/agents/recommendation`: specialist agent focused on final buying recommendations.
- `packages/agents/deal_advisor`: specialist agent that evaluates whether a specific listing, used product, import opportunity, or local offer is worth it.
- `packages/tools`: reusable tools grouped by product, pricing, import, and knowledge domains.
- `packages/rag`: local knowledge collections for product knowledge, buying guides, reviews, embeddings, and ingestion.
- `packages/shared`: shared schemas, DTOs, logging, configuration, errors, and observability utilities.

## Runtime Flow

1. User submits a shopping or product-related query.
2. The orchestrator extracts the shopping intent, budget, country, constraints, and missing information.
3. The orchestrator resolves the query to a canonical product when possible, or falls back to product search when the product is ambiguous.
4. The orchestrator gathers local price, import cost, and technical evidence through tools or specialist capabilities.
5. The orchestrator uses knowledge retrieval when product, pricing, or technical evidence is incomplete.
6. Specialist agents can own narrower workflows as the platform grows.
7. If a dependency fails, the orchestrator continues with partial evidence when safe and clearly states uncertainty.
8. The orchestrator returns a concise recommendation in Spanish.

## External Dependencies

- Landed backend API, configured through `LANDED_API_BASE_URL`.
- Google ADK for agent runtime and agent orchestration.

## Suggested Implementation

The initial implementation follows a flat supervisor architecture.

- `LandedOrchestratorAgent` is the supervisor. It plans, delegates, handles fallbacks, and synthesizes the final answer.
- Specialist agents own narrow domains: product search, deal assessment, audio expertise, pricing, import cost, and recommendation.
- Tools perform concrete actions such as backend API calls, product search, price lookup, import cost lookup, and knowledge retrieval.
- Shared schemas define the contracts that agents should exchange as the platform matures.

`DealAdvisorAgent` is intentionally a specialist, not a second orchestrator. It should be used when the user asks whether a concrete listing, used product, import opportunity, or local offer is a good deal.

The orchestrator prompt uses the RECAP / REASON / VERIFY loop as an internal reasoning discipline:

- RECAP: identify the user goal, budget, country, constraints, available evidence, and missing data.
- REASON: choose the smallest useful set of specialist capabilities or tools.
- VERIFY: ensure the recommendation respects constraints, uses available evidence, and clearly states uncertainty.

## Data Contracts

The first shared contracts live in `packages/shared/schemas/commerce.py`:

- `UserShoppingIntent`
- `ProductCandidate`
- `TechnicalAnalysis`
- `PricingResult`
- `ImportCostResult`
- `DealAssessmentResult`
- `EvidenceSource`
- `AgentConfidence`
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

Tools return a normalized response envelope with:

- `ok`: whether the operation completed successfully.
- `trace_id`: correlation identifier for debugging and observability.
- `source`: origin of the evidence.
- `data`: successful payload.
- `error`: normalized failure payload.

The API client includes configurable timeout, retry count, and exponential backoff.

The orchestrator is instructed to continue with partial evidence when pricing, import cost, product search, or RAG retrieval are unavailable, as long as the answer remains safe and useful. When evidence is incomplete, the final recommendation must clearly state the uncertainty instead of pretending full confidence.

## Observability

Every agent and tool interaction should be traceable through a shared `trace_id`.

The platform should log:

- user intent extraction;
- selected agents or tools;
- tool inputs and outputs;
- fallback decisions;
- failed dependencies;
- final recommendation;
- confidence and uncertainty notes.

This supports debugging, auditability, evaluation, and future optimization of the agentic workflow.

## Next Architecture Step

Today, the orchestrator calls specialist capabilities mostly through tools. The next step is to wrap specialist agents with ADK `AgentTool`, so the system follows the full Agent Delegates to Agent pattern:

```text
LandedOrchestratorAgent
  -> ProductSearchAgent
  -> DealAdvisorAgent
  -> AudioExpertAgent
  -> PricingAgent
  -> ImportCostAgent
  -> RecommendationAgent
```

This evolution should happen progressively. The platform should first validate that the tools, schemas, fallback behavior, and recommendation quality are stable before increasing the depth of agent-to-agent delegation.

## Architecture Principle

Landed should avoid creating agents just for structural complexity. A new specialist agent should be introduced only when a capability has enough independent logic, tools, evaluation criteria, or failure behavior to justify being isolated.

The current target is a pragmatic multi-agent commerce platform: simple enough to debug, modular enough to evolve, and reliable enough to produce useful buying recommendations for users.

# landed-ai-commerce-platform

AI commerce platform for Landed agents and shared commerce tooling.

## Project Structure

```text
landed-ai-commerce-platform/
├── packages/
│   ├── agents/
│   │   ├── orchestrator/
│   │   │   ├── landed_orchestrator_agent.py
│   │   │   └── prompts.py
│   │   ├── product_search/
│   │   │   ├── product_search_agent.py
│   │   │   └── prompts.py
│   │   ├── audio_expert/
│   │   │   ├── audio_expert_agent.py
│   │   │   └── prompts.py
│   │   ├── pricing/
│   │   │   ├── pricing_agent.py
│   │   │   └── prompts.py
│   │   ├── import_cost/
│   │   │   ├── import_cost_agent.py
│   │   │   └── prompts.py
│   │   ├── recommendation/
│   │   │   ├── recommendation_agent.py
│   │   │   └── prompts.py
│   │   └── deal_advisor/
│   │       ├── deal_advisor_agent.py
│   │       └── prompts.py
│   ├── tools/
│   │   ├── product/
│   │   ├── pricing/
│   │   └── knowledge/
│   ├── knowledge_base/
│   │   └── audio/
│   ├── rag/
│   │   ├── embeddings/
│   │   ├── retriever.py
│   │   └── local_retriever.py
│   ├── graphs/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── landed_langgraph.py
│   └── shared/
│       ├── schemas/
│       ├── dto/
│       ├── logging/
│       ├── config/
│       ├── errors/
│       └── observability/
├── docs/
│   ├── architecture.md
│   ├── architecture-diagram.md
│   ├── roadmap.md
│   └── evaluation.md
├── docker-compose.yml
└── README.md
```

## Agents

### Orchestrator

Coordinates product search, pricing, import cost, retrieval, and recommendation agents to help Colombian users decide whether importing a product is worth it.

### Specialized Agents

- `product_search`: resolves products and finds offers.
- `audio_expert`: provides product guidance for audio categories.
- `pricing`: analyzes Colombian local market prices.
- `import_cost`: estimates landed import costs.
- `recommendation`: turns the evidence into a final buying recommendation.
- `deal_advisor`: evaluates whether a specific buying opportunity is a good deal.

### LangGraph workflow

`packages/graphs` provides a deterministic LangGraph path that reuses the same tools and grounding layer:

```text
START -> orchestrator_node -> knowledge_node -> recommendation_node -> END
```

Run locally:

```bash
python -m packages.graphs.landed_langgraph
```

## Configuration

Set the Landed backend URL with:

```bash
LANDED_API_BASE_URL=http://localhost:3001
```

### LLM runtime profiles

Use one codebase for local development and Google Cloud deployment:

| Profile | `LLM_RUNTIME` | Agent models | Notes |
|---------|---------------|--------------|-------|
| **GCP** (default) | `gcp` | `gemini-2.5-flash-lite` | Native ADK + Gemini |
| **Local** | `local` | `llama3.1` (Ollama) | LiteLLM + `ollama_chat/` |

Local example:

```bash
LLM_RUNTIME=local
ORCHESTRATOR_MODEL=llama3.1
FAST_AGENT_MODEL=llama3.1
REASONING_AGENT_MODEL=llama3.1
OLLAMA_HOST=http://localhost:11434
```

GCP example (Cloud Run, Vertex, etc.):

```bash
LLM_RUNTIME=gcp
ORCHESTRATOR_MODEL=gemini-2.5-flash-lite
FAST_AGENT_MODEL=gemini-2.5-flash-lite
REASONING_AGENT_MODEL=gemini-2.5-flash-lite
```

Copy `.env.example` to `.env` and adjust the profile you need.

## Documentation

- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/evaluation.md`

## Development Guide

- Add or refine agent behavior in `packages/agents/<agent_name>/`.
- Keep agent instructions in each agent's `prompts.py`.
- Add deterministic API calls or calculations in `packages/tools/`.
- Add typed contracts in `packages/shared/schemas/` and transport DTOs in `packages/shared/dto/`.
- Add runtime configuration in `packages/shared/config/`.
- Add domain errors in `packages/shared/errors/`.
- Add trace/log helpers in `packages/shared/logging/` and agent observability helpers in `packages/shared/observability/`.
- Add future retrieval corpora or indexes in `packages/rag/`.

The orchestrator should stay focused on planning, delegation, fallback handling, and final synthesis. Domain-specific rules should live in the specialist agent that owns that domain.

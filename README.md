# landed-ai-commerce-platform

AI commerce platform for Landed. It helps Colombian users decide what to buy and whether importing a product is worth it, using multi-agent orchestration, local knowledge retrieval, and grounded recommendations.

## What this repo provides

- **ADK multi-agent runtime** for conversational commerce assistance.
- **LangGraph workflow runtime** for deterministic, stateful flows.
- **Local RAG + grounding** over a unified markdown knowledge base.
- **Shared tools** for product search, pricing, import cost, and knowledge retrieval.

## Architecture at a glance

```text
User query
  ↓
LangGraph runtime (primary entry point)
  ↓
LandedGraphState + graph_orchestrator_node
  ↓
ADK landed_orchestrator + specialist agents
  ↓
Shared domain tools
  ↓
RAG + Grounding
  ↓
final response
```

LangGraph coordinates flow and short-term memory. ADK executes specialist agents. They do not compete as two top-level orchestrators.

Visual diagrams: [docs/architecture-diagram.md](docs/architecture-diagram.md)

## Project structure

```text
landed-ai-commerce-platform/
├── packages/
│   ├── agents/              # Google ADK specialist agents
│   │   ├── orchestrator/
│   │   ├── product_search/
│   │   ├── audio_expert/
│   │   ├── pricing/
│   │   ├── import_cost/
│   │   ├── recommendation/
│   │   └── deal_advisor/
│   ├── graphs/              # LangGraph workflow layer
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── landed_langgraph.py
│   ├── tools/               # Domain tools
│   │   ├── product/
│   │   ├── pricing/
│   │   └── knowledge/
│   ├── knowledge_base/      # Unified markdown corpus
│   │   └── audio/
│   ├── rag/                 # Retrieval + grounding
│   │   ├── retriever.py
│   │   ├── local_retriever.py
│   │   ├── grounding_service.py
│   │   └── embeddings/
│   └── shared/              # Schemas, config, logging, observability
├── docs/
│   ├── architecture.md
│   ├── architecture-diagram.md
│   ├── roadmap.md
│   └── evaluation.md
├── scripts/
│   └── run_adk_agent.py
├── .env.example
└── requirements.txt
```

## Orchestration layers

### LangGraph (primary entry point)

Entry point: `packages.graphs.landed_langgraph.build_landed_graph`

| Node | Role |
|------|------|
| `graph_orchestrator_node` | Session state, routing, short-term memory |
| `knowledge_node` | Grounding via `retrieve_knowledge` (lab shortcut) |
| `recommendation_node` | Builds `final_answer` from grounded evidence |

Current lab graph:

```text
START -> graph_orchestrator_node -> knowledge_node -> recommendation_node -> END
```

Run:

```bash
.venv/bin/python -m packages.graphs.landed_langgraph
```

Target architecture: `graph_orchestrator_node` will delegate to ADK `landed_orchestrator`, which will call specialist agents through `AgentTool`.

### ADK (agent execution layer)

Entry point: `packages.agents.orchestrator.root_agent`

| Agent | Responsibility |
|-------|----------------|
| `landed_orchestrator` | Business orchestration inside ADK |
| `product_search` | Product resolution and offer search |
| `audio_expert` | Technical audio guidance |
| `pricing` | Colombian local price context |
| `import_cost` | Landed import cost estimation |
| `deal_advisor` | Concrete deal assessment |
| `recommendation` | Final buying recommendation |

Inspect ADK setup during development:

```bash
.venv/bin/python scripts/run_adk_agent.py
```

This script is for development only. Production user traffic should enter through LangGraph.

## Knowledge, RAG, and grounding

All local knowledge lives in `packages/knowledge_base/`.

| Layer | Responsibility |
|-------|----------------|
| **RAG** | Retrieve relevant chunks from Chroma or lexical fallback |
| **Grounding** | Answer only from retrieved context, cite sources, refuse when evidence is insufficient |

Flow:

```text
retrieve_knowledge
  -> search_knowledge (Chroma + Ollama embeddings, lexical fallback)
  -> grounding_service (Ollama llama3.1, restrictive prompt)
  -> grounded_answer + sources
```

Index local knowledge:

```bash
ollama serve
ollama pull nomic-embed-text
ollama pull llama3.1

.venv/bin/python -m packages.tools.knowledge.ingest_documents
```

Test grounding directly:

```bash
.venv/bin/python -c "
from packages.tools.knowledge.retrieve_knowledge_tool import retrieve_knowledge
r = retrieve_knowledge('headphones for classical music and gaming')
print(r['data']['grounded_answer'])
"
```

## Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Shared setting:

```bash
LANDED_API_BASE_URL=http://localhost:3001
```

### LLM runtime profiles

Use one codebase for local development and Google Cloud deployment:

| Profile | `LLM_RUNTIME` | Agent models | Notes |
|---------|---------------|--------------|-------|
| **GCP** (default) | `gcp` | `gemini-2.5-flash-lite` | Native ADK + Gemini |
| **Local** | `local` | `llama3.1` | LiteLLM + `ollama_chat/` |

Local profile:

```bash
LLM_RUNTIME=local
ORCHESTRATOR_MODEL=llama3.1
FAST_AGENT_MODEL=llama3.1
REASONING_AGENT_MODEL=llama3.1
OLLAMA_HOST=http://localhost:11434
OLLAMA_GROUNDING_MODEL=llama3.1
```

GCP profile:

```bash
LLM_RUNTIME=gcp
ORCHESTRATOR_MODEL=gemini-2.5-flash-lite
FAST_AGENT_MODEL=gemini-2.5-flash-lite
REASONING_AGENT_MODEL=gemini-2.5-flash-lite
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Optional: index knowledge and verify grounding
ollama serve
.venv/bin/python -m packages.tools.knowledge.ingest_documents

# Verify orchestration layers
.venv/bin/python -m packages.graphs.landed_langgraph
.venv/bin/python scripts/run_adk_agent.py
```

## Documentation

- [docs/architecture.md](docs/architecture.md) — written architecture reference
- [docs/architecture-diagram.md](docs/architecture-diagram.md) — mermaid diagrams
- [docs/roadmap.md](docs/roadmap.md)
- [docs/evaluation.md](docs/evaluation.md)

## Development guide

- Add or refine agent behavior in `packages/agents/<agent_name>/`.
- Keep agent instructions in each agent's `prompts.py`.
- Add deterministic API calls or calculations in `packages/tools/`.
- Add graph nodes or edges in `packages/graphs/`.
- Add markdown knowledge in `packages/knowledge_base/`, then re-run ingest.
- Add typed contracts in `packages/shared/schemas/` and transport DTOs in `packages/shared/dto/`.
- Add runtime configuration in `packages/shared/config/`.
- Add domain errors in `packages/shared/errors/`.
- Add trace/log helpers in `packages/shared/logging/` and observability helpers in `packages/shared/observability/`.

The LangGraph layer should own workflow sequencing and short-term memory. The ADK orchestrator should own business delegation to specialist agents. Domain-specific rules should live in the specialist agent or graph node that owns that domain.

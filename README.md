# landed-ai-commerce-platform

AI commerce platform for Landed agents and shared commerce tooling.

## Project Structure

```text
landed-ai-commerce-platform/
├── packages/
│   ├── agents/
│   │   ├── orchestrator/
│   │   │   └── landed_orchestrator_agent.py
│   │   ├── product_search/
│   │   │   └── product_search_agent.py
│   │   ├── audio_expert/
│   │   │   └── audio_expert_agent.py
│   │   ├── pricing/
│   │   │   └── pricing_agent.py
│   │   ├── import_cost/
│   │   │   └── import_cost_agent.py
│   │   ├── recommendation/
│   │   │   └── recommendation_agent.py
│   │   └── landed_deal_advisor/
│   │       └── agent.py
│   ├── tools/
│   │   ├── search_products_tool.py
│   │   ├── get_product_details_tool.py
│   │   ├── get_local_price_tool.py
│   │   ├── calculate_import_cost_tool.py
│   │   └── retrieve_knowledge_tool.py
│   ├── rag/
│   │   ├── product_knowledge/
│   │   ├── buying_guides/
│   │   ├── reviews/
│   │   └── embeddings/
│   └── shared/
│       ├── schemas/
│       ├── dto/
│       ├── logging/
│       └── config/
├── docs/
│   ├── architecture.md
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

`landed_deal_advisor` remains as a compatibility alias for the orchestrator.

## Configuration

Set the Landed backend URL with:

```bash
LANDED_API_BASE_URL=http://localhost:3001
```

## Documentation

- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/evaluation.md`

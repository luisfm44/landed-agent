# landed-ai-commerce-platform

AI commerce platform for Landed agents and shared commerce tooling.

## Project Structure

```text
landed-ai-commerce-platform/
├── packages/
│   └── agents/
│       ├── landed_deal_advisor/
│       │   ├── __init__.py
│       │   └── agent.py
│       └── shared/
│           ├── __init__.py
│           └── api_client.py
├── docs/
│   ├── architecture.md
│   ├── roadmap.md
│   └── evaluation.md
├── docker-compose.yml
└── README.md
```

## Agents

### Landed Deal Advisor

Helps Colombian users decide whether importing a product is worth it by comparing imported offers, local prices, landed cost, taxes, savings, and risk.

## Configuration

Set the Landed backend URL with:

```bash
LANDED_API_BASE_URL=http://localhost:3001
```

## Documentation

- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/evaluation.md`

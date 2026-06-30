# Evaluation

The platform should evaluate agents against realistic commerce decisions, not only tool execution.

## Evaluation Areas

- Product matching accuracy.
- Correct handling of accessories versus main products.
- Import cost explanation, including shipping, taxes, local price, savings, and risk.
- Recommendation quality: `Importar`, `Comprar local`, `Esperar`, or `Revisar manualmente`.
- Transparency when data is estimated, blocked, or incomplete.

## Suggested Test Set

- Exact product queries.
- Ambiguous product queries.
- Accessory-heavy search results.
- Products with missing local market data.
- Cases where importing is cheaper but riskier.

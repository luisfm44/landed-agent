# Architecture Diagrams

Visual reference for the Landed multi-agent commerce platform. These diagrams complement [architecture.md](./architecture.md).

## 1. System overview

```mermaid
flowchart TB
    USER[User query] --> ORCH[landed_orchestrator<br/>ADK root_agent]

    subgraph agents [Specialist agents]
        PS[product_search]
        AE[audio_expert]
        PR[pricing]
        IC[import_cost]
        DA[deal_advisor]
        REC[recommendation]
    end

    ORCH -->|AgentTool| PS
    ORCH -->|AgentTool| AE
    ORCH -->|AgentTool| PR
    ORCH -->|AgentTool| IC
    ORCH -->|AgentTool| DA
    ORCH -->|AgentTool| REC

    subgraph tools [Domain tools]
        T1[search_products]
        T2[get_product_details]
        T3[get_local_price]
        T4[calculate_import_cost]
        T5[retrieve_knowledge]
    end

    PS --> T1
    PS --> T2
    PR --> T3
    IC --> T4
    DA --> T3
    DA --> T4
    AE --> T5
    REC --> T5
    DA --> T5

    T1 --> API[Landed API]
    T2 --> API
    T3 --> API
    T4 --> API

    T5 --> RAG[RAG + Grounding layer]

    subgraph llm [LLM runtime]
        GEMINI[Gemini<br/>LLM_RUNTIME=gcp]
        OLLAMA_AGENT[Ollama llama3.1<br/>LLM_RUNTIME=local]
    end

    ORCH -.-> GEMINI
    ORCH -.-> OLLAMA_AGENT
    agents -.-> GEMINI
    agents -.-> OLLAMA_AGENT

    ORCH --> USER
```

## 2. End-to-end request flow

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant O as Orchestrator
    participant PS as product_search
    participant AE as audio_expert
    participant PR as pricing
    participant IC as import_cost
    participant RK as retrieve_knowledge
    participant API as Landed API
    participant RAG as RAG + Grounding

    U->>O: Shopping question

    Note over O: RECAP / REASON / VERIFY

    O->>PS: AgentTool — resolve product
    PS->>API: search_products / get_product_details
    API-->>PS: candidates
    PS-->>O: product evidence

    O->>AE: AgentTool — technical fit
    AE->>RK: retrieve_knowledge
    RK->>RAG: search + ground
    RAG-->>RK: grounded_answer + sources
    RK-->>AE: ToolResponse
    AE-->>O: technical analysis

    O->>PR: AgentTool — local price
    PR->>API: get_local_price
    API-->>PR: pricing context
    PR-->>O: pricing result

    O->>IC: AgentTool — import cost
    IC->>API: calculate_import_cost
    API-->>IC: landed cost
    IC-->>O: import result

    O-->>U: Final recommendation in Spanish
```

Not every request uses all specialists. The orchestrator selects the smallest useful subset per turn.

## 3. Knowledge layer: RAG + grounding

```mermaid
flowchart TD
    Q[Agent calls retrieve_knowledge] --> TOOL[retrieve_knowledge_tool]

    TOOL --> SEARCH[search_knowledge]

    SEARCH --> SEM[Semantic retriever<br/>Chroma + nomic-embed-text]
    SEM -->|distance <= 0.45| HIT1[Valid semantic match]
    SEM -->|weak or error| LEX[Lexical retriever<br/>knowledge_base/*.md]
    LEX -->|score >= 0.35| HIT2[Valid lexical match]
    LEX -->|no match| MISS[No evidence]

    HIT1 --> GROUND[grounding_service]
    HIT2 --> GROUND
    MISS --> NOANS[grounded_answer:<br/>no local evidence]

    GROUND --> CTX[Context assembly<br/>max 6000 chars]
    CTX --> LLM[Ollama llama3.1<br/>restrictive prompt]
    LLM --> GA[grounded_answer<br/>+ sources + citations]

    GA --> RESP[ToolResponse to agent]
    NOANS --> RESP

    subgraph corpus [Unified corpus]
        KB[knowledge_base/audio/*.md]
        CHROMA[(Chroma index)]
    end

    KB --> SEM
    KB --> LEX
    KB -->|ingest_documents| CHROMA
    CHROMA --> SEM
```

### RAG vs grounding

| Stage | Responsibility | Output |
|-------|----------------|--------|
| **RAG** | Retrieve relevant chunks | `sources[]`, `backend` |
| **Grounding** | Constrain answer to sources | `grounded_answer`, citations, refusal |

## 4. LLM runtime profiles

```mermaid
flowchart LR
    ENV[.env<br/>LLM_RUNTIME] --> RESOLVE[resolve_agent_model]

    ENV -->|local| LOCAL[LiteLLM<br/>ollama_chat/llama3.1]
    ENV -->|gcp| GCP[Gemini string<br/>gemini-2.5-flash-lite]

    RESOLVE --> AGENTS[All ADK agents]

    subgraph always_local [Always local today]
        EMB[Embeddings<br/>nomic-embed-text]
        GR[Grounding<br/>llama3.1]
    end

    AGENTS --> LOCAL
    AGENTS --> GCP
    RAG_LAYER[RAG layer] --> EMB
    RAG_LAYER --> GR
```

## 5. Package map

```mermaid
flowchart TB
    subgraph packages [packages/]
        AGENTS[agents/<br/>orchestrator + specialists]
        TOOLS[tools/<br/>product, pricing, knowledge]
        KB[knowledge_base/<br/>markdown corpus]
        RAG[rag/<br/>retriever, grounding, Chroma]
        SHARED[shared/<br/>schemas, config, logging]
    end

    AGENTS --> TOOLS
    TOOLS --> RAG
    TOOLS --> SHARED
    RAG --> KB
    AGENTS --> SHARED
```

## Related docs

- [architecture.md](./architecture.md) — written architecture reference
- [evaluation.md](./evaluation.md) — evaluation notes
- [roadmap.md](./roadmap.md) — planned improvements

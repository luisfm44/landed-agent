# Architecture Diagrams

Visual reference for the Landed multi-agent commerce platform. These diagrams complement [architecture.md](./architecture.md).

## 1. Target system overview

LangGraph is the user entry point. ADK executes specialist agents inside the graph.

```mermaid
flowchart TB
    USER[User query] --> LG[LangGraph runtime<br/>build_landed_graph]

    subgraph graph [LangGraph coordination layer]
        STATE[LandedGraphState]
        GO[graph_orchestrator_node]
        KN[knowledge_node]
        RN[recommendation_node]
    end

    LG --> GO
    GO --> STATE
    GO --> ADK

    subgraph adk [ADK execution layer]
        ORCH[landed_orchestrator<br/>root_agent]
        PS[product_search]
        AE[audio_expert]
        PR[pricing]
        IC[import_cost]
        DA[deal_advisor]
        REC[recommendation]
    end

    ADK[ADK runtime] --> ORCH
    ORCH -->|AgentTool| PS
    ORCH -->|AgentTool| AE
    ORCH -->|AgentTool| PR
    ORCH -->|AgentTool| IC
    ORCH -->|AgentTool| DA
    ORCH -->|AgentTool| REC

    subgraph tools [Shared domain tools]
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
    KN --> T5

    T1 --> API[Landed API]
    T2 --> API
    T3 --> API
    T4 --> API
    T5 --> RAG[RAG + Grounding layer]

    ORCH --> STATE
    KN --> STATE
    RN --> STATE
    RN --> USER
```

## 2. Current lab graph

The repository currently ships a reduced grounding-first graph while ADK wiring is added incrementally.

```mermaid
flowchart LR
    USER[User query] --> LG[LangGraph runtime]
    LG --> GO[graph_orchestrator_node]
    GO --> KN[knowledge_node]
    KN --> RK[retrieve_knowledge]
    RK --> RAG[RAG + Grounding]
    KN --> RN[recommendation_node]
    RN --> USER

    subgraph state [LandedGraphState]
        S1[user_message / messages]
        S2[intent / constraints]
        S3[grounded_answer / sources]
        S4[final_answer]
    end

    GO --> S2
    KN --> S3
    RN --> S4
```

## 3. Target end-to-end flow

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant G as LangGraph app
    participant GO as graph_orchestrator_node
    participant O as ADK landed_orchestrator
    participant AE as audio_expert
    participant RK as retrieve_knowledge
    participant RAG as RAG + Grounding
    participant ST as LandedGraphState

    U->>G: invoke(user_message, session metadata)
    G->>GO: update routing and memory
    GO->>ST: current_intent, constraints, messages

    G->>O: delegate business orchestration
    O->>AE: AgentTool
    AE->>RK: retrieve_knowledge
    RK->>RAG: search + ground
    RAG-->>RK: grounded_answer + sources
    RK-->>AE: ToolResponse
    AE-->>O: technical evidence
    O-->>G: specialist findings

    G->>ST: merge grounding and agent outputs
    G-->>U: final_answer
```

## 4. ADK-only development flow

`scripts/run_adk_agent.py` is for inspecting the ADK layer directly during development. It is not the production user entry point.

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Developer
    participant O as landed_orchestrator
    participant PS as product_search
    participant API as Landed API

    Dev->>O: inspect ADK root_agent setup
    O->>PS: AgentTool when invoked in a session
    PS->>API: shared tools
```

## 5. Knowledge layer: RAG + grounding

```mermaid
flowchart TD
    Q[retrieve_knowledge call] --> TOOL[retrieve_knowledge_tool]

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

    GA --> RESP[ToolResponse]
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

## 6. LLM runtime profiles

```mermaid
flowchart LR
    ENV[.env<br/>LLM_RUNTIME] --> RESOLVE[resolve_agent_model]

    ENV -->|local| LOCAL[LiteLLM<br/>ollama_chat/llama3.1]
    ENV -->|gcp| GCP[Gemini string<br/>gemini-2.5-flash-lite]

    RESOLVE --> ADK[ADK specialist agents]

    subgraph always_local [Always local today]
        EMB[Embeddings<br/>nomic-embed-text]
        GR[Grounding<br/>llama3.1]
    end

    ADK --> LOCAL
    ADK --> GCP
    RAG_LAYER[RAG layer] --> EMB
    RAG_LAYER --> GR
```

## 7. MCP tool ecosystem

MCP is a fourth entry point into the same shared tools used by LangGraph and ADK.

```mermaid
flowchart TB
    subgraph clients [Entry points]
        LG[LangGraph runtime]
        ADK[ADK specialist agents]
        MCP[Cursor / MCP client]
    end

    subgraph exposure [Exposure layers]
        GN[graph nodes]
        AT[AgentTool delegation]
        MS[landed-domain-mcp]
    end

    subgraph tools [Shared domain tools]
        T1[search_products]
        T2[get_product_details]
        T3[get_local_price]
        T4[calculate_import_cost]
        T5[retrieve_knowledge]
    end

    LG --> GN
    ADK --> AT
    MCP --> MS

    GN --> T5
    AT --> T1
    AT --> T2
    AT --> T3
    AT --> T4
    AT --> T5

    MS -->|search_landed_products| T1
    MS -->|get_landed_product_details| T2
    MS -->|get_landed_local_price| T3
    MS -->|calculate_landed_import_cost| T4
    MS -->|retrieve_landed_knowledge| T5

    T1 --> API[Landed API]
    T2 --> API
    T3 --> API
    T4 --> API
    T5 --> RAG[RAG + Grounding]
```

## 8. Package map

```mermaid
flowchart TB
    subgraph packages [packages/]
        GRAPHS[graphs/<br/>LangGraph entry + state]
        AGENTS[agents/<br/>ADK orchestrator + specialists]
        MCP[mcp/<br/>landed-domain-mcp]
        TOOLS[tools/<br/>product, pricing, knowledge]
        KB[knowledge_base/<br/>markdown corpus]
        RAG[rag/<br/>retriever, grounding, Chroma]
        SHARED[shared/<br/>schemas, config, logging]
    end

    GRAPHS --> AGENTS
    GRAPHS --> TOOLS
    AGENTS --> TOOLS
    MCP --> TOOLS
    TOOLS --> RAG
    TOOLS --> SHARED
    RAG --> KB
    AGENTS --> SHARED
    GRAPHS --> SHARED
    MCP --> SHARED
```

## Related docs

- [architecture.md](./architecture.md) — written architecture reference
- [evaluation.md](./evaluation.md) — evaluation notes
- [roadmap.md](./roadmap.md) — planned improvements

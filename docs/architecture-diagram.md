# Architecture Diagrams

Visual reference for the Landed multi-agent commerce platform. These diagrams complement [architecture.md](./architecture.md).

> **Updated:** default LangGraph flow uses `adk_orchestrator_node` + `adk_runner.py`. System-level registry lives in `packages/registry/`.

## 1. Platform layers with registry

Four cooperating layers, three entry points, one shared tool ecosystem, and one cross-cutting registry.

```mermaid
flowchart TB
    subgraph system [System-level layer]
        REG[Tool & Agent Registry<br/>packages/registry]
    end

    subgraph entry [Entry points]
        USER[User]
        MCPCLIENT[Cursor / MCP client]
    end

    subgraph coordination [LangGraph coordination]
        LG[build_landed_graph]
        GO[graph_orchestrator_node]
        AO[adk_orchestrator_node]
        STATE[LandedGraphState]
    end

    subgraph execution [ADK execution]
        RUN[adk_runner.py]
        ORCH[landed_orchestrator]
        PS[product_search]
        AE[audio_expert]
        PR[pricing]
        IC[import_cost]
        DA[deal_advisor]
        REC[recommendation]
    end

    subgraph exposure [External exposure]
        MCP[landed-domain-mcp]
    end

    subgraph capabilities [Shared capabilities]
        TOOLS[packages/tools]
        API[Landed API / mock :3001]
        RAG[RAG + grounding]
    end

    REG --> LG
    REG --> ORCH
    REG --> MCP
    REG --> TOOLS

    USER --> LG
    LG --> GO --> STATE
    GO --> AO --> RUN --> ORCH
    MCPCLIENT --> MCP

    ORCH --> PS
    ORCH --> AE
    ORCH --> PR
    ORCH --> IC
    ORCH --> DA
    ORCH --> REC

    PS --> TOOLS
    AE --> TOOLS
    PR --> TOOLS
    IC --> TOOLS
    DA --> TOOLS
    REC --> TOOLS
    MCP --> TOOLS

    TOOLS --> API
    TOOLS --> RAG
    AO --> STATE
    AO --> USER
```

## 2. Default graph (`use_adk=True`)

Production path inside LangGraph.

```mermaid
flowchart LR
    START((START)) --> GO[graph_orchestrator_node]
    GO --> AO[adk_orchestrator_node]
    AO --> RUN[adk_runner.py<br/>InMemoryRunner]
    RUN --> ORCH[landed_orchestrator]
    ORCH --> AGENTS[6 specialist agents<br/>via AgentTool]
    AGENTS --> TOOLS[5 shared tools]
    TOOLS --> BACKENDS[Landed API mock + RAG]
    AO --> ENDNODE((END))
```

## 3. Lab graph (`use_adk=False`)

Grounding validation without ADK runtime.

```mermaid
flowchart LR
    START((START)) --> GO[graph_orchestrator_node]
    GO --> KN[knowledge_node]
    KN --> RK[retrieve_knowledge]
    RK --> RAG[RAG + grounding]
    KN --> RN[recommendation_node]
    RN --> ENDNODE((END))
```

## 4. ADK specialist topology

```mermaid
flowchart TB
    ORCH[landed_orchestrator]

    ORCH -->|AgentTool| PS[product_search]
    ORCH -->|AgentTool| AE[audio_expert]
    ORCH -->|AgentTool| PR[pricing]
    ORCH -->|AgentTool| IC[import_cost]
    ORCH -->|AgentTool| DA[deal_advisor]
    ORCH -->|AgentTool| REC[recommendation]

    PS --> T1[search_products]
    PS --> T2[get_product_details]
    AE --> T5[retrieve_knowledge]
    PR --> T3[get_local_price]
    IC --> T4[calculate_import_cost]
    DA --> T3
    DA --> T4
    DA --> T5
    REC --> T5

    T1 --> API[Landed API / mock]
    T2 --> API
    T3 --> API
    T4 --> API
    T5 --> RAG[RAG + grounding]
```

## 5. Default end-to-end sequence

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant G as LangGraph
    participant GO as graph_orchestrator_node
    participant AO as adk_orchestrator_node
    participant R as adk_runner
    participant O as landed_orchestrator
    participant PS as product_search
    participant API as Landed API mock
    participant ST as LandedGraphState

    U->>G: invoke(user_message)
    G->>GO: session + routing
    GO->>ST: messages, constraints

    G->>AO: run ADK path
    AO->>R: run_adk_orchestrator()
    R->>O: InMemoryRunner.run_async()
    O->>PS: AgentTool
    PS->>API: search_products
    API-->>PS: ToolResponse
    PS-->>O: specialist result
    O-->>R: final text
    R-->>AO: final_answer
    AO->>ST: orchestrator_output
    G-->>U: final_answer
```

## 6. MCP tool ecosystem

```mermaid
flowchart TB
    MCPCLIENT[Cursor / MCP client] --> MCP[landed-domain-mcp]

    MCP --> MK1[retrieve_landed_knowledge]
    MCP --> MK2[search_landed_products]
    MCP --> MK3[get_landed_product_details]
    MCP --> MK4[get_landed_local_price]
    MCP --> MK5[calculate_landed_import_cost]

    MK1 --> T5[retrieve_knowledge]
    MK2 --> T1[search_products]
    MK3 --> T2[get_product_details]
    MK4 --> T3[get_local_price]
    MK5 --> T4[calculate_import_cost]

    T1 --> API[Landed API / mock]
    T2 --> API
    T3 --> API
    T4 --> API
    T5 --> RAG[RAG + grounding]
```

## 7. Local development stack

```mermaid
flowchart LR
    DEV[Developer] --> APP[LangGraph / ADK / MCP]

    subgraph local [Local services]
        MOCK[scripts/landed_api_mock.py<br/>localhost:3001]
        OLL[Ollama<br/>localhost:11434]
        CHR[(Chroma index)]
    end

    APP --> MOCK
    APP --> OLL
    APP --> CHR

    MOCK --> TAPI[product + pricing + import tools]
    OLL --> TAGENTS[agent LLM when LLM_RUNTIME=local]
    OLL --> TRAG[embeddings + grounding]
    CHR --> TRAG
```

## 8. Knowledge layer: RAG + grounding

```mermaid
flowchart TD
    Q[retrieve_knowledge] --> TOOL[retrieve_knowledge_tool]
    TOOL --> SEARCH[search_knowledge]

    SEARCH --> SEM[Chroma + nomic-embed-text]
    SEM -->|distance <= 0.45| HIT1[semantic hit]
    SEM -->|fallback| LEX[local_lexical]
    LEX -->|score >= 0.35| HIT2[lexical hit]
    LEX -->|no match| MISS[no evidence]

    HIT1 --> GROUND[grounding_service]
    HIT2 --> GROUND
    MISS --> NOANS[refusal answer]
    GROUND --> LLM[Ollama llama3.1]
    LLM --> GA[grounded_answer + sources]
```

## 9. LLM runtime profiles

```mermaid
flowchart LR
    ENV[.env LLM_RUNTIME] --> RESOLVE[resolve_agent_model]
    ENV -->|local| LOCAL[LiteLLM ollama_chat/llama3.1]
    ENV -->|gcp| GCP[Gemini gemini-2.5-flash-lite]
    RESOLVE --> ADK[ADK agents]

    subgraph always_local [Always local today]
        EMB[nomic-embed-text]
        GR[llama3.1 grounding]
    end

    RAG[RAG layer] --> EMB
    RAG --> GR
```

## 10. Package map

```mermaid
flowchart TB
    subgraph packages [packages/]
        REG[registry/<br/>tool + agent contracts]
        GRAPHS[graphs/<br/>state, nodes, adk_runner]
        AGENTS[agents/<br/>orchestrator + specialists]
        MCP[mcp/<br/>landed-domain-mcp]
        TOOLS[tools/<br/>product, pricing, knowledge]
        KB[knowledge_base/]
        RAG[rag/]
        SHARED[shared/]
    end

    subgraph scripts [scripts/]
        MOCK[landed_api_mock.py]
        ADKDEV[run_adk_agent.py]
    end

    REG --> AGENTS
    REG --> MCP
    REG --> TOOLS
    GRAPHS --> AGENTS
    GRAPHS --> TOOLS
    AGENTS --> TOOLS
    MCP --> TOOLS
    TOOLS --> RAG
    TOOLS --> MOCK
    RAG --> KB
    GRAPHS --> SHARED
    AGENTS --> SHARED
    MCP --> SHARED
    REG --> SHARED
```

## 11. System-level registry

```mermaid
flowchart LR
    subgraph registry [packages/registry]
        TR[tool_registry.py]
        AR[agent_registry.py]
        PERM[permissions.py]
        BOOT[bootstrap.py]
    end

    subgraph checks [Validated at startup / tests]
        ADKCHK[ADK specialist tools]
        MCPCHK[MCP exposed tools]
        SYNCCHK[tool ↔ agent consistency]
    end

    TR --> PERM
    AR --> PERM
    TR --> BOOT
    AR --> BOOT
    BOOT --> ADKCHK
    BOOT --> MCPCHK
    BOOT --> SYNCCHK
```

### Registry responsibilities

| Module | Declares |
|--------|----------|
| `tool_registry.py` | tool name, category, MCP name, allowed agents |
| `agent_registry.py` | agent role, runtime, A2A flag, allowed tools |
| `permissions.py` | `can_agent_use_tool`, `can_mcp_call_tool` |
| `bootstrap.py` | drift detection against live ADK and MCP code |

## Related docs

- [architecture.md](./architecture.md) — written architecture reference
- [evaluation.md](./evaluation.md) — evaluation notes
- [roadmap.md](./roadmap.md) — planned improvements

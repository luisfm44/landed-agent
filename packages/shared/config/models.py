import os
from typing import Any

from google.adk.models.lite_llm import LiteLlm

from packages.shared.config.settings import LLM_RUNTIME, OLLAMA_HOST

VALID_LLM_RUNTIMES = frozenset({"local", "gcp"})


def _ensure_ollama_env() -> None:
    os.environ.setdefault("OLLAMA_API_BASE", OLLAMA_HOST)


def resolve_agent_model(model_name: str) -> Any:
    """Resolve an ADK agent model for the active runtime.

    - local: Ollama through LiteLLM (`ollama_chat/<model>`)
    - gcp: Gemini model id string for native ADK integration
    """
    if LLM_RUNTIME not in VALID_LLM_RUNTIMES:
        raise ValueError(
            f"Invalid LLM_RUNTIME '{LLM_RUNTIME}'. Expected one of: local, gcp."
        )

    if LLM_RUNTIME == "local":
        _ensure_ollama_env()
        return LiteLlm(model=f"ollama_chat/{model_name}")

    return model_name

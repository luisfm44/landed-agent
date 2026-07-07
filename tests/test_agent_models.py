import pytest
from google.adk.models.lite_llm import LiteLlm

from packages.shared.config.models import resolve_agent_model


def test_resolve_agent_model_gcp():
    model = resolve_agent_model("gemini-2.5-flash-lite")
    assert model == "gemini-2.5-flash-lite"


def test_resolve_agent_model_local(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("LLM_RUNTIME", "local")
    monkeypatch.setattr(
        "packages.shared.config.models.LLM_RUNTIME",
        "local",
    )

    model = resolve_agent_model("llama3.1")

    assert isinstance(model, LiteLlm)

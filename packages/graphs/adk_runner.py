from __future__ import annotations

import asyncio
from typing import Any

from google.adk.runners import InMemoryRunner
from google.genai import types

from packages.agents.orchestrator.landed_orchestrator_agent import root_agent

APP_NAME = "landed-langgraph"
_runner: InMemoryRunner | None = None


def get_runner() -> InMemoryRunner:
    global _runner
    if _runner is None:
        _runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    return _runner


def extract_final_answer(events: list[Any]) -> str:
    """Return the last text response from the ADK root orchestrator."""
    final_chunks: list[str] = []

    for event in events:
        if getattr(event, "author", None) != "landed_orchestrator":
            continue

        content = getattr(event, "content", None)
        if not content or not content.parts:
            continue

        for part in content.parts:
            text = getattr(part, "text", None)
            if text:
                final_chunks.append(text.strip())

    return final_chunks[-1] if final_chunks else ""


async def _ensure_session(user_id: str, session_id: str) -> None:
    runner = get_runner()
    existing = await runner.session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if existing is None:
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )


async def _run_adk_orchestrator_async(
    *,
    user_id: str,
    session_id: str,
    user_message: str,
) -> dict[str, Any]:
    runner = get_runner()
    await _ensure_session(user_id=user_id, session_id=session_id)

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    events: list[Any] = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        events.append(event)

    final_answer = extract_final_answer(events)
    authors = sorted({getattr(event, "author", None) for event in events if getattr(event, "author", None)})

    return {
        "final_answer": final_answer,
        "events_count": len(events),
        "authors": authors,
        "agent": root_agent.name,
    }


def run_adk_orchestrator(
    *,
    user_id: str,
    session_id: str,
    user_message: str,
) -> dict[str, Any]:
    """Invoke the ADK business orchestrator from a LangGraph node."""
    return asyncio.run(
        _run_adk_orchestrator_async(
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
        )
    )

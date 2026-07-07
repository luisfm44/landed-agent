from typing import Any, Required, TypedDict


class LandedGraphState(TypedDict, total=False):
    # Identity / session
    session_id: str
    user_id: str

    # Conversation / working memory
    user_message: Required[str]
    messages: list[dict[str, str]]

    # Intent and task state
    current_intent: str | None
    product_type: str | None
    use_cases: list[str]
    budget: float | None
    country: str
    constraints: dict[str, Any]

    # Knowledge / grounding
    knowledge_result: dict[str, Any] | None
    grounded: bool
    grounded_answer: str | None
    sources: list[dict[str, Any]]

    # Agent outputs
    orchestrator_output: dict[str, Any] | None
    audio_expert_output: dict[str, Any] | None
    recommendation_output: dict[str, Any] | None
    deal_advisor_output: dict[str, Any] | None

    # Final answer
    final_answer: str | None


def require_user_message(state: LandedGraphState) -> str:
    user_message = state.get("user_message")
    if not user_message:
        raise ValueError("LandedGraphState requires user_message")
    return user_message

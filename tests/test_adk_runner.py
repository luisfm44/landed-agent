from types import SimpleNamespace

from packages.graphs.adk_runner import extract_final_answer


def test_extract_final_answer_returns_last_orchestrator_text():
    events = [
        SimpleNamespace(
            author="landed_orchestrator",
            content=SimpleNamespace(
                parts=[SimpleNamespace(text="Working on it...", function_call=None)]
            ),
        ),
        SimpleNamespace(
            author="pricing",
            content=SimpleNamespace(parts=[SimpleNamespace(text="ignored")]),
        ),
        SimpleNamespace(
            author="landed_orchestrator",
            content=SimpleNamespace(
                parts=[SimpleNamespace(text="Final recommendation for DT 770 Pro.")]
            ),
        ),
    ]

    assert extract_final_answer(events) == "Final recommendation for DT 770 Pro."

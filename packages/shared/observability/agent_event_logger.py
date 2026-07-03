from packages.shared.logging import get_logger, log_agent_event

logger = get_logger("landed.agent_events")


def record_agent_event(event: str, trace_id: str | None = None, **fields: object) -> None:
    log_agent_event(logger, event, trace_id, **fields)

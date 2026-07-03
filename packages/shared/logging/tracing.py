import logging
from uuid import uuid4


def new_trace_id() -> str:
    return str(uuid4())


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s trace_id=%(trace_id)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def log_agent_event(
    logger: logging.Logger,
    event: str,
    trace_id: str | None = None,
    **fields: object,
) -> None:
    payload = " ".join(f"{key}={value}" for key, value in fields.items())
    logger.info("%s %s", event, payload, extra={"trace_id": trace_id or "-"})

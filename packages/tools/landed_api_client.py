import requests

from packages.shared.config import (
    LANDED_API_BACKOFF_SECONDS,
    LANDED_API_BASE_URL,
    LANDED_API_MAX_RETRIES,
    LANDED_API_TIMEOUT_SECONDS,
)
from packages.shared.guardrails import with_exponential_backoff
from packages.shared.logging import get_logger, log_agent_event, new_trace_id

logger = get_logger(__name__)


def call_landed_api(path: str, params: dict | None = None) -> dict:
    trace_id = new_trace_id()

    def request() -> requests.Response:
        return requests.get(
            f"{LANDED_API_BASE_URL}{path}",
            params=params or {},
            timeout=LANDED_API_TIMEOUT_SECONDS,
        )

    try:
        log_agent_event(logger, "landed_api.request", trace_id, path=path)
        response = with_exponential_backoff(
            request,
            max_retries=LANDED_API_MAX_RETRIES,
            base_delay_seconds=LANDED_API_BACKOFF_SECONDS,
            retryable_exceptions=(
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ),
        )
        response.raise_for_status()
        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": response.json(),
        }
    except requests.exceptions.Timeout:
        return {
            "ok": False,
            "trace_id": trace_id,
            "error": "LANDED_TIMEOUT",
            "message": "Landed backend took too long to respond.",
        }
    except requests.exceptions.RequestException as error:
        return {
            "ok": False,
            "trace_id": trace_id,
            "error": "LANDED_API_ERROR",
            "message": str(error),
        }

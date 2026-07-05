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


def call_landed_api(
    path: str,
    params: dict | None = None,
    trace_id: str | None = None,
) -> dict:
    """Call the Landed backend API with timeout, retries, tracing, and normalized errors."""

    trace_id = trace_id or new_trace_id()
    normalized_path = path if path.startswith("/") else f"/{path}"
    url = f"{LANDED_API_BASE_URL}{normalized_path}"

    def request() -> requests.Response:
        return requests.get(
            url,
            params=params or {},
            timeout=LANDED_API_TIMEOUT_SECONDS,
        )

    try:
        log_agent_event(
            logger,
            "landed_api.request",
            trace_id,
            path=normalized_path,
            params=params or {},
        )

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

        try:
            payload = response.json()
        except ValueError:
            log_agent_event(
                logger,
                "landed_api.invalid_json",
                trace_id,
                path=normalized_path,
                status_code=response.status_code,
            )

            return {
                "ok": False,
                "trace_id": trace_id,
                "source": "landed_api",
                "error": "LANDED_INVALID_JSON",
                "message": "Landed backend returned a non-JSON response.",
            }

        log_agent_event(
            logger,
            "landed_api.success",
            trace_id,
            path=normalized_path,
            status_code=response.status_code,
        )

        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": payload,
        }

    except requests.exceptions.Timeout:
        log_agent_event(
            logger,
            "landed_api.timeout",
            trace_id,
            path=normalized_path,
        )

        return {
            "ok": False,
            "trace_id": trace_id,
            "source": "landed_api",
            "error": "LANDED_TIMEOUT",
            "message": "Landed backend took too long to respond.",
        }

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code if error.response is not None else None

        log_agent_event(
            logger,
            "landed_api.http_error",
            trace_id,
            path=normalized_path,
            status_code=status_code,
            message=str(error),
        )

        return {
            "ok": False,
            "trace_id": trace_id,
            "source": "landed_api",
            "error": "LANDED_HTTP_ERROR",
            "message": str(error),
            "status_code": status_code,
        }

    except requests.exceptions.RequestException as error:
        log_agent_event(
            logger,
            "landed_api.request_error",
            trace_id,
            path=normalized_path,
            message=str(error),
        )

        return {
            "ok": False,
            "trace_id": trace_id,
            "source": "landed_api",
            "error": "LANDED_API_ERROR",
            "message": str(error),
        }
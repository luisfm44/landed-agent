import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def with_exponential_backoff(
    operation: Callable[[], T],
    *,
    max_retries: int,
    base_delay_seconds: float,
    retryable_exceptions: tuple[type[Exception], ...],
) -> T:
    attempt = 0
    while True:
        try:
            return operation()
        except retryable_exceptions:
            if attempt >= max_retries:
                raise
            time.sleep(base_delay_seconds * (2**attempt))
            attempt += 1

from collections import Counter

_COUNTERS: Counter[str] = Counter()


def increment_metric(name: str, value: int = 1) -> None:
    _COUNTERS[name] += value


def get_metric(name: str) -> int:
    return _COUNTERS[name]

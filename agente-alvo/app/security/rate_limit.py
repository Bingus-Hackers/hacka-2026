import time
from collections import defaultdict

_WINDOW_SEC = 60
_MAX_REQUESTS = 30

_buckets: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(client_key: str) -> tuple[bool, str | None]:
    now = time.time()
    window_start = now - _WINDOW_SEC
    hits = [t for t in _buckets[client_key] if t > window_start]
    if len(hits) >= _MAX_REQUESTS:
        return False, "Rate limit excedido. Tente novamente em instantes."
    hits.append(now)
    _buckets[client_key] = hits
    return True, None

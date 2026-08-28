from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    "ledgercore_requests_total", "Total requests", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram(
    "ledgercore_request_latency_seconds", "Request latency", ["path"]
)
RATE_LIMITED_COUNT = Counter(
    "ledgercore_rate_limited_total", "Requests rejected by rate limiter"
)
CIRCUIT_STATE = Gauge(
    "ledgercore_circuit_breaker_state", "0=closed, 1=open, 2=half_open"
)
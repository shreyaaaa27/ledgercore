import httpx
from app.circuit_breaker import CircuitBreaker


BACKEND_URL = "http://backend-a:9000"
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10.0)


async def _do_request(path: str, method: str, body: bytes = None):
    async with httpx.AsyncClient() as client:
        return await client.request(method=method, url=f"{BACKEND_URL}/{path}", content=body, timeout=5.0)


async def forward_request(path: str, method: str, body: bytes = None):
    return await breaker.call(_do_request, path, method, body)
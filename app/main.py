import os
import time
import redis

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.gateway import forward_request
from app.metrics import RATE_LIMITED_COUNT, REQUEST_COUNT, REQUEST_LATENCY
from app.redis_bucket import RedisTokenBucket

app = FastAPI(title="LedgerCore")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

# Config: 10 requests burst, refills at 2 tokens/sec
bucket = RedisTokenBucket(redis_client, max_tokens=10, refill_rate=2)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.client.host if request.client else "unknown"
    start = time.monotonic()

    if not bucket.allow_request(client_id):
        RATE_LIMITED_COUNT.inc()
        REQUEST_COUNT.labels(request.method, request.url.path, "429").inc()
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded."})

    response = await call_next(request)
    duration = time.monotonic() - start

    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()

    return response


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_route(path: str, request: Request):
    body = await request.body()
    resp = await forward_request(path, request.method, body)
    return Response(content=resp.content, status_code=resp.status_code)
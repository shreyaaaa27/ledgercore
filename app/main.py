from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis
from app.gateway import forward_request
from fastapi.responses import Response
import os

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
    client_id = request.client.host  # IP-based for now

    if not bucket.allow_request(client_id):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again shortly."},
        )

    response = await call_next(request)
    return response


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_route(path: str, request: Request):
    body = await request.body()
    resp = await forward_request(path, request.method, body)
    return Response(content=resp.content, status_code=resp.status_code)
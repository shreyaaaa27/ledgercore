from fastapi.testclient import TestClient
from app.main import app, redis_client

client = TestClient(app)


def test_rate_limit_blocks_after_burst():
    redis_client.flushdb()
    responses = [client.get("/ping").status_code for _ in range(15)]
    assert 429 in responses
    assert responses.count(200) <= 10
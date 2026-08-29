import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app, redis_client


@pytest.mark.asyncio(loop_scope="session")
async def test_rate_limit_blocks_after_burst():
    await redis_client.flushdb()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        responses = [(await client.get("/ping")).status_code for _ in range(15)]

    assert 429 in responses
    assert responses.count(200) <= 10
import asyncio
import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from app.redis_bucket import RedisTokenBucket


# Use pytest_asyncio.fixture for async setup/teardown
@pytest_asyncio.fixture
async def redis_client():
    client = aioredis.Redis(host="redis", port=6379, decode_responses=True)
    yield client
    await client.flushdb()  # clean state between tests
    await client.aclose()


@pytest.mark.asyncio
async def test_allows_up_to_max_tokens(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=3, refill_rate=0)
    assert await bucket.allow_request("clientA") is True
    assert await bucket.allow_request("clientA") is True
    assert await bucket.allow_request("clientA") is True
    assert await bucket.allow_request("clientA") is False


@pytest.mark.asyncio
async def test_separate_clients_have_separate_buckets(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=1, refill_rate=0)
    assert await bucket.allow_request("clientA") is True
    assert await bucket.allow_request("clientB") is True  # different client, own bucket


@pytest.mark.asyncio
async def test_refills_over_time(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=1, refill_rate=10)
    assert await bucket.allow_request("clientC") is True
    assert await bucket.allow_request("clientC") is False
    
    # Non-blocking sleep for async tests
    await asyncio.sleep(0.2)
    
    assert await bucket.allow_request("clientC") is True
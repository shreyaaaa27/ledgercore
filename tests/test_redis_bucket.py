import time
import redis
import pytest
from app.redis_bucket import RedisTokenBucket


@pytest.fixture
def redis_client():
    client = redis.Redis(host="redis", port=6379, decode_responses=True)
    yield client
    client.flushdb()  # clean state between tests


def test_allows_up_to_max_tokens(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=3, refill_rate=0)
    assert bucket.allow_request("clientA") is True
    assert bucket.allow_request("clientA") is True
    assert bucket.allow_request("clientA") is True
    assert bucket.allow_request("clientA") is False


def test_separate_clients_have_separate_buckets(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=1, refill_rate=0)
    assert bucket.allow_request("clientA") is True
    assert bucket.allow_request("clientB") is True  # different client, own bucket


def test_refills_over_time(redis_client):
    bucket = RedisTokenBucket(redis_client, max_tokens=1, refill_rate=10)
    assert bucket.allow_request("clientC") is True
    assert bucket.allow_request("clientC") is False
    time.sleep(0.2)
    assert bucket.allow_request("clientC") is True
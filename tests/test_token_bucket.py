import time
from app.token_bucket import TokenBucket


def test_starts_full():
    bucket = TokenBucket(max_tokens=5, refill_rate=1)
    assert bucket.allow_request() is True


def test_exhausts_after_max_requests():
    bucket = TokenBucket(max_tokens=3, refill_rate=0)  # no refill
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is False  # 4th request should fail


def test_refills_over_time():
    bucket = TokenBucket(max_tokens=1, refill_rate=10)  # fast refill for testing
    assert bucket.allow_request() is True
    assert bucket.allow_request() is False  # no tokens left
    time.sleep(0.2)  # 0.2s * 10/s = 2 tokens worth, capped at max=1
    assert bucket.allow_request() is True  # refilled
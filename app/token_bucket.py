# app/token_bucket.py
import time


class TokenBucket:
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.tokens = max_tokens
        self.last_refill_time = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill_time
        refill_amount = elapsed * self.refill_rate
        self.tokens = min(self.max_tokens, self.tokens + refill_amount)
        self.last_refill_time = now

    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
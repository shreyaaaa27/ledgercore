import time
import redis
import os

LUA_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "token_bucket.lua")


class RedisTokenBucket:
    def __init__(self, redis_client: redis.Redis, max_tokens: int, refill_rate: float):
        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        with open(LUA_SCRIPT_PATH, "r") as f:
            script_body = f.read()
        self.script = self.redis.register_script(script_body)

    def allow_request(self, client_id: str) -> bool:
        key = f"bucket:{client_id}"
        now = time.time()
        result = self.script(
            keys=[key],
            args=[self.max_tokens, self.refill_rate, now],
        )
        return bool(result)
from app.token_bucket import TokenBucket


class BucketManager:
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.buckets: dict[str, TokenBucket] = {}

    def get_bucket(self, client_id: str) -> TokenBucket:
        if client_id not in self.buckets:
            self.buckets[client_id] = TokenBucket(self.max_tokens, self.refill_rate)
        return self.buckets[client_id]

    def allow_request(self, client_id: str) -> bool:
        return self.get_bucket(client_id).allow_request()
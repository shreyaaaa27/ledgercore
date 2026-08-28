import time
from enum import Enum


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = State.CLOSED
        self.last_failure_time = None

    def _can_attempt(self) -> bool:
        if self.state == State.CLOSED:
            return True
        if self.state == State.OPEN:
            if time.monotonic() - self.last_failure_time >= self.recovery_timeout:
                self.state = State.HALF_OPEN
                return True
            return False
        if self.state == State.HALF_OPEN:
            return True
        return False

    def record_success(self):
        self.failure_count = 0
        self.state = State.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.monotonic()
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN

    async def call(self, func, *args, **kwargs):
        if not self._can_attempt():
            raise Exception("Circuit is open — backend unavailable")
        try:
            result = await func(*args, **kwargs)
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            raise
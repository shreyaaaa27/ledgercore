import time
import pytest
from app.circuit_breaker import CircuitBreaker, State


@pytest.mark.asyncio
async def test_opens_after_threshold_failures():
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)

    async def failing():
        raise Exception("boom")

    for _ in range(2):
        with pytest.raises(Exception):
            await breaker.call(failing)

    assert breaker.state == State.OPEN

    with pytest.raises(Exception, match="Circuit is open"):
        await breaker.call(failing)


@pytest.mark.asyncio
async def test_half_open_recovers_on_success():
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)

    async def failing():
        raise Exception("boom")

    async def succeeding():
        return "ok"

    with pytest.raises(Exception):
        await breaker.call(failing)
    assert breaker.state == State.OPEN

    time.sleep(0.15)
    result = await breaker.call(succeeding)
    assert result == "ok"
    assert breaker.state == State.CLOSED
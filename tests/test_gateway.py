import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app, redis_client


@pytest.mark.asyncio(loop_scope="session")
@patch("app.main.forward_request", new_callable=AsyncMock)
async def test_gateway_forwards_request(mock_forward):
    await redis_client.flushdb()
    mock_forward.return_value.content = b"hello from backend"
    mock_forward.return_value.status_code = 200

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/test")

    assert response.status_code == 200
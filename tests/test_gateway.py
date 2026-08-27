from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app, redis_client

client = TestClient(app)


@patch("app.main.forward_request", new_callable=AsyncMock)
def test_gateway_forwards_request(mock_forward):
    redis_client.flushdb()
    mock_forward.return_value.content = b"hello from backend"
    mock_forward.return_value.status_code = 200

    response = client.get("/api/test")
    assert response.status_code == 200
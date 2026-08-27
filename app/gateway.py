import httpx

BACKEND_URL = "http://backend-a:9000"


async def forward_request(path: str, method: str, body: bytes = None):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=f"{BACKEND_URL}/{path}",
            content=body,
            timeout=5.0,
        )
    return response
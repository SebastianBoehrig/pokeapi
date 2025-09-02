import httpx
import pytest

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client
import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_rate_limit_adds_headers(client):
    settings.RATE_LIMIT_ENABLED = True

    response = await client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.headers["X-RateLimit-Limit"] == "500"
    assert response.headers["X-RateLimit-Remaining"] == "499"

    settings.RATE_LIMIT_ENABLED = False


@pytest.mark.asyncio
async def test_rate_limit_blocks_after_limit_exceeded(client):
    settings.RATE_LIMIT_ENABLED = True

    response = None

    for _ in range(501):
        response = await client.post(
            "/auth/login",
            data={
                "username": "wrong@example.com",
                "password": "wrongpassword"
            }
        )

    assert response.status_code == 429

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Too many requests. Please try again later."
    assert "retry_after_seconds" in data
    assert "Retry-After" in response.headers

    settings.RATE_LIMIT_ENABLED = False


@pytest.mark.asyncio
async def test_rate_limit_skips_when_disabled(client):
    settings.RATE_LIMIT_ENABLED = False

    response = await client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert "X-RateLimit-Limit" not in response.headers


@pytest.mark.asyncio
async def test_rate_limit_skips_unknown_path(client):
    settings.RATE_LIMIT_ENABLED = True

    response = await client.get("/unknown-path")

    assert response.status_code == 404
    assert "X-RateLimit-Limit" not in response.headers

    settings.RATE_LIMIT_ENABLED = False
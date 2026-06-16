import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from asgi_lifespan import LifespanManager

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

from app.models.user import User
from app.models.refresh_token import RefreshToken


TEST_DATABASE_URL = settings.TEST_DATABASE_URL


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    app.dependency_overrides[get_db] = override_get_db

    async with LifespanManager(app):
        redis = getattr(app.state, "redis", None)

        if redis:
            await redis.flushdb()

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac

    app.dependency_overrides.clear()
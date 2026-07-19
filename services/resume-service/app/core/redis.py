from arq.connections import ArqRedis, RedisSettings, create_pool

from app.core.config import settings


redis_client: ArqRedis | None = None


async def init_redis_client() -> ArqRedis:
    global redis_client

    if redis_client is None:
        redis_client = await create_pool(
            RedisSettings.from_dsn(settings.REDIS_URL)
        )

        await redis_client.ping()

    return redis_client


def get_redis_client() -> ArqRedis:
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized.")

    return redis_client


async def close_redis_client() -> None:
    global redis_client

    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None

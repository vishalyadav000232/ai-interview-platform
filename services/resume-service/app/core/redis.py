from redis.asyncio import Redis
from app.core.config import settings



async def create_redis_client()-> Redis:
    return Redis.from_url(
        url=settings.REDIS_URL,
         decode_responses=True,
        max_connections=20,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )
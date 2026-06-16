from app.core.redis import redis_client
from fastapi import Request
from redis.asyncio import Redis

async def get_redis(request : Request)-> Redis:
    return request.app.state.redis


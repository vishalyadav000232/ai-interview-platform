from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

import logging

from app.core.config import settings
from redis.asyncio import Redis


logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app=app)

        self.default_limit = 100
        self.default_window_second = 60

    async def dispatch(self, request: Request, call_next):

        if settings.RATE_LIMIT_ENABLED is False:
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        redis: Redis | None = getattr(request.app.state, "redis", None)

        if redis is None:
            logger.warning("Redis not found. Skipping gateway rate limit")
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        key = f"gateway_rate_limit:{client_ip}:{path}"

        try:
            current_count = await redis.incr(key)

            if current_count == 1:
                await redis.expire(
                    key,
                    self.default_window_second
                )

            if current_count > self.default_limit:
                ttl = await redis.ttl(key)

                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "message": "Too many requests. Please try again later.",
                        "retry_after_seconds": ttl,
                    },
                    headers={
                        "Retry-After": str(ttl)
                    }
                )

            response = await call_next(request)

            response.headers["X-RateLimit-Limit"] = str(self.default_limit)
            response.headers["X-RateLimit-Remaining"] = str(
                max(0, self.default_limit - current_count)
            )

            return response

        except Exception:
            logger.exception("Gateway rate limiter failed")
            return await call_next(request)

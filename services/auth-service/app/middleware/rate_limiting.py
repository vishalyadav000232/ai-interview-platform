import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

        self.rules = {
            "/auth/login": {
                "limit": 500,
                "window_seconds": 60,
            },
            "/auth/register": {
                "limit": 300,
                "window_seconds": 60,
            },
            "/auth/forgot-password": {
                "limit": 300,
                "window_seconds": 300,
            },
            "/auth/me": {
                "limit": 300,
                "window_seconds": 300,
            },
        }

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path not in self.rules:
            return await call_next(request)

        redis : Redis = getattr(request.app.state , "redis" , None)
        
        if redis is None:
            return call_next(request)
        
        client_ip = request.client.host

        rule = self.rules[path]

        key = f"rate_limit:{path}:{client_ip}"

        try:
            current_count = await redis.incr(key)

            if current_count == 1:
                await redis.expire(
                    key,
                    rule["window_seconds"]
                )

                logger.info(
                    "Rate limit window started",
                    extra={
                        "path": path,
                        "client_ip": client_ip,
                        "limit": rule["limit"],
                        "window_seconds": rule["window_seconds"]
                    }
                )

            logger.debug(
                "Rate limit counter incremented",
                extra={
                    "path": path,
                    "client_ip": client_ip,
                    "current_count": current_count,
                    "limit": rule["limit"]
                }
            )

            if current_count > rule["limit"]:

                ttl = await redis.ttl(key)

                logger.warning(
                    "Rate limit exceeded",
                    extra={
                        "path": path,
                        "client_ip": client_ip,
                        "current_count": current_count,
                        "limit": rule["limit"],
                        "retry_after_seconds": ttl
                    }
                )

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

            response.headers["X-RateLimit-Limit"] = str(
                rule["limit"]
            )

            response.headers["X-RateLimit-Remaining"] = str(
                max(
                    0,
                    rule["limit"] - current_count
                )
            )

            return response

        except Exception:
            logger.exception(
                "Rate limiter failed",
                extra={
                    "path": path,
                    "client_ip": client_ip
                }
            )

            return await call_next(request)
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.apis.route import router as main_router
from app.core.config import settings
from app.core.exceptions.exception_builder import register_exception_handlers
from app.core.logging import setup_logging
from app.core.redis import (
    close_redis_client,
    init_redis_client,
)
from app.database.session import AsyncLoaclSession, engine


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Resume Service")

    try:

        redis = await init_redis_client()


        await redis.ping()


        app.state.redis = redis

        logger.info("Redis connected successfully")


        async with AsyncLoaclSession() as session:
            await session.execute(text("SELECT 1"))

        logger.info("Database connected successfully")
        logger.info("Resume Service started successfully")

        
        yield

    except Exception:
        logger.exception("Resume Service lifecycle failed")
        raise

    finally:
        logger.info("Shutting down Resume Service")

        await close_redis_client()
        logger.info("Redis connection closed")

        await engine.dispose()
        logger.info("Database connection disposed successfully")

        logger.info("Resume Service shutdown completed")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "message": "Resume Service is running",
    }


@app.get("/health")
async def health():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "status": "healthy",
    }


app.include_router(main_router)

register_exception_handlers(app=app)

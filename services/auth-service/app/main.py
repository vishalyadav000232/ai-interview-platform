import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import api_router
from app.core.logging import setup_logging
from app.core.exception_handler import register_exception_handlers
from app.db.session import engine, AsyncSessionLocal
from app.core.redis import create_redis_client


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Auth Service")

    try:
        
        app.state.redis = create_redis_client()
        await app.state.redis.ping()
        logger.info("Redis connected successfully")


        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        logger.info("Database connected successfully")
        logger.info("Auth Service started successfully")

        yield

    except Exception:
        logger.exception("Auth Service startup failed")
        raise

    finally:
        logger.info("Shutting down Auth Service")

        redis = getattr(app.state, "redis", None)

        if redis:
            await redis.aclose()
            logger.info("Redis connection closed successfully")

        await engine.dispose()
        logger.info("Database engine disposed successfully")


app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "success": True,
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "healthy",
    }
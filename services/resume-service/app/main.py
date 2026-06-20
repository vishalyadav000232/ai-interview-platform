import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.logging import setup_logging
from app.core.redis import create_redis_client
from app.core.config import settings
from app.database.session import AsyncLoaclSession , engine
from sqlalchemy import text


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Resume Service")

    redis = None

    try:
        redis = await create_redis_client()
        await redis.ping()

        app.state.redis = redis

        logger.info("Redis connected successfully")
        
        async with AsyncLoaclSession() as session:
            await session.execute(text("SELECT 1"))
            
        logger.info("Database connected Successfullu ")
        
        
        logger.info("Resume Service started successfully")

    except Exception as e:
        logger.exception(f"Resume Service startup failed: {e}")
        raise

    yield

    logger.info("Shutting down Resume Service")

    if redis:
        await redis.aclose()
        logger.info("Redis connection closed")
        
    engine.dispose()
    
    logger.info("Database connection dispose successfully ")


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


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"Unhandled error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
        },
    )
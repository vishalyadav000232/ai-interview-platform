import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exception_handler import register_exception_handlers
from app.db.session import engine, AsyncSessionLocal


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Auth Service")

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        logger.info("Database connected successfully")

    except Exception:
        logger.exception("Database connection failed")
        raise

    logger.info("Auth Service started successfully")

    yield

    logger.info("Shutting down Auth Service")

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


# CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "success": True,
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "healthy",
    }
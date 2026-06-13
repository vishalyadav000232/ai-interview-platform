import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exception_handler import register_exception_handlers

# Configure Logging
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup Events
    """

    logger.info("Starting Auth Service")

    # Database Connection Check
    # Redis Connection Check
    # Kafka Connection Check
    # Background Workers Start

    yield

    """
    Shutdown Events
    """

    logger.info("Shutting down Auth Service")

    # Close DB Pool
    # Close Redis
    # Stop Workers


app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global Exception Handlers
register_exception_handlers(app)

# CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# API Routes
app.include_router(api_router)


@app.get(
    "/health",
    tags=["Health"]
)
async def health_check():
    return {
        "success": True,
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "healthy"
    }
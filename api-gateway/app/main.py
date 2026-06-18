import logging 
from fastapi import FastAPI
from contextlib import asynccontextmanager

import httpx

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.loggging import setup_logging
from app.routes.routes import router as main_router
from app.middleware.requset_logging import RequestLoggingMiddleware


from app.core.exception import GatewayException
from app.core.exception_handler import gateway_exception_handler

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app : FastAPI):
    setup_logging()
    
    logger.info("API Gateway starting...")
    
    app.state.http_client =  httpx.AsyncClient(
        timeout=httpx.Timeout(10.0),
        follow_redirects=True
    )
    
    logger.info("HTTP client initialized")
    yield
    
    

    await app.state.http_client.aclose()
    
    logger.info("HTTP client closed")
    logger.info("API Gateway stopped")




app = FastAPI(
     title=settings.APP_NAME,
    version="1.0.0",
    description="API Gateway for AI Interview Platform",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)


app.include_router(main_router)

app.add_exception_handler(
    GatewayException,
    gateway_exception_handler
)
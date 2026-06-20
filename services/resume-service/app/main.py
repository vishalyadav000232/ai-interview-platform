import logging
from fastapi import FastAPI
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


async def lifespan(app : FastAPI)->FastAPI:
    
    logger.info("Starting Resume Serivces !")
    
    
    
    
    
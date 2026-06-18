from fastapi import APIRouter
from app.core.config import settings




router = APIRouter(prefix='/api-gateway' , tags=["API GATWAY"])



@router.get("health")
async def health():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "status": "healthy",
    }
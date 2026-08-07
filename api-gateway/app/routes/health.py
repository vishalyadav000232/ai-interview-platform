import httpx

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.core.config import settings


router = APIRouter(prefix="/api-gateway", tags=["API Gateway"])


@router.get("/health")
async def health():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "status": "healthy",
    }


@router.get("/health/live")
async def liveness_check():
    return {
        "success": True,
        "service": settings.APP_NAME,
        "status": "alive",
    }


@router.get("/health/ready")
async def readiness_check(request: Request):
    client: httpx.AsyncClient = request.app.state.http_client

    services = {
        "auth-service": "unknown"
    }

    try:
        response = await client.get(
            f"{settings.AUTH_SERVICE_URL}/health"
        )

        if response.status_code == 200:
            services["auth-service"] = "healthy"
        else:
            services["auth-service"] = "unhealthy"

    except httpx.TimeoutException:
        services["auth-service"] = "timeout"

    except httpx.RequestError:
        services["auth-service"] = "unavailable"

    is_ready = all(
        service_status == "healthy"
        for service_status in services.values()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "success": is_ready,
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "status": "ready" if is_ready else "not_ready",
            "dependencies": services,
        }
    )

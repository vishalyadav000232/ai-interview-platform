from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.auth_proxy import router as auth_proxy_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_proxy_router)
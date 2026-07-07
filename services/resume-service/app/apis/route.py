from fastapi import APIRouter

from app.apis.routes.resume_routes import router as resume_router


router = APIRouter(prefix="/resume" , tags=["Resume"])

router.include_router(resume_router)
from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/health/db")
async def database_health(
    db: AsyncSession = Depends(get_db)
):
    await db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected"
    }
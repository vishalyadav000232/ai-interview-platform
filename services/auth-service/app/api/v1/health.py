from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/db")
async def database_health(
    db: AsyncSession = Depends(get_db)
):
    await db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected"
    }

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.repository.refresh_token_repository import RefreshTokenRepository
from app.repository.user import UserRepository

async def get_refresh_repo(db : AsyncSession = Depends(get_db))->RefreshTokenRepository:
    return RefreshTokenRepository(db=db)

async def get_user_repo(db : AsyncSession = Depends(get_db))->UserRepository:
    return UserRepository(db=db)
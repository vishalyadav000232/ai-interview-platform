from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db


from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.resume import ResumeRepository
async def get_resume_repo(
    db : AsyncSession = Depends(get_db)
)-> ResumeRepositoryInterface:
    return ResumeRepository(db=db)
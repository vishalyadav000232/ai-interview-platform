from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession , async_sessionmaker
from collections.abc import AsyncGenerator

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
) 


async def get_db()-> AsyncGenerator[AsyncSession , None]:
    async with AsyncSessionLocal() as session :
        yield session
        
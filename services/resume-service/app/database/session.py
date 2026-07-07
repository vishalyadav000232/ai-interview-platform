from sqlalchemy.ext.asyncio import async_sessionmaker , create_async_engine , AsyncSession

from app.core.config import settings
from collections.abc import AsyncGenerator



engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    
)


AsyncLoaclSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    autocommit =  False
)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncLoaclSession() as session:
        try:
            yield session
        finally:
            await session.close()
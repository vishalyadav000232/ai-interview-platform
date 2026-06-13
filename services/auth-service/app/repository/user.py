import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import CreateUser
from app.repository.interface.user_repository_interface import UserRepositoryInterface


logger = logging.getLogger(__name__)


class UserRepository(UserRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: CreateUser) -> User:
        try:
            new_user = User(
                first_name=user.first_name,
                last_name = user.last_name,
                email=user.email,
                password_hash=user.password
            )

            self.db.add(new_user)

            await self.db.commit()
            await self.db.refresh(new_user)

            logger.info(
                "User created successfully",
                extra={
                    "user_id": str(new_user.id),
                    "email": new_user.email
                }
            )

            return new_user

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to create user",
                extra={"email": user.email}
            )

            raise

    async def get_by_id(self, user_id: UUID) -> User | None:
        try:
            stmt = select(User).where(User.id == user_id)

            result = await self.db.execute(stmt)

            return result.scalar_one_or_none()

        except Exception:
            logger.exception(
                "Failed to fetch user by id",
                extra={
                    "user_id": str(user_id)
                }
            )
            raise
    
    async def get_by_email(self, email: str) -> User | None:
        try:
            stmt = select(User).where(User.email == email)

            result = await self.db.execute(stmt)

            return result.scalar_one_or_none()

        except Exception:
            logger.exception(
                "Failed to fetch user by email",
                extra={
                    "email": str(email)
                }
            )
            raise
    
    async def update(self, user: User) -> User:
        try:
            self.db.add(user)

            await self.db.commit()
            await self.db.refresh(user)

            logger.info(
                "User updated successfully",
                extra={
                    "user_id": str(user.id),
                    "email": user.email
                }
            )

            return user

        except Exception:
            await self.db.rollback()

            logger.exception(
                "Failed to update user",
                extra={
                    "user_id": str(user.id) if user and user.id else None
                }
            )

            raise
    
    async def delete(self, user: User) -> None:
        try:
            await self.db.delete(user)
            await self.db.commit()

            logger.info(
                    "User deleted successfully",
                    extra={
                        "user_id": str(user.id),
                        "email": user.email
                    }
                )

        except Exception:
                await self.db.rollback()

                logger.exception(
                    "Failed to delete user",
                    extra={
                        "user_id": str(user.id) if user else None
                    }
                )

                raise
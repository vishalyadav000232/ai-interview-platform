import logging

from uuid import UUID

from app.models.user import User
from app.schemas.user import CreateUser
from app.core.security import SecurityService
from app.repository.interface.user_repository_interface import UserRepositoryInterface
from app.services.interface.user import UserServiceInterface

logger = logging.getLogger(__name__)


class UserService(UserServiceInterface):

    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def create_user(self, user: CreateUser) -> User:
        logger.info(
            "Creating new user",
            extra={"email": user.email}
        )

        existing_user = await self.user_repo.get_by_email(user.email)

        if existing_user:
            logger.warning(
                "User registration failed: email already exists",
                extra={"email": user.email}
            )
            raise ValueError("Email already registered")

        user.password = SecurityService.hash_password(user.password)

        created_user = await self.user_repo.create(user)

        logger.info(
            "User created successfully",
            extra={
                "user_id": str(created_user.id),
                "email": created_user.email
            }
        )

        return created_user

    async def get_user_by_id(self, user_id: UUID) -> User:
        logger.debug(
            "Fetching user by id",
            extra={"user_id": str(user_id)}
        )

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            logger.warning(
                "User not found",
                extra={"user_id": str(user_id)}
            )
            raise ValueError("User not found")

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        logger.debug(
            "Fetching user by email",
            extra={"email": email}
        )

        return await self.user_repo.get_by_email(email)

    async def update_user(self, user_id: UUID, data: dict) -> User:
        logger.info(
            "Updating user",
            extra={"user_id": str(user_id)}
        )

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            logger.warning(
                "User update failed: user not found",
                extra={"user_id": str(user_id)}
            )
            raise ValueError("User not found")

        for field, value in data.items():
            if value is not None:
                setattr(user, field, value)

        updated_user = await self.user_repo.update(user)

        logger.info(
            "User updated successfully",
            extra={
                "user_id": str(updated_user.id),
                "email": updated_user.email
            }
        )

        return updated_user

    async def delete_user(self, user_id: UUID) -> None:
        logger.info(
            "Deleting user",
            extra={"user_id": str(user_id)}
        )

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            logger.warning(
                "User deletion failed: user not found",
                extra={"user_id": str(user_id)}
            )
            raise ValueError("User not found")

        await self.user_repo.delete(user)

        logger.info(
            "User deleted successfully",
            extra={"user_id": str(user_id)}
        )
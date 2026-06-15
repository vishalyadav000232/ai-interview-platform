import logging

from uuid import UUID

from app.models.user import User
from app.schemas.user import CreateUser , UpdateUser
from app.core.security import SecurityService
from app.repository.interface.user_repository_interface import UserRepositoryInterface
from app.services.interface.user import UserServiceInterface
from app.core.exceptions import UserNotFound


logger = logging.getLogger(__name__)


class UserService(UserServiceInterface):

    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def create_user(self, user: CreateUser) -> User:
        logger.info(
            "Creating new user",
            extra={"email": user.email}
        )


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
            raise UserNotFound()

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        logger.debug(
            "Fetching user by email",
            extra={"email": email}
        )

        return await self.user_repo.get_by_email(email)

    async def update_user(self, user_id: UUID, data: UpdateUser) -> User:
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
            raise UserNotFound()
        allowed_fields = {
            "first_name", "last_name"
        }

        for field, value in data.items():
            if field in allowed_fields and value is not None:
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
            raise UserNotFound()

        await self.user_repo.delete(user)

        logger.info(
            "User deleted successfully",
            extra={"user_id": str(user_id)}
        )
        
    async def verify_email(self, user_id : UUID )-> User:
        if not user_id :
            raise ValueError("user_id are missing")
        
        user = await self.get_user_by_id(user_id=user_id)
        
        
                
        updated_user = await self.update_user(
            user_id=user.id ,
            data={
                "is_email_verified" : True
            })
        logger.info(
            "Email verified successfully !",
            extra={
                "user_id":str(updated_user.id)
            }
        )
        return updated_user
        
    
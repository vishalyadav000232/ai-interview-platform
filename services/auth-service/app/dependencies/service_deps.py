import logging

from fastapi import Depends

from app.dependencies.repository import get_user_repo, get_refresh_repo

from app.repository.interface.user_repository_interface import UserRepositoryInterface
from app.repository.interface.refresh_token_interface import RefreshTokenRepositoryInterface

from app.services.interface.user import UserServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.services.interface.refresh_token_service_interface import RefreshTokenServiceInterface
from app.services.interface.auth import AuthServiceInterface

from app.services.user import UserService
from app.services.token_service import TokenService
from app.services.refresh_token_service import RefreshTokenService
from app.services.auth import AuthService


from app.services.interface.email_service import EmailServiceInterface
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


def get_refresh_service(
    refresh_repo: RefreshTokenRepositoryInterface = Depends(get_refresh_repo),
) -> RefreshTokenServiceInterface:
    logger.debug("Initializing RefreshTokenService")
    return RefreshTokenService(repo=refresh_repo)


def get_token_service(
    refresh_service: RefreshTokenServiceInterface = Depends(get_refresh_service),
) -> TokenServiceInterface:
    logger.debug("Initializing TokenService")
    return TokenService(refresh_service=refresh_service)


def get_user_service(
    user_repo: UserRepositoryInterface = Depends(get_user_repo),
) -> UserServiceInterface:
    logger.debug("Initializing UserService")
    return UserService(user_repo=user_repo)


def get_auth_service(
    user_service: UserServiceInterface = Depends(get_user_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
) -> AuthServiceInterface:
    logger.debug("Initializing AuthService")

    return AuthService(
        user_service=user_service,
        token_service=token_service,
    )
    
    

def get_email_service()->EmailServiceInterface:
    return EmailService()
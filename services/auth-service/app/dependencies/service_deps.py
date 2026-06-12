from fastapi import Depends

from app.services.token_service import TokenService
from app.services.refresh_token_service import RefreshTokenService

from app.repository.interface.refresh_token_interface import RefreshTokenRepositoryInterface
from app.services.interface.refresh_token_service_interface import RefreshTokenServiceInterface

from app.dependencies.repository import get_refresh_repo


async def get_refresh_service(
    refresh_repo: RefreshTokenRepositoryInterface = Depends(get_refresh_repo)
) -> RefreshTokenServiceInterface:
    return RefreshTokenService(repo=refresh_repo)


async def get_token_service(
    refresh_service: RefreshTokenServiceInterface = Depends(get_refresh_service)
) -> TokenService:
    return TokenService(refresh_service=refresh_service)
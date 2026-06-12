from  fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_token_service



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token : str = Depends(oauth2_scheme),
    token_serivce :TokenServiceInterface = Depends(get_token_service),
    user_service : UserServiceInterface = Depends(get_user_service)
):pass
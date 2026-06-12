import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_token_service, get_user_service
from app.services.interface.user import UserServiceInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: TokenServiceInterface = Depends(get_token_service),
    user_service: UserServiceInterface = Depends(get_user_service),
):
    try:
        payload = token_service.verify_access_token(token=token)

        user_id = payload.get("sub")

        if not user_id:
            logger.warning("Access token missing subject")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        user = await user_service.get_user_by_id(user_id=user_id)

        if not user:
            logger.warning(
                "Authenticated user not found",
                extra={"user_id": str(user_id)}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        logger.debug(
            "Current user authenticated successfully",
            extra={"user_id": str(user.id)}
        )

        return user

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to authenticate current user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    

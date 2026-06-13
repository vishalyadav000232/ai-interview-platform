import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import CreateUser
from app.services.interface.auth import AuthServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_auth_service , get_token_service
from app.schemas.auth import RegisterResponse
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("/test")
async def test_route():
    return {
        "success": True,
        "message": "Auth router working"
    }


@router.post("/register", status_code=status.HTTP_201_CREATED , response_model=RegisterResponse)
async def register(
    user: CreateUser,
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    token_service : TokenServiceInterface = Depends(get_token_service)
):
    try:
        created_user = await auth_service.register(user_data=user)
        
        logger.info(
    "User registered successfully",
    extra={
        "user_id": str(created_user.id),
        "email": created_user.email
    }
)
        
        access_token = await token_service.create_access_token(created_user.id)
        refresh_token = await token_service.create_refresh_token(created_user.id)
        
        

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user" : created_user,
                "access_token" : access_token
            }
        }

    except ValueError as e:
        logger.warning(
            "Registration failed",
            extra={"email": user.email, "error": str(e)}
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        logger.exception(
            "Unexpected error in register route",
            extra={"email": user.email}
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
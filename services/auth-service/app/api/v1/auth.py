import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import CreateUser
from app.services.interface.auth import AuthServiceInterface
from app.dependencies.service_deps import get_auth_service

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


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: CreateUser,
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):
    try:
        created_user = await auth_service.register(user_data=user)

        return {
            "success": True,
            "message": "User registered successfully",
            "data": created_user
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
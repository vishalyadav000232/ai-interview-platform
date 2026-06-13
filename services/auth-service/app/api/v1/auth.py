import logging

from fastapi import APIRouter, Depends, HTTPException, status , Cookie
from fastapi.responses import Response
from app.core.exceptions import AppException
from app.schemas.user import CreateUser 
from app.services.interface.auth import AuthServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_auth_service , get_token_service
from app.schemas.auth import RegisterResponse  , LoginResponse
from fastapi.security import OAuth2PasswordRequestForm
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
    response : Response,
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
        
        logger.info(
            "refresh_token success fully set into cookies " ,
            extra={
                "refresh" : refresh_token
            }
        )
        
        response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,      
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
        
        

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user" : created_user,
                "access_token" : access_token
            }
        }
        
    except AppException:
        raise

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





@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    payload: OAuth2PasswordRequestForm=Depends(),
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
):
    user = await auth_service.login(
       payload
    )

    access_token = await token_service.create_access_token(user.id)
    refresh_token = await token_service.create_refresh_token(user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer"
        }
    }
    
    
@router.post("/refresh")
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    token_service: TokenServiceInterface = Depends(get_token_service),
):
    try:
        user = await auth_service.refresh(refresh_token)

        access_token = await token_service.create_access_token(user.id)
        new_refresh_token = await token_service.create_refresh_token(user.id)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,      
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )

        logger.info(
            "Token refreshed successfully",
            extra={
                "user_id": str(user.id)
            }
        )

        return {
            "success": True,
            "message": "Token refreshed successfully",
            "data": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }

    except AppException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error in refresh route"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
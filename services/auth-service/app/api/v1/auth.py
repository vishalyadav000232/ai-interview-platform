import logging

from fastapi import APIRouter, Depends, HTTPException, status , Cookie , Query
from fastapi.responses import Response
from app.core.exceptions import AppException
from app.schemas.user import CreateUser 
from app.services.interface.auth import AuthServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_auth_service , get_token_service
from app.schemas.auth import RegisterResponse  , LoginResponse , ChangePassword
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse
from app.core.exceptions import RefreshTokenMissingException
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
        
        email_verification_token = await token_service.create_email_verification_token(
            created_user.id
        )

        verification_link = (
            "http://localhost:8001/auth/verify-email"
            f"?token={email_verification_token}"
        )

        logger.info(
            "Email verification link generated",
            extra={
                "user_id": str(created_user.id),
                "email": created_user.email,
                "verification_link": verification_link
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
        
        
        logger.info(
            "refresh_token success fully set into cookies " ,
            extra={
                "refresh" : refresh_token
            }
        )
        

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user" : created_user,
                "access_token" : access_token,
                "verification_link": verification_link
                
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
        "access_token": access_token,
        "token_type": "bearer",
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
    
    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error in refresh route"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        
@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    token_service: TokenServiceInterface = Depends(get_token_service),
):
    
   
    try:
        if not refresh_token:
            raise RefreshTokenMissingException()
        
        await token_service.revoke_refresh_token(refresh_token)

        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=False,
            samesite="lax"
        )

        return {
            "success": True,
            "message": "Logged out successfully"
        }

    except AppException:
        raise
    
    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error in logout route")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/logout-all")
async def logout_all_devices(
    response: Response,
    current_user: User = Depends(get_current_user),
    token_service: TokenServiceInterface = Depends(get_token_service),
):
    revoked_count = await token_service.revoke_all_user_sessions(
        current_user.id
    )

    response.delete_cookie(
        key="refresh_token"
    )

    return {
        "success": True,
        "message": "Logged out from all devices successfully",
        "data": {
            "revoked_sessions": revoked_count
        }
    }
    
@router.post('/change-password')
async def change_password(
    response : Response,
    payload : ChangePassword,
    curret_user : User = Depends(get_current_user),
    auth_service : AuthServiceInterface = Depends(get_auth_service)
):
    await auth_service.change_password(
        user=curret_user,
        new_password=payload.new_password ,
        old_password=payload.old_password
        
    )
    
    response.delete_cookie(
        key="refresh_token"
    )
    

    return {
            "success": True,
            "message": "Password changed successfully"
            }
    
    
    
@router.post("/verify-email")
async def verify_email(
    token :str=  Query(...) ,
    auth_sevice :AuthServiceInterface = Depends(get_auth_service)
):
    
    if not token:
        raise ValueError("token are missing..")
    
    await auth_sevice.verify_email(token=token)
    
    return {
        "success": True,
        "message": "Email verified successfully"
    }
    
@router.post("/resend-verification")
async def resend_verification(
    current_user: User = Depends(get_current_user),
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):

    verification_link = await auth_service.resend_verification_email(
        user=current_user
    )

    return {
        "success": True,
        "message": "Verification email sent successfully",
        "verification_link": verification_link
    }
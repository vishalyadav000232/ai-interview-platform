import logging

from fastapi import APIRouter, Depends, HTTPException, status , Cookie , Query , BackgroundTasks 
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
from app.core.exceptions import AppException
from app.schemas.user import CreateUser 
from app.services.interface.auth import AuthServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.dependencies.service_deps import get_auth_service , get_token_service , get_email_service
from app.schemas.auth import RegisterResponse  , LoginResponse , ChangePassword , ForgotPasswordRequest , ResetPasswordRequest
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse
from app.core.exceptions import RefreshTokenMissingException


from app.services.interface.email_service import EmailServiceInterface


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
    backgroung_task :BackgroundTasks,
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    token_service : TokenServiceInterface = Depends(get_token_service),
    email_service : EmailServiceInterface = Depends(get_email_service)
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
        
        backgroung_task.add_task(
            email_service.send_email_verification,
            created_user.email,
            verification_link
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
    
    
@router.get("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(
    token: str = Query(...),
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):
    await auth_service.verify_email(token=token)

    return {
        "success": True,
        "message": "Email verified successfully"
    }


@router.post("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(
    background_task : BackgroundTasks,
    current_user: User = Depends(get_current_user),
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    email_service : EmailServiceInterface = Depends(get_email_service)
):
    verification_link = await auth_service.resend_verification_email(
        user=current_user
    )
    
    
    background_task.add_task(
        email_service.send_email_verification,
        current_user.email,
        verification_link
    )

    return {
        "success": True,
        "message": "Verification email sent successfully",
        "data": {
            "verification_link": verification_link
        }
    }
    


from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

@router.patch("/dev/me/unverify-email", status_code=status.HTTP_200_OK)
async def unverify_my_email_for_testing(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.is_email_verified = False

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return {
        "success": True,
        "message": "Email verification status set to false for testing",
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "is_email_verified": current_user.is_email_verified
        }
    }
    

@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    auth_service: AuthServiceInterface = Depends(get_auth_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
):

    reset_link = await auth_service.forgot_password(
        email=payload.email
    )

    if reset_link:
        background_tasks.add_task(
            email_service.send_password_reset_email,
            payload.email,
            reset_link
        )

    return {
        "success": True,
        "message": "If this email exists, password reset instructions have been sent",
        "data": {
            "reset_link": reset_link
        }
    }
    

@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordRequest,
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):

    await auth_service.reset_password(
        token=payload.token,
        new_password=payload.new_password
    )

    return {
        "success": True,
        "message": "Password reset successfully"
    }
    
from fastapi.requests import Request

@router.get("/debug-headers")
async def debug_headers(request: Request):
    return {
        "x_request_id": request.headers.get("x-request-id"),
        "x_user_id": request.headers.get("x-user-id"),
        "x_user_role": request.headers.get("x-user-role"),
        "authorization_exists": request.headers.get("authorization") is not None
    }

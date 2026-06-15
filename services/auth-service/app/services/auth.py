import logging
from app.services.interface.user import UserServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.schemas.user import CreateUser
from app.models.user import User
from app.services.interface.auth import AuthServiceInterface
from fastapi.security import OAuth2PasswordRequestForm
from app.core.exceptions import( 
                                RefreshTokenMissingException , InvalidCredentialsException , 
                                AppException,
                                UserAlreadyExistException , 
                                InvalidRefreshTokenException,
                                EmailVerificationTokenMissing,
                                EmailAlreadyVerifiedException,
                                InvalidEmailVerificationTokenException,
                                UserNotFound
                                )
from app.core.security import SecurityService
from fastapi import HTTPException




logger = logging.getLogger(__name__)




class AuthService(AuthServiceInterface):
    
    
    def __init__(
        self,
        user_service : UserServiceInterface,
        token_service : TokenServiceInterface
        ):
        
        self.user_service = user_service
        self.token_service = token_service
        self.security_service = SecurityService()
        
        
        
    async def register(self , user_data : CreateUser)-> User:
        
        try:
            logger.info(
                "Register attempt started ",
                extra={
                    "email" : user_data.email
                }
            )
            existing_user = await self.user_service.get_user_by_email(user_data.email)
            
            if existing_user:
                logger.warning(
                    "Register failed: email already registered",
                    extra={
                        "email":user_data.email
                    }
                )
                raise UserAlreadyExistException()
            
            
            user = await self.user_service.create_user(user_data)
            
            
            logger.info(
                "User Register Successfully ",
                extra={
                    "user_id": str(user.id),
                    "email": user.email
                }
            )
            return user
            
        except ValueError:
            raise
            
        except Exception:
            logger.exception(
                "Unexpected error during user registration",
                extra={"email": user_data.email}
            )
            raise
        
    async def login(self,login_data: OAuth2PasswordRequestForm) -> User:

        logger.info(
            "Login attempt started",
            extra={"email": login_data.username}
        )

        user = await self.user_service.get_user_by_email(
            login_data.username
        )

        if not user:
            logger.warning(
                "Login failed: invalid credentials",
                extra={"email": login_data.username}
            )
            raise InvalidCredentialsException()

        if not self.security_service.verify_password(
            login_data.password,
            user.password_hash
        ):
            logger.warning(
                "Login failed: invalid credentials",
                extra={"email": login_data.username}
            )
            raise InvalidCredentialsException()

        # if not user.is_active:
        #     logger.warning(
        #         "Login failed: inactive user",
        #         extra={
        #             "user_id": str(user.id),
        #             "email": user.email,
        #         }
        #     )
        #     raise UserInactiveException()

        logger.info(
            "Login successful",
            extra={
                "user_id": str(user.id),
                "email": user.email,
            }
        )

        return user
    


    async def refresh(self, refresh_token: str) -> User:
        try:
            if not refresh_token:
                logger.warning("Refresh token missing from cookies")
                raise RefreshTokenMissingException()

            payload = await self.token_service.verify_refresh_token(refresh_token)

            user_id = payload.get("sub")

            if not user_id:
                logger.warning("User id missing in refresh token payload")
                raise InvalidRefreshTokenException()
            
            await self.token_service.revoke_refresh_token(refresh_token)

            user = await self.user_service.get_user_by_id(
                user_id=user_id
            )

            logger.info(
                "Refresh token verified successfully",
                extra={"user_id": user_id}
            )

            return user

        except AppException:
            raise
        
        except HTTPException:
            raise

        except Exception:
            logger.exception("Unexpected error during token refresh")
            raise
        
    async def logout(self, refresh_token: str | None):
        if not refresh_token:
            return RefreshTokenMissingException()

        await self.token_service.revoke_refresh_token(refresh_token)

        return True
    
    async def change_password(self , user : User,  old_password : str , new_password : str)->None:
        
        if not self.security_service.verify_password(old_password  ,user.password_hash ):
            logger.warning(
                "Old password is incorrect",
                extra={
                    "user_id": user.id
                }
            )
            raise InvalidCredentialsException()
        
        user.password_hash = self.security_service.hash_password(new_password)
        
        await self.user_service.update_user(user_id=user.id ,data= {
            "password_hash": user.password_hash
        })
        
        logger.info(
            "Password update successfully ",
            extra={
                "user_id" : user.id
            }
        )
        
        
        await self.token_service.revoke_all_user_sessions(user_id=user.id)
        
    
    async def verify_email(self, token: str) -> User:
        if not token:
            logger.warning("Email verification token is missing")
            raise EmailVerificationTokenMissing()

        payload = await self.token_service.verify_email_verification_token(
            token=token
        )

        user_id = payload.get("sub")

        if not user_id:
            logger.warning("User id missing in email verification token")
            raise InvalidEmailVerificationTokenException()

        user = await self.user_service.get_user_by_id(user_id=user_id)

        if user.is_email_verified:
            logger.info(
                "User email already verified",
                extra={"user_id": str(user.id)}
            )
            return user

        verified_user = await self.user_service.verify_email(user_id=user.id)

        logger.info(
            "User email verified successfully",
            extra={"user_id": str(verified_user.id)}
        )

        return verified_user
        
        
    async def resend_verification_email(self, user: User) -> str:
        if user.is_email_verified:
            raise EmailAlreadyVerifiedException()

        token = await self.token_service.create_email_verification_token(
            user_id=user.id
        )

        verification_link = (
            f"http://localhost:8001/auth/verify-email"
            f"?token={token}"
        )

        logger.info(
            "Email verification link generated",
            extra={"user_id": str(user.id)}
        )

        return verification_link
            
        
    async def forgot_password(self, email : str)-> None:
        
        if not email:
            raise ValueError("email are missing")
        
        user = await self.user_service.get_user_by_email(email=email)
        
        if not user:
            logger.warning(
                "user does not exist"
            )
            return None
        
        reset_token = await self.token_service.create_password_reset_token(user_id=user.id)
        
        reset_link = (
        "http://localhost:8001/auth/reset-password"
        f"?token={reset_token}"
    )
        logger.info(
        "Password reset link generated",
        extra={
            "user_id": str(user.id),
            "email": user.email
        }
    )
        return reset_link
    

    
    async def reset_password(self, token: str, new_password: str)-> None:
        
        payload = await self.token_service.verify_password_reset_token(token=token)
        
        user_id = payload.get("sub")

        if not user_id:
            raise InvalidCredentialsException()

        user = await self.user_service.get_user_by_id(
        user_id=user_id
    )
        new_password_hash = self.security_service.hash_password(
        new_password
    )
        
        await self.user_service.update_user(
        user_id=user.id,
        data={
            "password_hash": new_password_hash
        }
    )
        await self.token_service.revoke_all_user_sessions(
        user_id=user.id
    )
        
        logger.info(
        "Password reset successfully",
        extra={
            "user_id": str(user.id)
        }
    )

        
       
        
        
        
            
    
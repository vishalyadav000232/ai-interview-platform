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
                                InvalidRefreshTokenException
                                )
from app.core.security import SecurityService




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

        except Exception:
            logger.exception("Unexpected error during token refresh")
            raise
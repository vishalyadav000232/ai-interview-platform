import logging
from app.services.interface.user import UserServiceInterface
from app.services.interface.token_service_interface import TokenServiceInterface
from app.schemas.user import CreateUser
from app.models.user import User
from app.services.interface.auth import AuthServiceInterface

logger = logging.getLogger(__name__)


class AuthService(AuthServiceInterface):
    
    
    def __init__(
        self,
        user_service : UserServiceInterface,
        token_service : TokenServiceInterface
        ):
        
        self.user_service = user_service
        self.token_service = token_service
        
        
        
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
            
                
    
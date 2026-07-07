from abc import ABC , abstractmethod
from app.schemas.user import CreateUser
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm


class AuthServiceInterface(ABC):
    
    @abstractmethod
    async def register(self, user_data :CreateUser )-> User:
        raise NotImplementedError
    @abstractmethod
    async def login(self , login_data: OAuth2PasswordRequestForm)->User:
        raise NotImplementedError
    @abstractmethod
    async def refresh(self, refresh_token: str) -> User:
        raise NotImplementedError
    @abstractmethod
    async def change_password(self ,user : User ,  old_password : str , new_password : str)->None:
        raise NotImplementedError
    
    @abstractmethod
    async def verify_email(self,token: str) -> User:
        pass
    @abstractmethod
    async def resend_verification_email(self,user: User) -> str:
        pass
    
    @abstractmethod
    async def forgot_password(self , email:str)->None:
        raise NotImplementedError
    @abstractmethod
    async def reset_password(self , token : str , new_password : str)->None:
        raise NotImplementedError
    
        
        
        

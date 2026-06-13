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
        

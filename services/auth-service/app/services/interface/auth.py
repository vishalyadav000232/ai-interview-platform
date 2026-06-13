from abc import ABC , abstractmethod
from app.schemas.user import CreateUser
from app.models.user import User

class AuthServiceInterface(ABC):
    
    @abstractmethod
    async def register(self, user_data :CreateUser )-> User:
        raise NotImplementedError
        

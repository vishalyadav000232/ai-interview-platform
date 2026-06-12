from app.services.interface.token_service_interface import TokenServiceInterface
from app.services.interface.refresh_token_service_interface import RefreshTokenServiceInterface
from app.core.config import settings
import hashlib
from uuid import UUID
from datetime import datetime , timedelta , timezone
from jose import jwt , JWTError


class TokenService(TokenServiceInterface):
    
    def __init__(self , refresh_service : RefreshTokenServiceInterface):
        
        self.refresh_service = refresh_service
        
        self.secret_key = settings.JWT_SECRATE_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_expire_time = settings.REFRESH_TOKEN_EXPIRE_MINUTS
        self.refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        
        if not self.secret_key:
            raise ValueError("secret key is missing")
        
    @staticmethod  
    def hash_token(self , token:str)-> str:
        return hashlib.sha256(token.encode()).hexdigest()
    
    async def create_access_token(self, user_id : UUID | str):
        
        if not user_id:
            raise ValueError("user_id is missing")
        
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_expire_time)
        
        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": expire,
        }
        
        return jwt.encode(payload , self.secret_key , self.algorithm)

    
    
    
        
        
        
        
from app.services.interface.token_service_interface import TokenServiceInterface
from app.services.interface.refresh_token_service_interface import RefreshTokenServiceInterface
from app.core.config import settings
import hashlib
from uuid import UUID , uuid4
from datetime import datetime , timedelta , timezone
from jose import jwt , JWTError
from fastapi import HTTPException , status

import logging

logger = logging.getLogger(__name__)


class TokenService(TokenServiceInterface):
    
    def __init__(self , refresh_service : RefreshTokenServiceInterface):
        
        self.refresh_service = refresh_service
        
        self.secret_key = settings.JWT_SECRATE_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_expire_time = settings.ACCESS_TOKEN_EXPIRE_MINUTS
        self.refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        
        if not self.secret_key:
            raise ValueError("secret key is missing")
        
    @staticmethod  
    def hash_token( token:str)-> str:
        return hashlib.sha256(token.encode()).hexdigest()
    
    async def create_access_token(self, user_id : UUID | str)-> str:
        
        if not user_id:
            logger.warning("Access token creation faild : missing (user_id)")
            raise ValueError("user_id is missing")
        
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_expire_time)
        
        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": expire,
        }
        
        access_token = jwt.encode(payload , self.secret_key , algorithm=self.algorithm)
        logger.info(
            "Access token created",
            extra={
                "user_id": str(user_id),
                "token_type": "access",
                "expires_at": expire.isoformat()
            }
        )
        return access_token
    
    async def create_refresh_token(self, user_id : UUID | str)-> str:
        
        if not user_id :
            logger.warning("refresh token creation faild : missing (user_id")
            raise ValueError("user_id is missing..")
        try: 
            now = datetime.now(timezone.utc)
            expire = now + timedelta(days=self.refresh_expire_days)
            
            jti = str(uuid4())
            
            payload = {
                "sub" : str(user_id),
                "type" : "refresh",
                "iat" : now,
                "exp" : expire,
                "jti" : jti
            }
            
            refresh_token = jwt.encode(
                payload,
                self.secret_key,
                algorithm=self.algorithm
            
            )
            
            token_hash = self.hash_token(refresh_token)
            
            await self.refresh_service.create_token(
                user_id=user_id,
                jti=jti,
                token_hash=token_hash,
                expires_at=expire
            )
            
            logger.info(
            "Refresh token created",
            extra={
                "user_id": str(user_id),
                "jti": jti,
                "token_type": "refresh",
                "expires_at": expire.isoformat()
            }
        )
            return refresh_token
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create refresh token"
            )
        
    async def verify_token(self , token : str , token_type : str)-> dict:
        if not token:
            logger.warning("token are missing .")
            raise ValueError("missing token")
        
        try:
            payload = jwt.decode(token  , self.secret_key , algorithm= self.algorithm)
            
            actual_type = payload.get("type")
            user_id = payload.get("sub")
            
            if actual_type != token_type:
                logger.warning(
                    "Token type missmatch",
                    extra={
                        "expected_type":token_type,
                        "actual_type": actual_type,
                        "user_id": user_id
                        
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid Token "
                )
                
            logger.info(
                "Token veverified successfully ",
                extra={
                    "user_id": user_id,
                    "token_type": actual_type,
                    "jti": payload.get("jti")
                }
            )
            
            return payload
        except JWTError:
            logger.warning(
                "Invalid or expired token received",
                extra={"token_type": token_type}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
    
    async def verify_access_token(self, token: str) -> dict:
        return await self.verify_token(token, token_type="access")

    async def verify_refresh_token(self, token: str) -> dict:
        return await self.verify_token(token, token_type="refresh")
    
    
    
    async def revoke_refresh_token(self, token : str):
        payload = await self.verify_refresh_token(token)
        jti = payload.get("jti")
        if not jti:
            logger.warning(
                "Refresh token revoke failed: missing jti",
                extra={"user_id": payload.get("sub")}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
        )
        
        result = await self.refresh_service.revoke_token(jti=jti)
        logger.info(
        "Refresh token revoked",
        extra={
            "user_id": payload["sub"],
            "jti": jti
        }
        )
        
        return result
            
            


        
        
        
            
            
            
            
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
            
            logger.info(f"this is the jti {jti}")
            
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
        except Exception as error:
            logger.exception("Refresh token creation failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create refresh token"
            ) from error
        
    async def verify_token(self , token : str , token_type : str)-> dict:
        
        if not token:
            logger.warning("token are missing .")
            raise ValueError("missing token")
        
        try:
            payload =  jwt.decode(token  , self.secret_key , algorithms= [self.algorithm])
            
            actual_type = payload.get("type")
            user_id = payload.get("sub")
            
            logger.info(f"actuval type : {actual_type}")
            logger.info(f"token type : {token_type}")
            
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
        payload =  await self.verify_token(token, token_type="refresh")
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
        
        token_hash = self.hash_token(token=token)
            
        is_valid = await self.refresh_service.validate_token(jti=jti , token_hash=token_hash)
        
        
        if not is_valid:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or expired"
        )
            
        return payload
        
        
    
    
    
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
    
    async def rotate_refresh_token(self , refresh_token : str)->dict:
        payload = await self.verify_refresh_token(token=refresh_token)
        
        old_jti = payload.get("jti")
        user_id = payload.get("sub")
        
        if not old_jti or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        await self.refresh_service.revoke_token(old_jti)
        
        new_access_token = await self.create_access_token(user_id=user_id)
        new_refresh_token= await self.create_refresh_token(user_id=user_id)
        
        
        logger.info(
            "Refresh token rotated",
            extra={
                "user_id": user_id,
                "old_jti": old_jti
            }
        )
        
        return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
        
    async def revoke_all_user_sessions(self, user_id: UUID | str) -> int:
        if not user_id:
            raise ValueError("user_id is missing")

        revoked_count = await self.refresh_service.revoke_all_for_user(
            user_id=user_id
        )

        logger.info(
            "All user sessions revoked",
            extra={
                "user_id": str(user_id),
                "revoked_count": revoked_count
            }
        )

        return revoked_count
    
    
    async def create_email_verification_token(self, user_id: UUID | str) -> str:
        if not user_id:
            raise ValueError("user_id is missing")

        now = datetime.now(timezone.utc)
        expire = now + timedelta(hours=24)
        jti = str(uuid4())

        payload = {
            "sub": str(user_id),
            "type": "email_verification",
            "iat": now,
            "exp": expire,
            "jti": jti,
        }

        token = jwt.encode(
            payload,
            key=self.secret_key,
            algorithm=self.algorithm
        )

        logger.info(
            "Email verification token created successfully",
            extra={"user_id": str(user_id), "jti": jti}
        )

        return token
    async def verify_email_verification_token(self, token: str) -> dict:
        if not token:
            raise ValueError("email verification token is missing")

        payload = await self.verify_token(
            token=token,
            token_type="email_verification"
        )

        logger.info(
            "Email verification token verified successfully",
           
        )

        return payload
    
    
    async def create_password_reset_token(self, user_id : UUID | str)->str:
        if not user_id:
            raise ValueError("user-id is missing")
        
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=15)
        jti = str(uuid4())

        payload = {
            "sub": str(user_id),
            "type": "password_reset",
            "iat": now,
            "exp": expire,
            "jti": jti,
        }
        
        token = jwt.encode(
            payload,
            key=self.secret_key,
            algorithm=self.algorithm
        )

        logger.info(
            " password reset token created successfully",
            extra={"user_id": str(user_id), "jti": jti}
        )

        return token
    
    
    async def verify_password_reset_token(self, token : str)-> dict:
        
        
        payload =await  self.verify_token(token=token , token_type="password_reset")
        
        logger.info("password reset successfully ")
        
        return payload
        
        
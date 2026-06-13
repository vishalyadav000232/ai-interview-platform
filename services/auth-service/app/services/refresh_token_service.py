import logging
from app.services.interface.refresh_token_service_interface import RefreshTokenServiceInterface
from app.repository.interface.refresh_token_interface import RefreshTokenRepositoryInterface
from app.schemas.refresh_token import RefreshTokenCreate
from uuid import UUID
from datetime import datetime , timezone
from app.models.refresh_token import RefreshToken
import hmac


logger = logging.getLogger(__name__)



class RefreshTokenService(RefreshTokenServiceInterface):
    def __init__(self , repo :RefreshTokenRepositoryInterface ):
        self.repo = repo
        
    async def create_token(self, user_id : UUID, jti : str, token_hash : str, expires_at : datetime)->RefreshToken:
        
        if not user_id:
            raise ValueError("User ID is required")
        if not jti:
            raise ValueError("Token jti is required")
        if not token_hash:
            raise ValueError("Token hash is required")
        if expires_at <= datetime.now(timezone.utc):
            raise ValueError("Token expiry must be in future")
        
        payload = RefreshTokenCreate(
            user_id  = user_id,
            jti = jti,
            token_hash = token_hash,
            expires_at = expires_at
        )
        
        refresh_token = await self.repo.create(payload)
        
        
        logger.info(
            "Refresh token record created",
            extra={
                "user_id": str(user_id),
                "jti": jti,
            }
        )
        
        return refresh_token
    
    
    async def validate_token(self, jti : str, token_hash : str)-> bool:
        
        if not jti or not token_hash:
            return False
        
        refresh_token = await self.repo.get_by_jti(jti=jti)
        
        if refresh_token is None:
            return False
        
        
        if refresh_token.is_revoked:
            return False
        if refresh_token.expires_at <= datetime.now(timezone.utc):
            return False
        if not hmac.compare_digest(refresh_token.token_hash, token_hash):
            return False
        
        return True
    
    
    async def revoke_token(self, jti :str) -> bool:
        
        if not jti:
            return False
        
        refresh_token = await self.repo.get_by_jti(jti=jti)
        
        if  refresh_token is None : 
            return False
        
        if refresh_token.is_revoked:
            return True
        
        
        revoked_token = await self.repo.revoke(refresh_token.id)
        if revoked_token:
            logger.info(
                "Refresh token revoked",
                extra={"jti": jti}
            )
        
        return revoked_token is not None
    
    async def revoke_all_for_user(
        self,
        user_id: UUID | str,
    ) -> int:

        if not user_id:
            raise ValueError("User id is required")

        revoked_count = await self.repo.revoke_all_for_user(user_id)
        logger.info(
            "All refresh tokens revoked for user",
            extra={
                "user_id": str(user_id),
                "revoked_count": revoked_count,
            }
        )
        
        return revoked_count

        
        
        
       
        
        
        
        
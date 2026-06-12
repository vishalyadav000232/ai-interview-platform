from app.repository.interface.refresh_token_interface import RefreshTokenRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.refresh_token import RefreshTokenCreate
from app.models.refresh_token import RefreshToken
from sqlalchemy import select , update
from datetime import datetime


from uuid import UUID


class RefreshTokenRepository(RefreshTokenRepositoryInterface):
    def __init__(self , db : AsyncSession ):
        self.db = db
        
    
    async def create(self, payload :RefreshTokenCreate )->RefreshToken:
        
        refresh_token = RefreshToken(
            user_id = payload.user_id,
            token_hash= payload.token_hash,
            expires_at=payload.expire_at
        )
        
        self.db.add(refresh_token)
        
        await self.db.commit()
        await self.db.refresh(refresh_token)
        
        return refresh_token
    
    async def get_by_token_hash(self, token_hash : str)-> RefreshToken:
        
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
        
        result = await self.db.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def revoke(self, token_id : UUID | str):
        
        stmt = select(RefreshToken).where(
            RefreshToken.id == token_id
        )
        
        refresh = await self.db.execute(stmt)
        refresh_token = refresh.scalar_one_or_none()
        
        if refresh_token is None:
            return None
        
        refresh_token.is_revoke = True
        
        await self.db.commit()
        await self.db.refresh(refresh_token)
        
        return refresh_token
    
    async def revoke_all_for_user(self, user_id :UUID | str):
        
        stmt = update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).values(
            is_revoked =True,
            revoked_at= datetime.utcnow
        )
        try:
            results = await self.db.execute(stmt)
            await self.db.commit()
            
            return results.rowcount or 0
        except Exception:
            await self.db.rollback()
            raise
    
    async def get_by_jti(self,jti: str,) -> RefreshToken | None:

        stmt = select(RefreshToken).where(
            RefreshToken.jti == jti
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
        
        
        
        
        
        
        
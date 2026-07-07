from sqlalchemy import String , ForeignKey , DateTime , Boolean , func
from sqlalchemy.orm import Mapped  , mapped_column
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid4
    )
    jti :Mapped[str] =mapped_column(String(255) , nullable=False , unique=True)
    
    user_id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id" , ondelete="CASCADE"),
        nullable=False,
        index=True,
        
    )
    
    token_hash : Mapped[str] = mapped_column(
        String(255) , nullable=False ,unique=True)
    expires_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    
    is_revoked :Mapped[bool] = mapped_column(Boolean , default=False)
    revoked_at: Mapped[datetime] =mapped_column(DateTime(timezone=True), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True) , server_default=func.now())
    




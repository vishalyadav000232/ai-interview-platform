from app.db.base import Base
from sqlalchemy.orm import Mapped , mapped_column 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String , Enum , Boolean , DateTime , func
from uuid import uuid4 , UUID as PyUUID
from app.core.constant import UserRole
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id : Mapped[PyUUID] = mapped_column(UUID(as_uuid=True) , index=True , primary_key=True , default=uuid4)
    
    
    first_name :Mapped[str] = mapped_column(String(100) , nullable=False )
    last_name : Mapped[str] = mapped_column(String(100) , nullable=True)
    
    email : Mapped[str] = mapped_column(String(255) , index=True , unique=True , nullable= False)
    
    password_hash : Mapped[str] = mapped_column(String(255) , nullable=False)
    
    role : Mapped[UserRole] = mapped_column(Enum(UserRole) , default=UserRole.STUDENT , nullable=False)
    
    auth_provider : Mapped[str] = mapped_column(String(50) , default="LOCAL")
    
    is_email_verified : Mapped[bool] = mapped_column(Boolean, default=True)
    is_active:Mapped[bool]= mapped_column(Boolean , default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    last_login_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True) , nullable=True)
    
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True) , server_default=func.now() , nullable=False)
    
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True) , server_default=func.now(),onupdate=func.now() , nullable=False )
    
    
    
    
    
    
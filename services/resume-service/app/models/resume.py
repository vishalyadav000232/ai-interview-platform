from sqlalchemy.orm import mapped_column , Mapped  , relationship 
from sqlalchemy import String , Boolean , DateTime , Text , Enum , Integer

from datetime import datetime , timezone
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.database.base import Base
from enum import Enum as PyEnum

class ResumeStatus(str , PyEnum):
    
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    FAILED = "failed"



class Resume(Base):
    
    __tablename__= "resumes"
    
    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True) , primary_key=True , index= True , default=uuid4)
    
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True) , index=True , nullable=False)
    
    original_file_name : Mapped[str]= mapped_column(String(255) , nullable=False)
    
    storage_file_name : Mapped[str] = mapped_column(String(255) , nullable=False , unique=True)
    
    file_url : Mapped[str] = mapped_column(Text , nullable=False)
    
    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[ResumeStatus] = mapped_column(
        Enum(ResumeStatus),
        default=ResumeStatus.UPLOADED,
        nullable=False,
        index=True
    )

    parsed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    upload_source: Mapped[str] = mapped_column(
        String(50),
        default="local" ,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )
    failure_reason: Mapped[str | None] = mapped_column(
    Text,
    nullable=True
)
    processing_started_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True
)

    processing_completed_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True
)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    profile = relationship(
    "ResumeProfile",
    back_populates="resume",
    uselist=False,
    cascade="all, delete-orphan",
)
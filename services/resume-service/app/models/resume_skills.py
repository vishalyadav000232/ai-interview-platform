from app.database.base import Base
from uuid import UUID as PayUUID , uuid4
from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey , String , DateTime , func , UniqueConstraint

class ResumeSkill(Base):
    
    __tablename__="resume_skills"
    
    __table_args__= (
        UniqueConstraint("resume_id" , "skill_name", name="uq_resume_skills"),
    )
    
    id : Mapped[PayUUID] = mapped_column(UUID(as_uuid=True) , primary_key=True , index= True , nullable= False , default=uuid4)
    
    resume_id : Mapped[PayUUID] = mapped_column(UUID(as_uuid=True) ,ForeignKey("resumes.id" , ondelete="CASCADE") , nullable= False , index= True )
    
    skill_name :Mapped[str] = mapped_column(String(255) , nullable= False , index=True )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="skills",
    )
    
    
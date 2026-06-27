from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
        index=True,
    )

    resume_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    overall_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    profile_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    skills_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    education_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    experience_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    projects_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    resume_completeness: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    keyword_match_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    missing_skills: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    matched_skills: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    suggestions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    strengths: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    weaknesses: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
    )

    analysis_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="v1",
    )

    analysis_time_ms: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="analysis",
    )
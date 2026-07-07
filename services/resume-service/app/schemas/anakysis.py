from pydantic import BaseModel , ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class ResumeAnalysisResponse(BaseModel):
    id: UUID
    resume_id: UUID

    overall_score: Decimal

    profile_score: Decimal
    skills_score: Decimal
    education_score: Decimal
    experience_score: Decimal
    projects_score: Decimal

    matched_skills: list[str]
    missing_skills: list[str]

    suggestions: list[str]
    strengths: list[str]
    weaknesses: list[str]

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
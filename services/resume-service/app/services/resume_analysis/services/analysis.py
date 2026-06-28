
import time
from decimal import Decimal , ROUND_HALF_UP
from uuid import UUID

from app.models.resume_analysis import ResumeAnalysis
from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_analysis import ResumeAnalysisRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface

from functools import cached_property

from dataclasses import dataclass
from typing import Final

 
ANALYSIS_VERSION: Final[str] = "v3"
 
DB_FETCH_TIMEOUT_SECONDS: Final[float] = 5.0
 
CACHE_TTL_SECONDS: Final[int] = 300  # 5 minutes
 
FRESHER_BASELINE_SCORE: Final[Decimal] = Decimal("5")
 
PROJECTS_THRESHOLD: Final[int] = 2
 
REQUIRED_SKILLS: Final[frozenset[str]] = frozenset({
    "python",
    "fastapi",
    "postgresql",
    "sql",
    "docker",
    "redis",
    "git",
    "github",
    "rest api",
    "jwt",
})

@dataclass(frozen=True)
class _ScoreWeights:
    
    PROFILE:    Decimal = Decimal("20")
    SKILLS:     Decimal = Decimal("30")
    EDUCATION:  Decimal = Decimal("15")
    PROJECTS:   Decimal = Decimal("20")
    EXPERIENCE: Decimal = Decimal("15")
    
    def total(self)-> Decimal:
        self.PROFILE + self.SKILLS + self.EDUCATION + self.PROJECTS + self.EXPERIENCE


W = Final[_ScoreWeights] = _ScoreWeights()
 


PROFILE_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "full_name",
    "email",
    "phone",
    "linkedin_url",
)

@dataclass(frozen=True)
class SectionScores:
    profile : Decimal
    skills: Decimal
    education: Decimal
    projects: Decimal
    experience: Decimal
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    
    @cached_property
    def overall(self) -> Decimal:
        
        raw = (
            self.profile
            + self.skills
            + self.education
            + self.projects
            + self.experience
        )
        return min(raw, Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
 
    @cached_property
    def keyword_match_percentage(self) -> Decimal:
        if not REQUIRED_SKILLS:
            return Decimal("0")
        return (
            Decimal(len(self.matched_skills))
            / Decimal(len(REQUIRED_SKILLS))
            * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
    

def score_profile(profile) -> Decimal:
    if not profile:
        return Decimal("0")
 
    points_each = W.PROFILE / Decimal(len(PROFILE_REQUIRED_FIELDS))
    present = sum(1 for f in PROFILE_REQUIRED_FIELDS if getattr(profile, f, None))
    return (points_each * Decimal(present)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
 
 
def score_skills(skills) -> tuple[Decimal, list[str], list[str]]:
    
    resume_skills: set[str] = {
        skill.name.lower().strip()
        for skill in (skills or [])
        if getattr(skill, "name", None)
    }
 
    matched = sorted(REQUIRED_SKILLS & resume_skills)
    missing = sorted(REQUIRED_SKILLS - resume_skills)
 
    score = (
        Decimal(len(matched)) / Decimal(len(REQUIRED_SKILLS))
    ) * W.SKILLS
 
    return score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), matched, missing
 
 
def score_education(education) -> Decimal:
    
    return W.EDUCATION if education else Decimal("0")
 
 
def score_projects(projects) -> Decimal:
  
    count = len(projects or [])
    if count == 0:
        return Decimal("0")
    if count < PROJECTS_THRESHOLD:
        return W.PROJECTS / Decimal("2")
    return W.PROJECTS
 
 
def score_experience(experiences) -> Decimal:
   
    return W.EXPERIENCE if experiences else FRESHER_BASELINE_SCORE
 


def build_section_scores(
    profile, skills, education, projects, experiences
) -> SectionScores:
   
    skills_score, matched, missing = score_skills(skills)
    return SectionScores(
        profile=score_profile(profile),
        skills=skills_score,
        education=score_education(education),
        projects=score_projects(projects),
        experience=score_experience(experiences),
        matched_skills=tuple(matched),
        missing_skills=tuple(missing),
    )
    


def _profile_complete(s: SectionScores) -> bool:
    return s.profile >= W.PROFILE
 
 
def _skills_strong(s: SectionScores) -> bool:
    # "strong" = at least 2/3 of required skills present
    return s.skills >= W.SKILLS * Decimal("0.67")
 
 
def generate_suggestions(s: SectionScores) -> list[str]:
    out: list[str] = []
    if not _profile_complete(s):
        out.append(
            "Complete your profile: add full name, email, phone, and LinkedIn URL."
        )
    if s.missing_skills:
        out.append(
            f"Add these in-demand backend skills: {', '.join(s.missing_skills)}."
        )
    if s.education == Decimal("0"):
        out.append(
            "Add your education details (degree, institution, graduation year)."
        )
    if s.projects < W.PROJECTS:
        out.append(
            f"Include at least {PROJECTS_THRESHOLD} technical projects "
            "with tech stack and measurable impact."
        )
    if s.experience < W.EXPERIENCE:
        out.append(
            "Add internship, freelance, or open-source contribution experience."
        )
    return out
 
 
def generate_strengths(s: SectionScores) -> list[str]:
    out: list[str] = []
    if _profile_complete(s):
        out.append("Profile section is fully filled out.")
    if _skills_strong(s):
        out.append(
            f"Strong backend skill coverage "
            f"({len(s.matched_skills)}/{len(REQUIRED_SKILLS)} required skills matched)."
        )
    if s.education > Decimal("0"):
        out.append("Education details are present.")
    if s.projects >= W.PROJECTS:
        out.append(f"Has {PROJECTS_THRESHOLD}+ technical projects showcased.")
    if s.experience >= W.EXPERIENCE:
        out.append("Work or internship experience is documented.")
    return out
 
 
def generate_weaknesses(s: SectionScores) -> list[str]:
    out: list[str] = []
    if not _profile_complete(s):
        out.append("Profile is incomplete — missing contact or LinkedIn info.")
    if not _skills_strong(s):
        missing_str = ", ".join(s.missing_skills) if s.missing_skills else "none detected"
        out.append(f"Key backend skills missing: {missing_str}.")
    if s.education == Decimal("0"):
        out.append("Education section is absent.")
    if s.projects < W.PROJECTS:
        out.append("Insufficient technical projects to stand out to recruiters.")
    if s.experience < W.EXPERIENCE:
        out.append("Limited or no professional/internship experience listed.")
    return out
 

class ResumeAnalysisService:
    def __init__(
        self,
        resume_repo: ResumeRepositoryInterface,
        profile_repo: ResumeProfileRepositoryInterface,
        skill_repo: ResumeSkillRepositoryInterface,
        education_repo: ResumeEducationRepositoryInterface,
        project_repo: ResumeProjectRepositoryInterface,
        experience_repo: ResumeExprienceRepositoryInteraface,
        analysis_repo: ResumeAnalysisRepositoryInterface,
    ) -> None:
        self.resume_repo = resume_repo
        self.profile_repo = profile_repo
        self.skill_repo = skill_repo
        self.education_repo = education_repo
        self.project_repo = project_repo
        self.experience_repo = experience_repo
        self.analysis_repo = analysis_repo
       
        
    

    async def analyze_resume(self, resume_id: UUID) -> ResumeAnalysis:
        start_time = time.perf_counter()

        resume = await self.resume_repo.get_by_id(resume_id)
        if not resume:
            raise ValueError("Resume not found")

        profile = await self.profile_repo.get_by_resume_id(resume_id)
        skills = await self.skill_repo.get_by_resume_id(resume_id)
        education = await self.education_repo.get_by_resume_id(resume_id)
        projects = await self.project_repo.get_by_resume_id(resume_id)
        experiences = await self.experience_repo.get_by_resume_id(resume_id)

        profile_score = self._calculate_profile_score(profile)
        skills_score, matched_skills, missing_skills = self._calculate_skills_score(skills)
        education_score = self._calculate_education_score(education)
        projects_score = self._calculate_projects_score(projects)
        experience_score = self._calculate_experience_score(experiences)

        overall_score = self._calculate_overall_score(
            profile_score=profile_score,
            skills_score=skills_score,
            education_score=education_score,
            projects_score=projects_score,
            experience_score=experience_score,
        )

        suggestions = self._generate_suggestions(
            profile_score=profile_score,
            skills_score=skills_score,
            education_score=education_score,
            projects_score=projects_score,
            experience_score=experience_score,
            missing_skills=missing_skills,
        )

        strengths = self._generate_strengths(
            profile_score=profile_score,
            skills_score=skills_score,
            education_score=education_score,
            projects_score=projects_score,
            experience_score=experience_score,
        )

        weaknesses = self._generate_weaknesses(
            profile_score=profile_score,
            skills_score=skills_score,
            education_score=education_score,
            projects_score=projects_score,
            experience_score=experience_score,
        )

        analysis_time_ms = int((time.perf_counter() - start_time) * 1000)

        analysis = ResumeAnalysis(
            resume_id=resume_id,
            overall_score=overall_score,
            profile_score=profile_score,
            skills_score=skills_score,
            education_score=education_score,
            projects_score=projects_score,
            experience_score=experience_score,
            resume_completeness=overall_score,
            keyword_match_percentage=skills_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            suggestions=suggestions,
            strengths=strengths,
            weaknesses=weaknesses,
            analysis_version="v1",
            analysis_time_ms=analysis_time_ms,
        )

        return await self.analysis_repo.create(analysis)

    def _calculate_profile_score(self, profile) -> Decimal:
        score = Decimal("0")

        if not profile:
            return score

        if getattr(profile, "full_name", None):
            score += Decimal("5")

        if getattr(profile, "email", None):
            score += Decimal("5")

        if getattr(profile, "phone", None):
            score += Decimal("5")

        if getattr(profile, "linkedin_url", None):
            score += Decimal("5")

        return score

    def _calculate_skills_score(self, skills) -> tuple[Decimal, list[str], list[str]]:
        required_skills = {
            "python",
            "fastapi",
            "postgresql",
            "sql",
            "docker",
            "redis",
            "git",
            "github",
            "rest api",
            "jwt",
        }

        resume_skills = {
            skill.name.lower().strip()
            for skill in skills
            if getattr(skill, "name", None)
        }

        matched_skills = sorted(required_skills.intersection(resume_skills))
        missing_skills = sorted(required_skills.difference(resume_skills))

        if not required_skills:
            return Decimal("0"), matched_skills, missing_skills

        match_percentage = (
            Decimal(len(matched_skills)) / Decimal(len(required_skills))
        ) * Decimal("30")

        return match_percentage, matched_skills, missing_skills

    def _calculate_education_score(self, education) -> Decimal:
        if not education:
            return Decimal("0")

        return Decimal("15")

    def _calculate_projects_score(self, projects) -> Decimal:
        project_count = len(projects)

        if project_count == 0:
            return Decimal("0")

        if project_count == 1:
            return Decimal("10")

        return Decimal("20")

    def _calculate_experience_score(self, experiences) -> Decimal:
        if not experiences:
            return Decimal("5")

        return Decimal("15")

    def _calculate_overall_score(
        self,
        profile_score: Decimal,
        skills_score: Decimal,
        education_score: Decimal,
        projects_score: Decimal,
        experience_score: Decimal,
    ) -> Decimal:
        return (
            profile_score
            + skills_score
            + education_score
            + projects_score
            + experience_score
        )

    def _generate_suggestions(
        self,
        profile_score: Decimal,
        skills_score: Decimal,
        education_score: Decimal,
        projects_score: Decimal,
        experience_score: Decimal,
        missing_skills: list[str],
    ) -> list[str]:
        suggestions: list[str] = []

        if profile_score < Decimal("20"):
            suggestions.append("Complete your profile section with name, email, phone and LinkedIn.")

        if missing_skills:
            suggestions.append(f"Add missing backend skills: {', '.join(missing_skills)}.")

        if education_score == Decimal("0"):
            suggestions.append("Add your education details.")

        if projects_score < Decimal("20"):
            suggestions.append("Add at least two strong technical projects.")

        if experience_score < Decimal("15"):
            suggestions.append("Add internship, freelance, open-source or practical project experience.")

        return suggestions

    def _generate_strengths(
        self,
        profile_score: Decimal,
        skills_score: Decimal,
        education_score: Decimal,
        projects_score: Decimal,
        experience_score: Decimal,
    ) -> list[str]:
        strengths: list[str] = []

        if profile_score == Decimal("20"):
            strengths.append("Profile section is complete.")

        if skills_score >= Decimal("20"):
            strengths.append("Good backend skill coverage.")

        if education_score == Decimal("15"):
            strengths.append("Education section is available.")

        if projects_score == Decimal("20"):
            strengths.append("Good number of technical projects.")

        if experience_score == Decimal("15"):
            strengths.append("Experience section is available.")

        return strengths

    def _generate_weaknesses(
        self,
        profile_score: Decimal,
        skills_score: Decimal,
        education_score: Decimal,
        projects_score: Decimal,
        experience_score: Decimal,
    ) -> list[str]:
        weaknesses: list[str] = []

        if profile_score < Decimal("20"):
            weaknesses.append("Profile section is incomplete.")

        if skills_score < Decimal("20"):
            weaknesses.append("Important backend skills are missing.")

        if education_score == Decimal("0"):
            weaknesses.append("Education section is missing.")

        if projects_score < Decimal("20"):
            weaknesses.append("Projects section needs improvement.")

        if experience_score < Decimal("15"):
            weaknesses.append("Experience section is weak or missing.")

        return weaknesses
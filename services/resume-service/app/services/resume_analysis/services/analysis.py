import time
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from functools import cached_property
from typing import Final
from uuid import UUID

from app.models.resume_analysis import ResumeAnalysis
from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_analysis import ResumeAnalysisRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface


ANALYSIS_VERSION: Final[str] = "v3"
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

PROFILE_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "full_name",
    "email",
    "phone",
    "linkedin_url",
)


@dataclass(frozen=True)
class _ScoreWeights:
    PROFILE: Decimal = Decimal("20")
    SKILLS: Decimal = Decimal("30")
    EDUCATION: Decimal = Decimal("15")
    PROJECTS: Decimal = Decimal("20")
    EXPERIENCE: Decimal = Decimal("15")

    def total(self) -> Decimal:
        return (
            self.PROFILE
            + self.SKILLS
            + self.EDUCATION
            + self.PROJECTS
            + self.EXPERIENCE
        )


W: Final[_ScoreWeights] = _ScoreWeights()


@dataclass(frozen=True)
class SectionScores:
    profile: Decimal
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
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
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

    present = sum(
        1
        for field in PROFILE_REQUIRED_FIELDS
        if getattr(profile, field, None)
    )

    return (points_each * Decimal(present)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def score_skills(skills) -> tuple[Decimal, tuple[str, ...], tuple[str, ...]]:
    resume_skills: set[str] = {
        skill.name.lower().strip()
        for skill in (skills or [])
        if getattr(skill, "name", None)
    }

    matched = tuple(sorted(REQUIRED_SKILLS & resume_skills))
    missing = tuple(sorted(REQUIRED_SKILLS - resume_skills))

    if not REQUIRED_SKILLS:
        return Decimal("0"), matched, missing

    score = (
        Decimal(len(matched))
        / Decimal(len(REQUIRED_SKILLS))
        * W.SKILLS
    )

    return (
        score.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        matched,
        missing,
    )


def score_education(education) -> Decimal:
    return W.EDUCATION if education else Decimal("0")


def score_projects(projects) -> Decimal:
    count = len(projects or [])

    if count == 0:
        return Decimal("0")

    if count < PROJECTS_THRESHOLD:
        return (W.PROJECTS / Decimal("2")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    return W.PROJECTS


def score_experience(experiences) -> Decimal:
    return W.EXPERIENCE if experiences else FRESHER_BASELINE_SCORE


def build_section_scores(
    profile,
    skills,
    education,
    projects,
    experiences,
) -> SectionScores:
    skills_score, matched, missing = score_skills(skills)

    return SectionScores(
        profile=score_profile(profile),
        skills=skills_score,
        education=score_education(education),
        projects=score_projects(projects),
        experience=score_experience(experiences),
        matched_skills=matched,
        missing_skills=missing,
    )


def _profile_complete(scores: SectionScores) -> bool:
    return scores.profile >= W.PROFILE


def _skills_strong(scores: SectionScores) -> bool:
    return scores.skills >= (W.SKILLS * Decimal("0.67"))


def generate_suggestions(scores: SectionScores) -> list[str]:
    suggestions: list[str] = []

    if not _profile_complete(scores):
        suggestions.append(
            "Complete your profile: add full name, email, phone, and LinkedIn URL."
        )

    if scores.missing_skills:
        suggestions.append(
            f"Add these in-demand backend skills: {', '.join(scores.missing_skills)}."
        )

    if scores.education == Decimal("0"):
        suggestions.append(
            "Add your education details such as degree, institution, and graduation year."
        )

    if scores.projects < W.PROJECTS:
        suggestions.append(
            f"Include at least {PROJECTS_THRESHOLD} technical projects with tech stack and measurable impact."
        )

    if scores.experience < W.EXPERIENCE:
        suggestions.append(
            "Add internship, freelance, open-source, or practical project experience."
        )

    return suggestions


def generate_strengths(scores: SectionScores) -> list[str]:
    strengths: list[str] = []

    if _profile_complete(scores):
        strengths.append("Profile section is fully filled out.")

    if _skills_strong(scores):
        strengths.append(
            f"Strong backend skill coverage ({len(scores.matched_skills)}/{len(REQUIRED_SKILLS)} required skills matched)."
        )

    if scores.education > Decimal("0"):
        strengths.append("Education details are present.")

    if scores.projects >= W.PROJECTS:
        strengths.append(f"Has {PROJECTS_THRESHOLD}+ technical projects showcased.")

    if scores.experience >= W.EXPERIENCE:
        strengths.append("Work or internship experience is documented.")

    return strengths


def generate_weaknesses(scores: SectionScores) -> list[str]:
    weaknesses: list[str] = []

    if not _profile_complete(scores):
        weaknesses.append("Profile is incomplete — missing contact or LinkedIn info.")

    if not _skills_strong(scores):
        missing = ", ".join(scores.missing_skills) if scores.missing_skills else "none detected"
        weaknesses.append(f"Key backend skills missing: {missing}.")

    if scores.education == Decimal("0"):
        weaknesses.append("Education section is absent.")

    if scores.projects < W.PROJECTS:
        weaknesses.append("Insufficient technical projects to stand out to recruiters.")

    if scores.experience < W.EXPERIENCE:
        weaknesses.append("Limited or no professional/internship experience listed.")

    return weaknesses


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

        scores = build_section_scores(
            profile=profile,
            skills=skills,
            education=education,
            projects=projects,
            experiences=experiences,
        )

        analysis_time_ms = int((time.perf_counter() - start_time) * 1000)

        analysis = ResumeAnalysis(
            resume_id=resume_id,
            overall_score=scores.overall,
            profile_score=scores.profile,
            skills_score=scores.skills,
            education_score=scores.education,
            projects_score=scores.projects,
            experience_score=scores.experience,
            resume_completeness=scores.overall,
            keyword_match_percentage=scores.keyword_match_percentage,
            matched_skills=list(scores.matched_skills),
            missing_skills=list(scores.missing_skills),
            suggestions=generate_suggestions(scores),
            strengths=generate_strengths(scores),
            weaknesses=generate_weaknesses(scores),
            analysis_version=ANALYSIS_VERSION,
            analysis_time_ms=analysis_time_ms,
        )

        return await self.analysis_repo.create(analysis)

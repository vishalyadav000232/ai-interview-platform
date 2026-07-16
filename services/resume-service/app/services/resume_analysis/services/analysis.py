import time
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from functools import cached_property
from typing import Final
from uuid import UUID

from app.models.resume_analysis import ResumeAnalysis
from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_analysis import (
    ResumeAnalysisRepositoryInterface,
)
from app.repository.interface.resume_profile import (
    ResumeProfileRepositoryInterface,
)
from app.repository.interface.resume_skill import (
    ResumeSkillRepositoryInterface,
)
from app.repository.interface.resume_education import (
    ResumeEducationRepositoryInterface,
)
from app.repository.interface.resume_project import (
    ResumeProjectRepositoryInterface,
)
from app.repository.interface.resume_expriennc import (
    ResumeExprienceRepositoryInteraface,
)


ANALYSIS_VERSION: Final[str] = "v4"

FRESHER_BASELINE_SCORE: Final[Decimal] = Decimal("5")

PROJECTS_THRESHOLD: Final[int] = 2


REQUIRED_SKILLS: Final[frozenset[str]] = frozenset(
    {
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
)


SKILL_ALIASES: Final[dict[str, str]] = {
    "fast api": "fastapi",
    "fast-api": "fastapi",

    "postgres": "postgresql",
    "postgre sql": "postgresql",
    "postgres sql": "postgresql",

    "rest apis": "rest api",
    "rest-api": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",

    "git hub": "github",

    "json web token": "jwt",
    "json web tokens": "jwt",
    "jwt token": "jwt",

    "structured query language": "sql",
}


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
        raw_score = (
            self.profile
            + self.skills
            + self.education
            + self.projects
            + self.experience
        )

        return min(
            raw_score,
            Decimal("100"),
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @cached_property
    def keyword_match_percentage(self) -> Decimal:
        if not REQUIRED_SKILLS:
            return Decimal("0")

        percentage = (
            Decimal(len(self.matched_skills))
            / Decimal(len(REQUIRED_SKILLS))
            * Decimal("100")
        )

        return percentage.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


def normalize_text(value: str) -> str:
    return " ".join(
        value.strip().lower().split()
    )


def normalize_skill_name(value: str) -> str:
    normalized_value = normalize_text(value)

    return SKILL_ALIASES.get(
        normalized_value,
        normalized_value,
    )


def extract_skill_name(skill: object) -> str | None:
    raw_skill_name = (
        getattr(skill, "name", None)
        or getattr(skill, "skill_name", None)
        or getattr(skill, "normalized_name", None)
        or getattr(skill, "title", None)
    )

    if not raw_skill_name:
        return None

    normalized_skill = normalize_skill_name(
        str(raw_skill_name)
    )

    return normalized_skill or None


def score_profile(profile: object | None) -> Decimal:
    if profile is None:
        return Decimal("0")

    points_per_field = (
        W.PROFILE
        / Decimal(len(PROFILE_REQUIRED_FIELDS))
    )

    present_fields = sum(
        1
        for field_name in PROFILE_REQUIRED_FIELDS
        if getattr(profile, field_name, None)
    )

    score = (
        points_per_field
        * Decimal(present_fields)
    )

    return score.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def score_skills(
    skills,
) -> tuple[
    Decimal,
    tuple[str, ...],
    tuple[str, ...],
]:
    resume_skills: set[str] = set()

    for skill in skills or []:
        skill_name = extract_skill_name(skill)

        if skill_name:
            resume_skills.add(skill_name)

    matched_skills = tuple(
        sorted(
            REQUIRED_SKILLS.intersection(
                resume_skills
            )
        )
    )

    missing_skills = tuple(
        sorted(
            REQUIRED_SKILLS.difference(
                resume_skills
            )
        )
    )

    if not REQUIRED_SKILLS:
        return (
            Decimal("0"),
            matched_skills,
            missing_skills,
        )

    score = (
        Decimal(len(matched_skills))
        / Decimal(len(REQUIRED_SKILLS))
        * W.SKILLS
    )

    return (
        score.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        ),
        matched_skills,
        missing_skills,
    )


def score_education(education) -> Decimal:
    if education is None:
        return Decimal("0")

    if isinstance(
        education,
        (list, tuple, set),
    ):
        return (
            W.EDUCATION
            if len(education) > 0
            else Decimal("0")
        )

    return W.EDUCATION


def score_projects(projects) -> Decimal:
    project_count = len(projects or [])

    if project_count == 0:
        return Decimal("0")

    if project_count < PROJECTS_THRESHOLD:
        return (
            W.PROJECTS
            / Decimal("2")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    return W.PROJECTS


def score_experience(experiences) -> Decimal:
    if experiences:
        return W.EXPERIENCE

    return FRESHER_BASELINE_SCORE


def build_section_scores(
    profile,
    skills,
    education,
    projects,
    experiences,
) -> SectionScores:
    (
        skills_score,
        matched_skills,
        missing_skills,
    ) = score_skills(skills)

    return SectionScores(
        profile=score_profile(profile),
        skills=skills_score,
        education=score_education(education),
        projects=score_projects(projects),
        experience=score_experience(experiences),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )


def _profile_complete(
    scores: SectionScores,
) -> bool:
    return scores.profile >= W.PROFILE


def _skills_strong(
    scores: SectionScores,
) -> bool:
    minimum_score = (
        W.SKILLS
        * Decimal("0.67")
    )

    return scores.skills >= minimum_score


def generate_suggestions(
    scores: SectionScores,
) -> list[str]:
    suggestions: list[str] = []

    if not _profile_complete(scores):
        suggestions.append(
            "Complete your profile: add full name, "
            "email, phone, and LinkedIn URL."
        )

    if scores.missing_skills:
        suggestions.append(
            "Add these relevant backend skills "
            "only if you genuinely know them: "
            f"{', '.join(scores.missing_skills)}."
        )

    if scores.education == Decimal("0"):
        suggestions.append(
            "Add education details such as degree, "
            "institution, and graduation year."
        )

    if scores.projects < W.PROJECTS:
        suggestions.append(
            f"Include at least {PROJECTS_THRESHOLD} "
            "technical projects with tech stack, "
            "your contribution, and measurable impact."
        )

    if scores.experience < W.EXPERIENCE:
        suggestions.append(
            "Add internship, freelance, open-source, "
            "or practical project experience."
        )

    return suggestions


def generate_strengths(
    scores: SectionScores,
) -> list[str]:
    strengths: list[str] = []

    if _profile_complete(scores):
        strengths.append(
            "Profile section is fully filled out."
        )

    if _skills_strong(scores):
        strengths.append(
            "Strong backend skill coverage "
            f"({len(scores.matched_skills)}/"
            f"{len(REQUIRED_SKILLS)} required skills matched)."
        )

    if scores.education > Decimal("0"):
        strengths.append(
            "Education details are present."
        )

    if scores.projects >= W.PROJECTS:
        strengths.append(
            f"Has {PROJECTS_THRESHOLD}+ "
            "technical projects showcased."
        )

    if scores.experience >= W.EXPERIENCE:
        strengths.append(
            "Work, internship, or practical "
            "experience is documented."
        )

    return strengths


def generate_weaknesses(
    scores: SectionScores,
) -> list[str]:
    weaknesses: list[str] = []

    if not _profile_complete(scores):
        weaknesses.append(
            "Profile is incomplete — missing contact "
            "or LinkedIn information."
        )

    if not _skills_strong(scores):
        if scores.missing_skills:
            weaknesses.append(
                "Key backend skills missing: "
                f"{', '.join(scores.missing_skills)}."
            )
        else:
            weaknesses.append(
                "Backend skill coverage is below "
                "the recommended level."
            )

    if scores.education == Decimal("0"):
        weaknesses.append(
            "Education section is absent."
        )

    if scores.projects < W.PROJECTS:
        weaknesses.append(
            "Insufficient technical projects "
            "to stand out to recruiters."
        )

    if scores.experience < W.EXPERIENCE:
        weaknesses.append(
            "Limited or no professional or "
            "internship experience is listed."
        )

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

    async def analyze_resume(
        self,
        resume_id: UUID,
    ) -> ResumeAnalysis:
        start_time = time.perf_counter()

        resume = await self.resume_repo.get_by_id(
            resume_id
        )

        if resume is None:
            raise ValueError(
                "Resume not found"
            )

        profile = (
            await self.profile_repo.get_by_resume_id(
                resume_id
            )
        )

        skills = (
            await self.skill_repo.get_by_resume_id(
                resume_id
            )
        )

        education = (
            await self.education_repo.get_by_resume_id(
                resume_id
            )
        )

        projects = (
            await self.project_repo.get_by_resume_id(
                resume_id
            )
        )

        experiences = (
            await self.experience_repo.get_by_resume_id(
                resume_id
            )
        )

        scores = build_section_scores(
            profile=profile,
            skills=skills,
            education=education,
            projects=projects,
            experiences=experiences,
        )

        analysis_time_ms = int(
            (
                time.perf_counter()
                - start_time
            )
            * 1000
        )

        analysis_data = {
            "overall_score": scores.overall,
            "profile_score": scores.profile,
            "skills_score": scores.skills,
            "education_score": scores.education,
            "projects_score": scores.projects,
            "experience_score": scores.experience,
            "resume_completeness": scores.overall,
            "keyword_match_percentage": (
                scores.keyword_match_percentage
            ),
            "matched_skills": list(
                scores.matched_skills
            ),
            "missing_skills": list(
                scores.missing_skills
            ),
            "suggestions": generate_suggestions(
                scores
            ),
            "strengths": generate_strengths(
                scores
            ),
            "weaknesses": generate_weaknesses(
                scores
            ),
            "analysis_version": ANALYSIS_VERSION,
            "analysis_time_ms": analysis_time_ms,
        }

        existing_analysis = (
            await self.analysis_repo.get_latest_by_resume_id(
                resume_id
            )
        )

        if existing_analysis is not None:
            return await self.analysis_repo.update(
                obj=existing_analysis,
                data=analysis_data,
            )

        analysis = ResumeAnalysis(
            resume_id=resume_id,
            **analysis_data,
        )

        return await self.analysis_repo.create(
            obj=analysis,
        )




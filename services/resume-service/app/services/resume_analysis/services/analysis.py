




import time
from decimal import Decimal
from uuid import UUID

from app.models.resume_analysis import ResumeAnalysis
from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_analysis import ResumeAnalysisRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface


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
import logging
from pathlib import Path
from uuid import UUID

from app.core.exceptions.exception import (
    EmptyResumeTextException,
    ResumeParsedDataInvalidException,
    ResumeParsingException,
    ResumeTextExtractionException,
)
from app.models.resume_profile import ResumeProfile
from app.models.resume_project import ResumeProject
from app.models.resume_education import ResumeEducation
from app.models.resume_skills import ResumeSkill
from app.models.resume_exprience import ResumeExperience

from app.repository.interface.resume import ResumeRepositoryInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface

from app.services.parser.interface.resume_parser import ResumeParserInterface
from app.services.parser.interface.resume_text_extractor import (
    ResumeTextExtractorInterface,
)


logger = logging.getLogger(__name__)


class ResumeParsingService:
    def __init__(
        self,
        resume_repo: ResumeRepositoryInterface,
        text_extractor: ResumeTextExtractorInterface,
        resume_parser: ResumeParserInterface,
        resume_profile_repo: ResumeProfileRepositoryInterface,
        skill_repo: ResumeSkillRepositoryInterface,
        edu_repo: ResumeEducationRepositoryInterface,
        project_repo: ResumeProjectRepositoryInterface,
        exp_repo: ResumeExprienceRepositoryInteraface,
    ):
        self.resume_repo = resume_repo
        self.text_extractor = text_extractor
        self.resume_parser = resume_parser
        self.resume_profile_repo = resume_profile_repo
        self.skill_repo = skill_repo
        self.education_repo = edu_repo
        self.project_repo = project_repo
        self.exp_repo = exp_repo

    async def process_resume(
    self,
    resume_id: UUID,
    file_path: Path,
) -> None:
        logger.info(
            "Starting background resume parsing",
            extra={
                "resume_id": str(resume_id),
                "file_path": str(file_path),
            },
        )

        text = await self._extract_text(file_path)

        parsed_data = await self._parse_text(text)

        await self._save_parsed_data(
            resume_id=resume_id,
            parsed_data=parsed_data,
            parsed_text=text,
        )

        logger.info(
            "Background resume parsing completed",
            extra={
                "resume_id": str(resume_id),
                "skills_count": len(parsed_data.get("skills", [])),
                "education_count": len(parsed_data.get("educations", [])),
                "project_count": len(parsed_data.get("projects", [])),
                "experience_count": len(parsed_data.get("experiences", [])),
            },
        )

    async def _extract_text(self, file_path: Path) -> str:
        try:
            text = await self.text_extractor.extract_text(file_path)
        except Exception as exc:
            raise ResumeTextExtractionException() from exc

        if not text or not text.strip():
            raise EmptyResumeTextException()

        return text

    async def _parse_text(self, text: str) -> dict:
        try:
            parsed_data = await self.resume_parser.parse(text)
        except Exception as exc:
            logger.exception("Resume parser failed")
            raise ResumeParsingException() from exc

        if not isinstance(parsed_data, dict):
            raise ResumeParsedDataInvalidException()

        return parsed_data

    async def _save_parsed_data(
        self,
        resume_id: UUID,
        parsed_data: dict,
        parsed_text: str,
    ) -> None:
        try:
            profile = self._build_profile(resume_id, parsed_data)
            skills = self._build_skills(resume_id, parsed_data)
            educations = self._build_educations(resume_id, parsed_data)
            projects = self._build_projects(resume_id, parsed_data)
            experiences = self._build_experiences(resume_id, parsed_data)

            await self.resume_profile_repo.create(profile, commit=False)

            if skills:
                await self.skill_repo.bulk_create(skills, commit=False)

            if educations:
                await self.education_repo.bulk_create(educations, commit=False)

            if projects:
                await self.project_repo.bulk_create(projects, commit=False)

            if experiences:
                await self.exp_repo.bulk_create(experiences, commit=False)

            await self.resume_repo.update_parsed_text(
                resume_id=resume_id,
                parsed_text=parsed_text,
                commit=False,
            )



            await self.resume_repo.commit()

        except Exception as exc:
            await self.resume_repo.rollback()

            logger.exception(
                "Failed to save parsed resume data",
                extra={
                    "resume_id": str(resume_id),
                },
            )

            raise ResumeParsingException() from exc

    def _build_profile(
        self,
        resume_id: UUID,
        parsed_data: dict,
    ) -> ResumeProfile:
        parsed_profile = parsed_data.get("profile") or {}

        return ResumeProfile(
            resume_id=resume_id,
            full_name=parsed_profile.get("full_name"),
            email=parsed_profile.get("email"),
            phone=parsed_profile.get("phone"),
            linkedin_url=parsed_profile.get("linkedin_url"),
            github_url=parsed_profile.get("github_url"),
            professional_summary=parsed_profile.get("professional_summary"),
        )

    def _build_skills(
        self,
        resume_id: UUID,
        parsed_data: dict,
    ) -> list[ResumeSkill]:
        return [
            ResumeSkill(
                resume_id=resume_id,
                skill_name=skill,
            )
            for skill in parsed_data.get("skills", [])
            if skill
        ]

    def _build_educations(
        self,
        resume_id: UUID,
        parsed_data: dict,
    ) -> list[ResumeEducation]:
        return [
            ResumeEducation(
                resume_id=resume_id,
                degree=edu.get("degree"),
                institution=edu.get("institution"),
                field_of_study=edu.get("field_of_study"),
                start_year=edu.get("start_year"),
                end_year=edu.get("end_year"),
                grade=edu.get("grade"),
            )
            for edu in parsed_data.get("educations", [])
            if isinstance(edu, dict)
        ]

    def _build_projects(
        self,
        resume_id: UUID,
        parsed_data: dict,
    ) -> list[ResumeProject]:
        return [
            ResumeProject(
                resume_id=resume_id,
                project_name=proj.get("project_name"),
                technologies=proj.get("technologies"),
                project_url=proj.get("project_url"),
                description=proj.get("description"),
            )
            for proj in parsed_data.get("projects", [])
            if isinstance(proj, dict)
        ]

    def _build_experiences(
        self,
        resume_id: UUID,
        parsed_data: dict,
    ) -> list[ResumeExperience]:
        return [
            ResumeExperience(
                resume_id=resume_id,
                company_name=exp.get("company_name"),
                job_title=exp.get("job_title"),

                location=exp.get("location"),
                start_date=exp.get("start_date"),
                end_date=exp.get("end_date"),

                description=exp.get("description"),
            )
            for exp in parsed_data.get("experiences", [])
            if isinstance(exp, dict)
        ]

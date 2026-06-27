import logging
from pathlib import Path
from uuid import UUID

from app.core.exceptions.exception import (
    EmptyResumeTextException,
    ResumeException,
    ResumeParsedDataInvalidException,
    ResumeParsingException,
    ResumeTextExtractionException,
)


from app.models.resume import ResumeStatus
from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.parser.interface.resume_parser import ResumeParserInterface
from app.services.parser.interface.resume_text_extractor import ResumeTextExtractorInterface
from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface
from app.repository.interface.resume_project import ResumeProjectRepositoryInterface
from app.repository.interface.resume_expriennc import ResumeExprienceRepositoryInteraface

from app.models.resume_profile import ResumeProfile
from app.models.resume_project import ResumeProject
from app.models.resume_education import ResumeEducation
from app.models.resume_skills import ResumeSkill
from app.models.resume_exprience import ResumeExperience


logger = logging.getLogger(__name__)


class ResumeParsingService:
    def __init__(
        self,
        resume_repo: ResumeRepositoryInterface,
        text_extractor: ResumeTextExtractorInterface,
        resume_parser: ResumeParserInterface,
        resume_Profile_repo : ResumeProfileRepositoryInterface,
        skill_repo : ResumeSkillRepositoryInterface,
        edu_repo : ResumeEducationRepositoryInterface,
        project_repo : ResumeProjectRepositoryInterface,
        exp_repo : ResumeExprienceRepositoryInteraface,
        
    ):
        self.resume_repo = resume_repo
        self.text_extractor = text_extractor
        self.resume_parser = resume_parser
        self.resume_profile = resume_Profile_repo
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

        try:
            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.PROCESSING,
            )

            try:
                text = await self.text_extractor.extract_text(file_path)
            except Exception as exc:
                raise ResumeTextExtractionException() from exc

            if not text or not text.strip():
                raise EmptyResumeTextException()

            try:
                parsed_data = await self.resume_parser.parse(text)
                
                print("this is the parse data --> " , parsed_data)
                
                parsed_profile = parsed_data.get("profile")
                profile = ResumeProfile(
                        resume_id=resume_id,
                        full_name=parsed_profile.get("full_name"),
                        email=parsed_profile.get("email"),
                        phone=parsed_profile.get("phone"),
                        linkedin_url=parsed_profile.get("linkedin_url"),
                        github_url=parsed_profile.get("github_url"),
                        professional_summary = parsed_profile.get("professional_summary")
                    )

                
                await self.resume_profile.create(profile)
                
                
                skills = [
                 ResumeSkill(
                        resume_id=resume_id,
                        skill_name=skill,
                    )
                    for skill in parsed_data.get("skills", [])
                ]

                await self.skill_repo.bulk_create(skills)
                
                print("EDUCATION DATA:", parsed_data.get("educations"))
                
                educations = [
                    ResumeEducation(
                        resume_id=resume_id,
                        degree=edu.get("degree"),
                        institution=edu.get("institution"),
                        start_year=edu.get("start_year"),
                        end_year=edu.get("end_year"),
                    )
                    for edu in parsed_data.get("educations", [])
                ]

                await self.education_repo.bulk_create(educations)
                
                
                
                projects = [
                    ResumeProject(
                        resume_id = resume_id,
                        project_name = proj.get("project_name"),
                        technologies = proj.get("technologies"),
                        project_url = proj.get("project_url"),
                        description = proj.get("description")
                        
                    ) for proj in parsed_data.get("projects" , [])
                ]
                
                await self.project_repo.bulk_create(projects)
                
                
                print("thhis is tje experiences", parsed_data.get("experiences" , []))
                

                experiences = [
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
            ]

                if experiences:
                    await self.exp_repo.bulk_create(experiences)
                                
                
                
                
            except Exception as exc:
                raise ResumeParsingException() from exc

            if not isinstance(parsed_data, dict):
                raise ResumeParsedDataInvalidException()

            await self.resume_repo.update_parsed_text(
                resume_id=resume_id,
                parsed_text=text,
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.ANALYZED,
            )

            logger.info(
                "Background resume parsing completed",
                extra={
                    "resume_id": str(resume_id),
                    "skills_count": len(parsed_data.get("skills", [])),
                },
            )

        except ResumeException as exc:
            logger.warning(
                "Resume parsing failed",
                extra={
                    "resume_id": str(resume_id),
                    "file_path": str(file_path),
                    "error_code": exc.error_code,
                    "error": exc.message,
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason=exc.message,
            )

        except Exception:
            logger.exception(
                "Unexpected resume parsing error",
                extra={
                    "resume_id": str(resume_id),
                    "file_path": str(file_path),
                },
            )

            await self.resume_repo.update_status(
                resume_id=resume_id,
                status=ResumeStatus.FAILED,
                failure_reason="Unexpected resume parsing error",
            )
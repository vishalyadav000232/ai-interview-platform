import logging
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status

from app.models.resume import Resume
from app.repository.interface.resume import ResumeRepositoryInterface
from app.services.interface.resume import ResumeServiceInterface

from app.repository.interface.resume_education import ResumeEducationRepositoryInterface
from app.repository.interface.resume_profile import ResumeProfileRepositoryInterface
from app.repository.interface.resume_skill import ResumeSkillRepositoryInterface



logger = logging.getLogger(__name__)


class ResumeService(ResumeServiceInterface):
    def __init__(self,
                resume_repo: ResumeRepositoryInterface,
                profile_repo: ResumeProfileRepositoryInterface,
                skill_repo: ResumeSkillRepositoryInterface,
                education_repo: ResumeEducationRepositoryInterface,
                 ):
        self.resume_repo = resume_repo
        self.upload_dir = Path("uploads/resumes")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_repo = profile_repo
        self.skill_repo = skill_repo
        self.education_repo = education_repo

    async def upload_resume(
        self,
        user_id: UUID,
        file: UploadFile,
    ) -> Resume:
        allowed_files = {
            "application/pdf": "pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        }

        if file.content_type not in allowed_files:
            logger.warning(
                "Invalid resume file type",
                extra={
                    "user_id": str(user_id),
                    "content_type": file.content_type,
                },
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and DOCX files are allowed",
            )

        file_bytes = await file.read()

        max_size = 5 * 1024 * 1024

        if len(file_bytes) > max_size:
            logger.warning(
                "Resume file size exceeded",
                extra={
                    "user_id": str(user_id),
                    "file_size": len(file_bytes),
                    "max_size": max_size,
                },
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 5MB",
            )

        file_extension = allowed_files[file.content_type]
        storage_file_name = f"{uuid4()}.{file_extension}"
        file_path = self.upload_dir / storage_file_name

        try:
            with open(file_path, "wb") as f:
                f.write(file_bytes)

            resume = Resume(
                user_id=user_id,
                original_file_name=file.filename,
                storage_file_name=storage_file_name,
                file_url=str(file_path),
                file_type=file_extension,
                file_size=len(file_bytes),
                upload_source="local",
            )

            return await self.resume_repo.create(resume=resume)

        except Exception:
            logger.exception(
                "Failed to upload resume",
                extra={
                    "user_id": str(user_id),
                    "file_name": file.filename,
                },
            )

            raise
    
    async def get_resume(
    self,
    user_id: UUID,
    resume_id: UUID,
) -> Resume | None:
        resume = await self.resume_repo.get_by_id(resume_id)

        if resume is None:
            return None

        if str(resume.user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resume",
            )

        return resume


    async def get_user_resumes(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        return await self.resume_repo.get_active_by_user_id(user_id)


    async def delete_resume(
        self,
        user_id: UUID,
        resume_id: UUID,
    ) -> bool:
        resume = await self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        if resume is None:
            return False

        return await self.resume_repo.soft_delete(resume_id)
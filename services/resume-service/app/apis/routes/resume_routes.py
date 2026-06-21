from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.services.interface.resume import ResumeServiceInterface
from app.schemas.resume import ResumeDataResponse  , ResumeListResponse



from app.dependencies.service_deps import get_resume_service

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=ResumeDataResponse,
)
async def upload_resume(
    user_id: UUID,
    file: UploadFile = File(...),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    resume = await resume_service.upload_resume(
        user_id=user_id,
        file=file,
    )

    return {
        "success": True,
        "message": "Resume uploaded successfully",
        "data": resume,
    }


@router.get(
    "/user/{user_id}",
    response_model=ResumeListResponse,
)
async def get_user_resumes(
    user_id: UUID,
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    resumes = await resume_service.get_user_resumes(user_id)

    return {
        "success": True,
        "message": "Resumes fetched successfully",
        "data": resumes,
    }
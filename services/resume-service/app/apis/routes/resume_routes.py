from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status , Header , HTTPException 
from pathlib import Path 

from fastapi.responses import FileResponse

from app.services.interface.resume import ResumeServiceInterface
from app.schemas.resume import ResumeDataResponse  , ResumeListResponse


from app.dependencies.auth import get_current_user_id


from app.dependencies.service_deps import get_resume_service

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=ResumeDataResponse,
)
async def upload_resume(
    x_request_id: UUID = Header(...),
    file: UploadFile = File(...),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    resume = await resume_service.upload_resume(
        user_id=x_request_id,
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


@router.get("/my-resume"  , status_code=status.HTTP_200_OK , response_model=ResumeListResponse)
async def get_my_resume(
    user_id :UUID = Depends(get_current_user_id),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    
    resumes = await resume_service.get_user_resumes(user_id=user_id)
    
    return{
        "success": True,
        "message": "Resumes fetched successfully",
        "data": resumes,
    }

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status



@router.get(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResumeDataResponse
)
async def get_resume(
    resume_id: UUID,
    user_id :UUID = Depends(get_current_user_id),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    print(resume_id)
    resume = await resume_service.get_resume(resume_id=resume_id , user_id=user_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    

    return {
        "success": True,
        "message": "Resume fetched successfully",
        "data": resume,
    }


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_resume(
    resume_id: UUID,
    user_id :UUID = Depends(get_current_user_id),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    resume = await resume_service.get_resume(resume_id=resume_id , user_id=user_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if str(resume.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this resume",
        )

    deleted = await resume_service.delete_resume(resume_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume could not be deleted",
        )

    return {
        "success": True,
        "message": "Resume deleted successfully",
    }
    

@router.get("/download/{resume_id}")
async def download_resume(
    resume_id: UUID,
    user_id :UUID = Depends(get_current_user_id),
    resume_service: ResumeServiceInterface = Depends(get_resume_service),
):
    resume = await resume_service.get_resume(resume_id=resume_id , user_id=user_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if resume.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to download this resume",
        )
        
    print("resume.file_url =", resume.file_url)
    print("absolute path =", Path(resume.file_url).resolve())
    print("exists =", Path(resume.file_url).exists())

    file_path = Path(resume.file_url)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found",
        )

    return FileResponse(
        path=file_path,
        filename=resume.original_file_name,
        media_type="application/octet-stream",
    )
    
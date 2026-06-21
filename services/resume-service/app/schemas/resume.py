from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.resume import ResumeStatus


class ResumeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    user_id: UUID

    original_file_name: str
    file_url: str

    file_type: str
    file_size: int

    status: ResumeStatus

    created_at: datetime
    updated_at: datetime
    
class ResumeDataResponse(BaseModel):
    success : bool
    message : str
    data : ResumeResponse
    


from datetime import datetime

from pydantic import BaseModel


class UploadResult(BaseModel):
    resume_id: str
    original_filename: str
    stored_filename: str
    uploaded_at: datetime
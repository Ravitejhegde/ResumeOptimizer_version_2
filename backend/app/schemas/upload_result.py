from datetime import datetime

from pydantic import BaseModel


class UploadResult(BaseModel):
    id: str
    original_filename: str
    stored_filename: str
    uploaded_at: datetime
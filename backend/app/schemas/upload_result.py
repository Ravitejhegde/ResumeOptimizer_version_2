from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UploadResult(BaseModel):
    """
    Result returned after storing an uploaded file.

    Represents only physical storage information.

    Used by:
        - ResumeService
        - Document processing pipeline

    Does not contain:
        - Database IDs
        - User information
        - Workspace information
        - Resume lifecycle state
    """


    original_filename: str = Field(
        ...,
        description="Original filename uploaded by user",
        examples=[
            "resume.docx"
        ],
    )


    stored_filename: str = Field(
        ...,
        description="Generated safe filename stored on disk",
        examples=[
            "8f4c3a2d.docx"
        ],
    )


    file_path: str = Field(
        ...,
        description="Absolute or relative storage path",
        examples=[
            "storage/resumes/8f4c3a2d.docx"
        ],
    )


    file_size: int = Field(
        ...,
        ge=1,
        description="File size in bytes",
    )


    uploaded_at: datetime = Field(
        ...,
        description="Timestamp when file was stored",
    )
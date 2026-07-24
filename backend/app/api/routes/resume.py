from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.upload.upload_service import UploadService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Temporary guest upload.
    """

    service = UploadService(db)

    resume = await service.upload_resume(
        workspace_id=1,
        file=file,
    )

    return {
        "resume_id": resume.id,
        "filename": resume.original_filename,
        "stored_filename": resume.stored_filename,
        "status": resume.status,
    }
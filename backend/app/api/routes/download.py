from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings

router = APIRouter(
    prefix="/download",
    tags=["Download"],
)


@router.get("/{filename}")
def download_resume(filename: str):

    file_path = settings.EXPORT_PATH / filename

    if not Path(file_path).exists():

        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(

        path=file_path,

        filename=filename,

        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",

    )
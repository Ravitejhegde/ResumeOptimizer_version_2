from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.get("/download/{filename}")
def download_resume(
    filename: str,
):

    # -----------------------------------------
    # Prevent path traversal
    # -----------------------------------------

    filename = Path(filename).name

    file_path = (
        settings.EXPORT_DIR
        / filename
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Optimized resume not found.",
        )

    return FileResponse(

        path=file_path,

        filename=filename,

        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),

        headers={
            "Cache-Control": "no-cache",
        },

    )
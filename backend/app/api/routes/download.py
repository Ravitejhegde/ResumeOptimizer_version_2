from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.download.download_service import (
    DownloadService,
)


router = APIRouter(
    prefix="/download",
    tags=["Download"],
)


@router.get("/{resume_output_id}")
def download_resume(
    resume_output_id: str,
    db: Session = Depends(get_db),
):

    service = DownloadService(db)

    try:

        file_path = service.get_file(
            resume_output_id
        )

        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
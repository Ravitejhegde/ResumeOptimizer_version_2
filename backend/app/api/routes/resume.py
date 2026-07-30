from __future__ import annotations


from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session


from app.database.session import get_db

from app.database.models.user import User


from app.api.dependencies.current_user import (
    get_current_user,
)


from app.services.resume.resume_service import (
    ResumeService,
)


from app.services.workspace.workspace_service import (
    WorkspaceService,
)



router = APIRouter(
    prefix="/resume",
    tags=[
        "Resume"
    ],
)



@router.post(
    "/upload",
)
async def upload_resume(
    file: UploadFile = File(...),

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Upload resume for authenticated user.
    """


    workspace_service = WorkspaceService(
        db
    )


    workspace = (
        workspace_service.get_user_workspace(
            current_user.id
        )
    )


    if workspace is None:

        workspace = (
            workspace_service.create_workspace(
                user_id=current_user.id
            )
        )



    service = ResumeService(
        db
    )


    try:

        resume = await service.upload_resume(
            workspace_id=workspace.id,
            file=file,
        )


        return {

            "resume_id": resume.id,

            "filename": resume.original_filename,

            "status": resume.status,

        }



    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume upload failed.",
        ) from exc
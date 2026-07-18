from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.exceptions import FileValidationError, StorageError
from app.schemas.response import ApiResponse
from app.services.storage.file_storage import FileStorage
from app.services.validation.file_validator import FileValidator

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/upload", response_model=ApiResponse)
async def upload_resume(file: UploadFile = File(...)):
    try:
        await FileValidator.validate(file)

        result = await FileStorage.save(file)

        return ApiResponse(
            success=True,
            message="Resume uploaded successfully.",
            data=result,
        )

    except FileValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except StorageError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
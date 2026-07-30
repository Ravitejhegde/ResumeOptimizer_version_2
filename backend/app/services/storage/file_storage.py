from __future__ import annotations

import logging

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import StorageError

from app.schemas.upload_result import UploadResult


logger = logging.getLogger(__name__)


class FileStorage:
    """
    Handles physical file storage.

    Responsibilities:
        - Validate uploaded files.
        - Generate unique filenames.
        - Store files on disk.
        - Return file metadata.

    Does not:
        - Create database records.
        - Manage users.
        - Manage resume lifecycle.
        - Parse documents.
    """


    ALLOWED_EXTENSIONS = {
        ".docx",
        ".pdf",
    }


    CHUNK_SIZE = 1024 * 1024



    # ======================================================
    # Save Upload
    # ======================================================

    @classmethod
    async def save(
        cls,
        file: UploadFile,
    ) -> UploadResult:
        """
        Save uploaded file and return metadata.
        """

        destination: Path | None = None


        try:

            # ----------------------------------
            # Validate filename
            # ----------------------------------

            if not file.filename:

                raise StorageError(
                    "Filename missing."
                )


            extension = (
                Path(file.filename)
                .suffix
                .lower()
            )


            if extension not in cls.ALLOWED_EXTENSIONS:

                raise StorageError(
                    f"Unsupported file type: {extension}"
                )


            # ----------------------------------
            # Prepare directory
            # ----------------------------------

            settings.RESUME_STORAGE_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )


            # ----------------------------------
            # Generate filename
            # ----------------------------------

            stored_filename = (
                f"{uuid4()}{extension}"
            )


            destination = (
    settings.RESUME_STORAGE_DIR
    /
    stored_filename
)


            # ----------------------------------
            # Write file
            # ----------------------------------

            file_size = 0


            with destination.open(
                "wb"
            ) as buffer:


                while True:

                    chunk = await file.read(
                        cls.CHUNK_SIZE
                    )


                    if not chunk:

                        break


                    buffer.write(
                        chunk
                    )


                    file_size += len(
                        chunk
                    )



            # ----------------------------------
            # Validate content
            # ----------------------------------

            if file_size == 0:

                raise StorageError(
                    "Uploaded file is empty."
                )



            # Reset upload stream

            await file.seek(
                0
            )



            logger.info(
                "Stored file: %s (%s bytes)",
                stored_filename,
                file_size,
            )



            return UploadResult(

                original_filename=(
                    file.filename
                ),

                stored_filename=(
                    stored_filename
                ),

                file_path=str(
                    destination
                ),

                file_size=file_size,

                uploaded_at=datetime.now(
                    timezone.utc
                ),

            )



        except StorageError:

            # cleanup failed upload

            if destination and destination.exists():

                destination.unlink()


            raise



        except Exception as exc:


            logger.exception(
                "File storage failed"
            )


            if destination and destination.exists():

                destination.unlink()


            raise StorageError(
                "Failed to store uploaded file."
            ) from exc
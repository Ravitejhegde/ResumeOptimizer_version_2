from __future__ import annotations

import logging
from pathlib import Path

from fastapi import UploadFile

from app.services.storage.file_storage import (
    FileStorage,
)


logger = logging.getLogger(__name__)


class StorageService:
    """
    Application storage service.

    Responsibilities:
        - Save uploaded files.
        - Delete stored files.
        - Check file existence.
        - Get file size.

    Does not:
        - Manage database.
        - Manage resume records.
        - Create resume entities.
    """


    def __init__(self) -> None:

        self.files = FileStorage()



    # ======================================================
    # Save
    # ======================================================

    async def save_upload(
        self,
        file: UploadFile,
    ):
        """
        Save uploaded file.

        Returns:
            StoredFile metadata.
        """


        stored = await self.files.save(
            file
        )


        logger.info(
            "File stored: %s",
            stored.stored_filename,
        )


        return stored



    # ======================================================
    # Exists
    # ======================================================

    def exists(
        self,
        file_path: str,
    ) -> bool:

        return Path(
            file_path
        ).exists()



    # ======================================================
    # Size
    # ======================================================

    def get_size(
        self,
        file_path: str,
    ) -> int:

        path = Path(
            file_path
        )


        if not path.exists():

            return 0


        return path.stat().st_size



    # ======================================================
    # Delete
    # ======================================================

    def delete(
        self,
        file_path: str,
    ) -> bool:
        """
        Delete stored file.
        """


        path = Path(
            file_path
        )


        if not path.exists():

            logger.warning(
                "File not found: %s",
                file_path,
            )

            return False


        path.unlink()


        logger.info(
            "File deleted: %s",
            file_path,
        )


        return True
from sqlalchemy.orm import Session

from app.database.models.download import Download
from app.database.repositories.base_repository import (
    BaseRepository,
)


class DownloadRepository(
    BaseRepository[Download],
):
    """
    Repository for Download operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            Download,
            db,
        )

    def get_by_resume_output(
        self,
        resume_output_id: str,
    ) -> list[Download]:

        return (
            self.db.query(
                Download
            )
            .filter(
                Download.resume_output_id
                == resume_output_id
            )
            .order_by(
                Download.downloaded_at.desc()
            )
            .all()
        )

    def count_downloads(
        self,
        resume_output_id: str,
    ) -> int:

        return (
            self.db.query(
                Download
            )
            .filter(
                Download.resume_output_id
                == resume_output_id
            )
            .count()
        )
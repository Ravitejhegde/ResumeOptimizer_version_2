from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.guest_resume import GuestResume


class GuestResumeRepository:
    """
    Database access for guest resumes.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    def create(
        self,
        resume: GuestResume,
    ) -> GuestResume:
        """
        Persist a new guest resume.
        """

        self.db.add(resume)
        self.db.flush()

        return resume

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_id(
        self,
        resume_id: str,
    ) -> GuestResume | None:
        """
        Return a guest resume by ID.
        """

        return (
            self.db.query(GuestResume)
            .filter(
                GuestResume.id == resume_id,
            )
            .first()
        )

    def get_by_guest(
        self,
        guest_id: str,
    ) -> list[GuestResume]:
        """
        Return all resumes belonging to a guest.
        """

        return (
            self.db.query(GuestResume)
            .filter(
                GuestResume.guest_id == guest_id,
            )
            .order_by(
                GuestResume.created_at.desc()
            )
            .all()
        )

    def count_by_guest(
        self,
        guest_id: str,
    ) -> int:
        """
        Return the number of resumes belonging to a guest.
        """

        return (
            self.db.query(GuestResume)
            .filter(
                GuestResume.guest_id == guest_id,
            )
            .count()
        )

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(
        self,
        resume: GuestResume,
    ) -> None:
        """
        Delete a guest resume record.
        """

        self.db.delete(resume)
        self.db.flush()
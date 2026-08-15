from __future__ import annotations

import logging
from pathlib import Path

from app.application.models.optimization_request import (
    OptimizationRequest,
)
from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)
from app.database.models.guest import Guest
from app.database.models.guest_resume import GuestResume
from app.guest.services.guest_usage_service import (
    GuestUsageService,
)


logger = logging.getLogger(__name__)


class GuestOptimizationService:
    """
    Coordinates guest resume optimization.

    Guest-specific rules live here.
    The actual resume optimization is delegated to the
    existing ResumeOptimizationService.
    """

    def __init__(self, db) -> None:
        self.db = db

        self.usage_service = GuestUsageService(db)

        self.optimization_service = (
            ResumeOptimizationService()
        )

    def optimize(
        self,
        guest: Guest,
        guest_resume: GuestResume,
        guest_session_id: str,
        job_description: str,
    ):
        """
        Optimize a guest resume.

        Usage is consumed only after successful optimization.
        """

        # --------------------------------------------------
        # Validate ownership
        # --------------------------------------------------

        if guest_resume.guest_id != guest.id:
            raise ValueError(
                "Guest resume does not belong to this guest."
            )

        # --------------------------------------------------
        # Validate session
        # --------------------------------------------------

        self.usage_service._get_valid_session(
            guest=guest,
            guest_session_id=guest_session_id,
        )

        # --------------------------------------------------
        # Check usage
        # --------------------------------------------------

        if not self.usage_service.can_optimize(guest):
            raise ValueError(
                "Guest optimization limit reached."
            )

        # --------------------------------------------------
        # Validate source file
        # --------------------------------------------------

        resume_path = Path(
            guest_resume.file_path
        )

        if not resume_path.exists():
            raise FileNotFoundError(
                "Guest resume file is no longer available."
            )

        # --------------------------------------------------
        # Output file
        # --------------------------------------------------

        output_path = (
            resume_path.parent
            / f"{resume_path.stem}_optimized.docx"
        )

        # --------------------------------------------------
        # Existing optimization engine
        # --------------------------------------------------

        request = OptimizationRequest(
            resume_path=str(resume_path),
            job_description=job_description,
            output_path=str(output_path),
        )

        try:
            result = (
                self.optimization_service.optimize(
                    request
                )
            )

            # --------------------------------------------------
            # Consume usage ONLY after success
            # --------------------------------------------------

            if not result.success:
                raise ValueError(
                    result.message
                )

            self.usage_service.consume_optimization(
                guest=guest,
                guest_session_id=guest_session_id,
            )

            return result

        except Exception:
            logger.exception(
                "Guest resume optimization failed: "
                "guest_resume_id=%s",
                guest_resume.id,
            )

            raise
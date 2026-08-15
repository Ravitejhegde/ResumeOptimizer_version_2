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
from app.database.models.referral import Referral
from app.guest.services.guest_usage_service import (
    GuestUsageService,
)
from app.referral.services.referral_service import (
    ReferralService,
)


logger = logging.getLogger(__name__)


class GuestOptimizationService:
    """
    Coordinates guest resume optimization.

    Guest-specific rules live here.
    The actual resume optimization is delegated to the
    existing ResumeOptimizationService.

    A successful first optimization by a referred guest
    completes the referral and grants the referrer
    two additional samples.
    """

    def __init__(self, db) -> None:
        self.db = db

        self.usage_service = GuestUsageService(db)

        self.referral_service = ReferralService(db)

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

        If this guest was referred and this is their first
        successful optimization, the referral is completed
        and the referrer receives two samples.
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
            # Optimization must succeed
            # --------------------------------------------------

            if not result.success:
                raise ValueError(
                    result.message
                )

            # --------------------------------------------------
            # Consume B's optimization
            # --------------------------------------------------

            self.usage_service.consume_optimization(
                guest=guest,
                guest_session_id=guest_session_id,
            )

            # --------------------------------------------------
            # Complete referral
            #
            # IMPORTANT:
            # This happens only after successful optimization.
            # --------------------------------------------------

            self._complete_referral_if_eligible(
                referred_guest=guest,
            )

            return result

        except Exception:
            logger.exception(
                "Guest resume optimization failed: "
                "guest_resume_id=%s",
                guest_resume.id,
            )

            raise

    # ==========================================================
    # Referral
    # ==========================================================

    def _complete_referral_if_eligible(
        self,
        referred_guest: Guest,
    ) -> None:
        """
        Complete and reward the referral belonging to this guest.

        Only a pending referral is eligible.

        If the guest was not referred, nothing happens.

        If the referral was already completed/rewarded,
        nothing happens.
        """

        referral = (
            self.db.query(Referral)
            .filter(
                Referral.referred_guest_id
                == referred_guest.id,
                Referral.status == "pending",
                Referral.reward_granted.is_(False),
            )
            .first()
        )

        if referral is None:
            return

        # ------------------------------------------------------
        # Complete referral
        # ------------------------------------------------------

        self.referral_service.complete_referral(
            referral,
        )

        # ------------------------------------------------------
        # Grant A's reward
        # ------------------------------------------------------

        self.referral_service.grant_reward(
            referral,
        )

        logger.info(
            "Referral completed and reward granted: "
            "referral_id=%s referred_guest_id=%s "
            "referrer_guest_id=%s",
            referral.id,
            referral.referred_guest_id,
            referral.referrer_guest_id,
        )
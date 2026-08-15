from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.referral import Referral


class ReferralRepository:
    """
    Database access for referral records.
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
        referral: Referral,
    ) -> Referral:
        """
        Persist a new referral.
        """

        self.db.add(referral)
        self.db.flush()

        return referral

    # ==========================================================
    # Queries
    # ==========================================================

    def get_by_id(
        self,
        referral_id: str,
    ) -> Referral | None:
        """
        Return a referral by its primary key.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.id == referral_id,
            )
            .first()
        )

    def get_by_referrer_and_referred(
        self,
        referrer_guest_id: str,
        referred_guest_id: str,
    ) -> Referral | None:
        """
        Return the referral relationship between
        two guests, if it exists.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
                Referral.referred_guest_id
                == referred_guest_id,
            )
            .first()
        )

    def get_by_referred_guest(
        self,
        referred_guest_id: str,
    ) -> Referral | None:
        """
        Return the referral that brought a guest
        into the application.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referred_guest_id
                == referred_guest_id,
            )
            .first()
        )

    def get_by_referrer(
        self,
        referrer_guest_id: str,
    ) -> list[Referral]:
        """
        Return all referrals created by a guest.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
            )
            .all()
        )

    # ==========================================================
    # Reward Queries
    # ==========================================================

    def get_unrewarded_by_referrer(
        self,
        referrer_guest_id: str,
    ) -> list[Referral]:
        """
        Return completed referrals that have not
        received their reward yet.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
                Referral.status == "completed",
                Referral.reward_granted.is_(False),
            )
            .all()
        )

    # ==========================================================
    # Update
    # ==========================================================

    def update(
        self,
        referral: Referral,
    ) -> Referral:
        """
        Persist changes to an existing referral.
        """

        self.db.flush()

        return referral
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
        Return a referral by ID.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.id == referral_id,
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
            .order_by(
                Referral.created_at.desc()
            )
            .all()
        )

    def get_by_referred(
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

    def get_by_referrer_and_referred(
        self,
        referrer_guest_id: str,
        referred_guest_id: str,
    ) -> Referral | None:
        """
        Return a specific referral relationship.
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

    # ==========================================================
    # Existence
    # ==========================================================

    def exists_between(
        self,
        referrer_guest_id: str,
        referred_guest_id: str,
    ) -> bool:
        """
        Return True when a referral relationship already exists.
        """

        return (
            self.db.query(Referral.id)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
                Referral.referred_guest_id
                == referred_guest_id,
            )
            .first()
            is not None
        )

    # ==========================================================
    # Counts
    # ==========================================================

    def count_by_referrer(
        self,
        referrer_guest_id: str,
    ) -> int:
        """
        Count referrals created by a guest.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
            )
            .count()
        )

    def count_rewarded_by_referrer(
        self,
        referrer_guest_id: str,
    ) -> int:
        """
        Count referrals whose reward was granted.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
                Referral.reward_granted.is_(True),
            )
            .count()
        )

    def count_pending_by_referrer(
        self,
        referrer_guest_id: str,
    ) -> int:
        """
        Count completed referrals whose reward
        has not yet been granted.
        """

        return (
            self.db.query(Referral)
            .filter(
                Referral.referrer_guest_id
                == referrer_guest_id,
                Referral.status == "completed",
                Referral.reward_granted.is_(False),
            )
            .count()
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
            .order_by(
                Referral.created_at.asc()
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
        Flush changes to an existing referral.
        """

        self.db.flush()

        return referral
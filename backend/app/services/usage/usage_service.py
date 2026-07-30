from __future__ import annotations

import json
import logging

from sqlalchemy.orm import Session

from app.database.models.usage_event import UsageEvent
from app.database.repositories.usage_repository import (
    UsageRepository,
)


logger = logging.getLogger(__name__)


class UsageService:
    """
    Business logic for usage tracking.

    Responsibilities:
    - Record application events
    - Track user activity
    - Track guest activity
    - Provide usage statistics
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._usage = UsageRepository(db)

    # ==========================================================
    # Create Events
    # ==========================================================

    def record_user_event(
        self,
        user_id: str,
        event_type: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
        metadata: dict | None = None,
    ) -> UsageEvent:
        """
        Records an event performed by a registered user.
        """

        event = UsageEvent(
            user_id=user_id,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            event_metadata=(
                json.dumps(metadata)
                if metadata
                else None
            ),
        )

        result = self._usage.create(
            event
        )

        logger.info(
            "User usage event recorded: %s",
            event_type,
        )

        return result

    def record_guest_event(
        self,
        guest_session_id: str,
        event_type: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
        metadata: dict | None = None,
    ) -> UsageEvent:
        """
        Records an event performed by a guest.
        """

        event = UsageEvent(
            guest_session_id=guest_session_id,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            event_metadata=(
                json.dumps(metadata)
                if metadata
                else None
            ),
        )

        result = self._usage.create(
            event
        )

        logger.info(
            "Guest usage event recorded: %s",
            event_type,
        )

        return result

    # ==========================================================
    # Queries
    # ==========================================================

    def get_user_history(
        self,
        user_id: str,
    ) -> list[UsageEvent]:
        """
        Returns usage history for a user.
        """

        return self._usage.get_by_user(
            user_id
        )

    def get_guest_history(
        self,
        guest_session_id: str,
    ) -> list[UsageEvent]:
        """
        Returns usage history for a guest session.
        """

        return (
            self._usage.get_by_guest_session(
                guest_session_id
            )
        )

    def count_user_usage(
        self,
        user_id: str,
    ) -> int:
        """
        Returns total events created by user.
        """

        return self._usage.count_by_user(
            user_id
        )

    def count_guest_usage(
        self,
        guest_session_id: str,
    ) -> int:
        """
        Returns total events created by guest.
        """

        return (
            self._usage.count_by_guest_session(
                guest_session_id
            )
        )

    # ==========================================================
    # Checks
    # ==========================================================

    def user_has_usage(
        self,
        user_id: str,
    ) -> bool:
        """
        Checks whether user has any activity.
        """

        return self._usage.user_has_events(
            user_id
        )

    def guest_has_usage(
        self,
        guest_session_id: str,
    ) -> bool:
        """
        Checks whether guest has any activity.
        """

        return (
            self._usage.guest_session_has_events(
                guest_session_id
            )
        )
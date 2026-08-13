from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.database.models.webhook_event import (
    WebhookEvent,
)

from app.database.repositories.base_repository import (
    BaseRepository,
)


logger = logging.getLogger(__name__)


class WebhookEventRepository(
    BaseRepository[WebhookEvent]
):
    """
    Repository for Stripe webhook events.

    Responsibilities:

        - Store processed webhook events.
        - Prevent duplicate processing.
        - Query event history.

    Does NOT:

        - Validate Stripe signatures.
        - Process business logic.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            WebhookEvent,
            db,
        )


    def exists(
        self,
        provider: str,
        event_id: str,
    ) -> bool:
        """
        Check whether webhook was already processed.
        """

        return (
            self.db.query(
                WebhookEvent
            )
            .filter(
                WebhookEvent.provider == provider,
                WebhookEvent.event_id == event_id,
            )
            .first()
            is not None
        )


    def create(
        self,
        provider: str,
        event_id: str,
        event_type: str,
    ) -> WebhookEvent:
        """
        Store webhook event.
        """

        event = WebhookEvent(
            provider=provider,
            event_id=event_id,
            event_type=event_type,
        )

        self.db.add(
            event
        )

        self.db.commit()

        self.db.refresh(
            event
        )

        return event
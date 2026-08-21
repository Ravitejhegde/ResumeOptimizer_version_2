from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models.webhook_event import WebhookEvent
from app.database.repositories.base_repository import BaseRepository


class WebhookEventRepository(BaseRepository[WebhookEvent]):
    """
    Repository for payment-provider webhook events.

    Responsibilities:
    - Detect previously processed events.
    - Register webhook events in the current database transaction.

    Important:
    This repository does NOT commit the transaction when creating
    an event. The caller owns the transaction boundary.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            WebhookEvent,
            db,
        )

    # ==========================================================
    # Queries
    # ==========================================================

    def exists(
        self,
        provider: str,
        event_id: str,
    ) -> bool:
        """
        Return True when this provider event was already processed.
        """
        return (
            self.db.query(WebhookEvent)
            .filter(
                WebhookEvent.provider == provider,
                WebhookEvent.event_id == event_id,
            )
            .first()
            is not None
        )

    def get_by_event_id(
        self,
        event_id: str,
    ) -> WebhookEvent | None:
        """
        Return a webhook event by provider event ID.
        """
        return (
            self.db.query(WebhookEvent)
            .filter(
                WebhookEvent.event_id == event_id,
            )
            .first()
        )

    # ==========================================================
    # Creation
    # ==========================================================

    def create(
        self,
        provider: str,
        event_id: str,
        event_type: str,
    ) -> WebhookEvent:
        """
        Register a webhook event.

        Uses flush rather than commit so the event and the business
        state changes are committed atomically by the service.
        """

        event = WebhookEvent(
            provider=provider,
            event_id=event_id,
            event_type=event_type,
            processed=True,
        )

        self.db.add(event)
        self.db.flush()
        self.db.refresh(event)

        return event
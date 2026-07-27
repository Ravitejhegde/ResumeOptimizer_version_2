from sqlalchemy.orm import Session

from app.database.models.webhook_event import (
    WebhookEvent,
)


class WebhookEventRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def exists(
        self,
        provider: str,
        event_id: str,
    ) -> bool:

        return (

            self.db.query(
                WebhookEvent
            )

            .filter(

                WebhookEvent.provider
                == provider,

                WebhookEvent.event_id
                == event_id,

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

        event = WebhookEvent(

            provider=provider,

            event_id=event_id,

            event_type=event_type,

            processed=True,

        )

        self.db.add(event)

        self.db.commit()

        self.db.refresh(event)

        return event





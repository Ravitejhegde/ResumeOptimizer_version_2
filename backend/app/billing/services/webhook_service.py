from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import Session

from app.billing.providers.stripe.webhook import (
    StripeWebhook,
)

from app.billing.repository.database_order_repository import (
    DatabaseOrderRepository,
)

from app.billing.repository.database_subscription_repository import (
    DatabaseSubscriptionRepository,
)

from app.billing.repository.database_transaction_repository import (
    DatabaseTransactionRepository,
)

from app.billing.repository.webhook_event_repository import (
    WebhookEventRepository,
)

from app.database.models.payment_transaction import (
    PaymentTransaction,
)

from app.database.models.subscription import (
    Subscription,
)


class WebhookService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.webhook = StripeWebhook()

        self.orders = DatabaseOrderRepository(
            db
        )

        self.transactions = (
            DatabaseTransactionRepository(
                db
            )
        )

        self.subscriptions = (
            DatabaseSubscriptionRepository(
                db
            )
        )

        self.events = WebhookEventRepository(
            db
        )

    def process(
        self,
        payload: bytes,
        signature: str,
    ):

        event = self.webhook.verify(
            payload,
            signature,
        )

        event_id = event["id"]

        event_type = event["type"]

        # ---------------------------------------
        # Prevent duplicate webhook processing
        # ---------------------------------------

        if self.events.exists(
            "stripe",
            event_id,
        ):

            return {
                "duplicate": True,
                "event_id": event_id,
            }

        self.events.create(
            provider="stripe",
            event_id=event_id,
            event_type=event_type,
        )

        # ---------------------------------------
        # Route Event
        # ---------------------------------------

        if self.webhook.is_checkout_completed(
            event
        ):

            self._checkout_completed(
                event
            )

        elif self.webhook.is_invoice_paid(
            event
        ):

            self._invoice_paid(
                event
            )

        elif self.webhook.is_invoice_failed(
            event
        ):

            self._invoice_failed(
                event
            )

        elif self.webhook.is_subscription_updated(
            event
        ):

            self._subscription_updated(
                event
            )

        elif self.webhook.is_subscription_deleted(
            event
        ):

            self._subscription_deleted(
                event
            )

        return {
            "processed": True,
            "event": event_type,
            "event_id": event_id,
        }

    def _checkout_completed(
        self,
        event,
    ):

        data = self.webhook.data(
            event
        )

        order = self.orders.get(
            data["client_reference_id"]
        )

        if order is None:
            return

        order.status = "paid"

        self.orders.update(
            order
        )

        transaction = PaymentTransaction(

            order_id=order.id,

            provider="stripe",

            provider_transaction_id=data.get(
                "payment_intent"
            ),

            amount=order.amount,

            currency=order.currency,

            status="succeeded",

        )

        self.transactions.create(
            transaction
        )

        subscription = Subscription(

            user_id=order.user_id,

            order_id=order.id,

            status="active",

            starts_at=datetime.utcnow(),

            expires_at=(
                datetime.utcnow()
                + timedelta(days=30)
            ),

        )

        self.subscriptions.create(
            subscription
        )

    def _invoice_paid(
        self,
        event,
    ):

        pass

    def _invoice_failed(
        self,
        event,
    ):

        pass

    def _subscription_updated(
        self,
        event,
    ):

        pass

    def _subscription_deleted(
        self,
        event,
    ):

        pass
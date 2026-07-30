from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session

from app.billing.providers.stripe_provider import (
    StripeProvider,
)
from app.billing.services.stripe_webhook_service import (
    StripeWebhookService,
)
from app.database.session import get_db

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.post("/webhook/stripe")
async def stripe_webhook(

    request: Request,

    db: Session = Depends(get_db),

):

    payload = await request.body()

    signature = request.headers.get(
        "Stripe-Signature"
    )

    provider = StripeProvider()

    try:

        event = provider.verify_webhook(

            payload,

            signature,

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e),

        )

    # -------------------------------------
    # Payment Success
    # -------------------------------------

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        service = StripeWebhookService(
            db
        )

        service.payment_success(

            order_id=session["client_reference_id"],

            transaction_id=session["payment_intent"],

            amount=session["amount_total"] / 100,

            currency=session["currency"].upper(),

        )

    return {

        "received": True,

    }





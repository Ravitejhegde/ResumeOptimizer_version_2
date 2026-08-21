from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.billing.services.webhook_service import WebhookService
from app.database.session import get_db


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str | None = Header(
        default=None,
        alias="Stripe-Signature",
    ),
) -> dict:
    """
    Receive a Stripe webhook.

    HTTP responsibilities only:

        1. Read request body.
        2. Read Stripe signature.
        3. Pass event to WebhookService.
        4. Convert service errors into HTTP responses.

    All billing business logic lives in WebhookService.
    """

    # ----------------------------------------------------------
    # Stripe signature
    # ----------------------------------------------------------

    if not stripe_signature:
        raise HTTPException(
            status_code=400,
            detail="Missing Stripe-Signature header.",
        )

    # ----------------------------------------------------------
    # Raw request body
    # ----------------------------------------------------------

    payload = await request.body()

    if not payload:
        raise HTTPException(
            status_code=400,
            detail="Empty webhook payload.",
        )

    # ----------------------------------------------------------
    # Business processing
    # ----------------------------------------------------------

    service = WebhookService(db)

    try:
        result = service.process(
            payload=payload,
            signature=stripe_signature,
        )

        return result

    except ValueError as exc:
        db.rollback()

        logger.warning(
            "Stripe webhook rejected: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        db.rollback()

        logger.exception(
            "Stripe webhook processing failed.",
        )

        raise HTTPException(
            status_code=500,
            detail="Webhook processing failed.",
        )
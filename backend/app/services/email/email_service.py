"""
Central email delivery service.
"""

from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger(__name__)


class EmailService:
    """
    Central service responsible for sending application emails.

    Authentication and verification services should not contain
    SMTP implementation details.
    """

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send a plain-text email.

        When email is disabled, no email is sent.
        """

        if not settings.ENABLE_EMAIL:
            logger.info(
                "Email delivery disabled. "
                "Skipping email to %s.",
                to_email,
            )
            return

        self._validate_configuration()

        message = EmailMessage()

        message["From"] = (
            f"{settings.EMAIL_FROM_NAME} "
            f"<{settings.EMAIL_FROM}>"
        )

        message["To"] = to_email
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=30,
        ) as smtp:

            smtp.starttls()

            smtp.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )

            smtp.send_message(message)

        logger.info(
            "Email sent successfully to %s.",
            to_email,
        )

    # ==========================================================
    # Configuration
    # ==========================================================

    @staticmethod
    def _validate_configuration() -> None:
        """
        Validate SMTP configuration before sending.
        """

        required = {
            "SMTP_HOST": settings.SMTP_HOST,
            "SMTP_USERNAME": settings.SMTP_USERNAME,
            "SMTP_PASSWORD": settings.SMTP_PASSWORD,
            "EMAIL_FROM": settings.EMAIL_FROM,
        }

        missing = [
            name
            for name, value in required.items()
            if not value
        ]

        if missing:
            raise RuntimeError(
                "Email configuration is incomplete. "
                f"Missing: {', '.join(missing)}"
            )
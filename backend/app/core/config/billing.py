from __future__ import annotations

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class BillingSettings(BaseSettings):
    """
    Billing configuration.
    """

    BILLING_PROVIDER: str = Field(
        default="stripe",
    )

    DEFAULT_COUNTRY: str = Field(
        default="IN",
    )

    DEFAULT_CURRENCY: str = Field(
        default="INR",
    )

    STRIPE_SECRET_KEY: str = Field(
        default="",
    )

    STRIPE_PUBLISHABLE_KEY: str = Field(
        default="",
    )

    STRIPE_WEBHOOK_SECRET: str = Field(
        default="",
    )

    STRIPE_API_VERSION: str = Field(
        default="2025-06-30.basil",
    )

    FRONTEND_URL: str = Field(
        default="http://localhost:5173",
    )

    BILLING_SUCCESS_PATH: str = Field(
        default="/billing/success",
    )

    BILLING_CANCEL_PATH: str = Field(
        default="/billing/cancel",
    )

    BILLING_PORTAL_PATH: str = Field(
        default="/dashboard",
    )

    ENABLE_TRIALS: bool = Field(
        default=True,
    )

    ENABLE_PROMOTION_CODES: bool = Field(
        default=True,
    )

    ENABLE_AUTOMATIC_TAX: bool = Field(
        default=True,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def BILLING_SUCCESS_URL(self) -> str:
        return (
            self.FRONTEND_URL
            + self.BILLING_SUCCESS_PATH
        )

    @property
    def BILLING_CANCEL_URL(self) -> str:
        return (
            self.FRONTEND_URL
            + self.BILLING_CANCEL_PATH
        )

    @property
    def BILLING_PORTAL_RETURN_URL(self) -> str:
        return (
            self.FRONTEND_URL
            + self.BILLING_PORTAL_PATH
        )





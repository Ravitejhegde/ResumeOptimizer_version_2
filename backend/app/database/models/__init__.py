"""
Database models.

Import every SQLAlchemy model here so they are registered with
SQLAlchemy before Base.metadata.create_all() is executed.
"""

from .download import Download
from .email_verification_token import EmailVerificationToken
from .feature import Feature
from .generated_resume import GeneratedResume
from .guest import Guest
from .guest_session import GuestSession
from .optimization_job import OptimizationJob
from .order import Order
from .payment_transaction import PaymentTransaction
from .plan import Plan
from .plan_feature import PlanFeature
from .pricing import Pricing
from .resume import Resume
from .subscription import Subscription
from .usage_event import UsageEvent
from .user import User
from .webhook_event import WebhookEvent
from .workspace import Workspace
from .referral import Referral

__all__ = [
    "Download",
    "EmailVerificationToken",
    "Feature",
    "GeneratedResume",
    "Guest",
    "GuestSession",
    "OptimizationJob",
    "Order",
    "PaymentTransaction",
    "Plan",
    "PlanFeature",
    "Pricing",
    "Resume",
    "Subscription",
    "UsageEvent",
    "User",
    "WebhookEvent",
    "Referral",
    "Workspace",
]
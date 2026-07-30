from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.models.plan import Plan
from app.database.models.plan_feature import PlanFeature
from app.database.models.pricing import Pricing


def seed_database(db: Session) -> None:
    """
    Seeds the default application data.

    Safe to execute multiple times.
    """

    # ==========================================================
    # Feature
    # ==========================================================

    feature = (
        db.query(Feature)
        .filter(
            Feature.code == "resume_optimization",
        )
        .first()
    )

    if feature is None:
        feature = Feature(
            code="resume_optimization",
            name="Resume Optimization",
            description="Optimize resumes using AI.",
        )

        db.add(feature)
        db.flush()

    # ==========================================================
    # Plan
    # ==========================================================

    plan = (
        db.query(Plan)
        .filter(
            Plan.code == "free",
        )
        .first()
    )

    if plan is None:
        plan = Plan(
            code="free",
            name="Free",
            description="Free Plan",
        )

        db.add(plan)
        db.flush()

    # ==========================================================
    # Plan Feature
    # ==========================================================

    if (
        db.query(PlanFeature)
        .filter(
            PlanFeature.plan_id == plan.id,
            PlanFeature.feature_id == feature.id,
        )
        .first()
        is None
    ):
        db.add(
            PlanFeature(
                plan_id=plan.id,
                feature_id=feature.id,
                value="10",
                active=True,
            )
        )

    # ==========================================================
    # Pricing
    # ==========================================================

    if (
        db.query(Pricing)
        .filter(
            Pricing.plan_id == plan.id,
            Pricing.country_code == "IN",
        )
        .first()
        is None
    ):
        db.add(
            Pricing(
                plan_id=plan.id,
                country_code="IN",
                currency_code="INR",
                monthly_price=Decimal("0.00"),
                yearly_price=Decimal("0.00"),
                payment_provider="internal",
            )
        )

    db.commit()
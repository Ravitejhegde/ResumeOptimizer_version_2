from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.models.plan import Plan
from app.database.models.plan_feature import PlanFeature
from app.database.models.pricing import Pricing


# ==========================================================
# Product Catalog
# ==========================================================
#
# This is the single place where the commercial plan catalog
# is defined.
#
# To add/change a plan later, update this configuration.
#
# Pricing is country-specific.
# Plan limits are stored as plan features.
#
# ==========================================================


PLANS = [
    {
        "code": "brown",
        "name": "Brown",
        "description": "200 resume optimizations per month.",
        "monthly_optimizations": 200,
    },
    {
        "code": "silver",
        "name": "Silver",
        "description": "300 resume optimizations per month.",
        "monthly_optimizations": 300,
    },
    {
        "code": "gold",
        "name": "Gold",
        "description": "400 resume optimizations per month.",
        "monthly_optimizations": 400,
    },
]


COUNTRY_PRICING = {
    "IN": {
        "currency": "INR",
        "prices": {
            "brown": Decimal("99.00"),
            "silver": Decimal("129.00"),
            "gold": Decimal("149.00"),
        },
    },
}


def _get_or_create_feature(
    db: Session,
) -> Feature:
    """
    Get or create the resume optimization feature.
    """

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
            description="Number of resume optimizations available.",
            value_type="integer",
            active=True,
        )

        db.add(feature)
        db.flush()

    else:
        # Keep the existing feature definition aligned
        # with the actual value being stored in PlanFeature.
        feature.name = "Resume Optimization"
        feature.description = (
            "Number of resume optimizations available."
        )
        feature.value_type = "integer"
        feature.active = True

    return feature


def _get_or_create_plan(
    db: Session,
    plan_config: dict,
) -> Plan:
    """
    Get or create a commercial plan.
    """

    plan = (
        db.query(Plan)
        .filter(
            Plan.code == plan_config["code"],
        )
        .first()
    )

    if plan is None:
        plan = Plan(
            code=plan_config["code"],
            name=plan_config["name"],
            description=plan_config["description"],
            active=True,
        )

        db.add(plan)
        db.flush()

    else:
        plan.name = plan_config["name"]
        plan.description = plan_config["description"]
        plan.active = True

    return plan


def _upsert_plan_feature(
    db: Session,
    plan: Plan,
    feature: Feature,
    value: int,
) -> PlanFeature:
    """
    Create or update the feature value for a plan.
    """

    plan_feature = (
        db.query(PlanFeature)
        .filter(
            PlanFeature.plan_id == plan.id,
            PlanFeature.feature_id == feature.id,
        )
        .first()
    )

    if plan_feature is None:
        plan_feature = PlanFeature(
            plan_id=plan.id,
            feature_id=feature.id,
            value=str(value),
            active=True,
        )

        db.add(plan_feature)

    else:
        plan_feature.value = str(value)
        plan_feature.active = True

    return plan_feature


def _upsert_pricing(
    db: Session,
    plan: Plan,
    country_code: str,
    currency_code: str,
    monthly_price: Decimal,
) -> Pricing:
    """
    Create or update country-specific pricing.
    """

    pricing = (
        db.query(Pricing)
        .filter(
            Pricing.plan_id == plan.id,
            Pricing.country_code == country_code,
        )
        .first()
    )

    if pricing is None:
        pricing = Pricing(
            plan_id=plan.id,
            country_code=country_code,
            currency_code=currency_code,
            monthly_price=monthly_price,
            yearly_price=None,
            payment_provider="stripe",
            active=True,
        )

        db.add(pricing)

    else:
        pricing.currency_code = currency_code
        pricing.monthly_price = monthly_price
        pricing.payment_provider = "stripe"
        pricing.active = True

    return pricing


def seed_database(
    db: Session,
) -> None:
    """
    Seed the ResumeOptimizer commercial product catalog.

    Safe to execute multiple times.

    Current catalog:

        Brown
            ₹99/month
            200 optimizations

        Silver
            ₹129/month
            300 optimizations

        Gold
            ₹149/month
            400 optimizations

    Guest free samples are intentionally NOT represented
    as a paid Plan.
    """

    # ======================================================
    # Feature
    # ======================================================

    feature = _get_or_create_feature(db)

    # ======================================================
    # Plans + Features
    # ======================================================

    plans_by_code: dict[str, Plan] = {}

    for plan_config in PLANS:

        plan = _get_or_create_plan(
            db,
            plan_config,
        )

        _upsert_plan_feature(
            db,
            plan,
            feature,
            plan_config["monthly_optimizations"],
        )

        plans_by_code[plan.code] = plan

    # ======================================================
    # Country Pricing
    # ======================================================

    for country_code, country_config in COUNTRY_PRICING.items():

        currency_code = country_config["currency"]
        prices = country_config["prices"]

        for plan_code, monthly_price in prices.items():

            plan = plans_by_code.get(plan_code)

            if plan is None:
                continue

            _upsert_pricing(
                db,
                plan,
                country_code,
                currency_code,
                monthly_price,
            )

    # ======================================================
    # Disable old Free plan
    # ======================================================
    #
    # Free guest samples are handled outside the paid
    # subscription catalog.
    #
    # We don't delete the old record because deleting it
    # could become dangerous later if historical orders
    # reference it.
    #
    # ======================================================

    old_free_plan = (
        db.query(Plan)
        .filter(
            Plan.code == "free",
        )
        .first()
    )

    if old_free_plan is not None:
        old_free_plan.active = False

        for pricing in old_free_plan.pricing:
            pricing.active = False

        for plan_feature in old_free_plan.features:
            plan_feature.active = False

    # ======================================================
    # Commit
    # ======================================================

    db.commit()
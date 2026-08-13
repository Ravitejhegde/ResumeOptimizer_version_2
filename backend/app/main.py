from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router as analysis_router
from app.api.routes.auth import router as auth_router
from app.api.routes.download import router as download_router
from app.api.routes.optimization import (
    router as optimization_router,
)
from app.api.routes.resume import router as resume_router
from app.api.routes.user import router as user_router
from app.billing.routes.checkout import (
    router as billing_checkout_router,
)
from app.billing.routes.plans import (
    router as billing_plans_router,
)
from app.guest.routes.guest import router as guest_router
from app.billing.routes.pricing import (
    router as billing_pricing_router,
)
from app.billing.routes.webhook import (
    router as billing_webhook_router,
)
from app.core.config import settings
from app.database.init_db import initialize_database

load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    """
    Initialize the application.
    """

    settings.create_directories()

    initialize_database()


# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(resume_router)
app.include_router(analysis_router)
app.include_router(optimization_router)
app.include_router(download_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(guest_router)
# --------------------------------------------------
# Billing Routes
# --------------------------------------------------

app.include_router(
    billing_checkout_router,
)

app.include_router(
    billing_plans_router,
)

app.include_router(
    billing_pricing_router,
)

# app.include_router(
#     billing_subscription_router,
# )

# app.include_router(
#     billing_portal_router,
# )

app.include_router(
    billing_webhook_router,
)


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
    }

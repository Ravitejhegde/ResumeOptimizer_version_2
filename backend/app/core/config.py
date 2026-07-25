from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------

    APP_NAME: str = "ResumeOptimizer API"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    # ---------------------------------------------------------
    # Security
    # ---------------------------------------------------------

    SECRET_KEY: str = (
        "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_IN_PRODUCTION"
    )

    # ---------------------------------------------------------
    # AI
    # ---------------------------------------------------------

    AI_PROVIDER: str = "openrouter"

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODEL: str = (
        "deepseek/deepseek-chat-v3-0324"
    )

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = (
        "gemini-2.5-flash-lite"
    )

    # ---------------------------------------------------------
    # Upload
    # ---------------------------------------------------------

    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS: tuple[str, ...] = (
        ".docx",
    )

    # ---------------------------------------------------------
    # Billing
    # ---------------------------------------------------------

    DEFAULT_COUNTRY: str = "IN"

    DEFAULT_CURRENCY: str = "INR"

    DEFAULT_PROVIDER: str = "stripe"

    STRIPE_SECRET_KEY: str = ""

    STRIPE_PUBLISHABLE_KEY: str = ""

    STRIPE_WEBHOOK_SECRET: str = ""

    STRIPE_API_VERSION: str = "2025-06-30.basil"

    BILLING_SUCCESS_URL: str = (
        "http://localhost:5173/billing/success"
    )

    BILLING_CANCEL_URL: str = (
        "http://localhost:5173/billing/cancel"
    )

    BILLING_PORTAL_RETURN_URL: str = (
        "http://localhost:5173/dashboard"
    )

    ENABLE_AUTOMATIC_TAX: bool = True

    ENABLE_PROMOTION_CODES: bool = True

    ENABLE_TRIALS: bool = True

    # ---------------------------------------------------------
    # Project Paths
    # ---------------------------------------------------------

    BASE_DIR: Path = (
        Path(__file__).resolve().parents[2]
    )

    STORAGE_PATH: Path = (
        BASE_DIR / "storage"
    )

    TEMP_PATH: Path = (
        STORAGE_PATH / "temp"
    )

    RESUME_PATH: Path = (
        STORAGE_PATH / "resumes"
    )

    PREVIEW_PATH: Path = (
        STORAGE_PATH / "previews"
    )

    EXPORT_PATH: Path = (
        STORAGE_PATH / "exports"
    )

    LOG_PATH: Path = (
        BASE_DIR / "logs"
    )

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------

    DATABASE_URL: str = (
    "postgresql+psycopg://postgres:Teju2103@localhost:5432/resume_optimizer"
)

    model_config = SettingsConfigDict(

        env_file=".env",

        case_sensitive=True,

        extra="ignore",

    )


settings = Settings()
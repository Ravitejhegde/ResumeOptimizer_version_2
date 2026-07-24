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
    # Project Paths
    # ---------------------------------------------------------
    BASE_DIR: Path = Path(__file__).resolve().parents[2]

    STORAGE_PATH: Path = BASE_DIR / "storage"

    TEMP_PATH: Path = STORAGE_PATH / "temp"

    RESUME_PATH: Path = STORAGE_PATH / "resumes"

    PREVIEW_PATH: Path = STORAGE_PATH / "previews"

    EXPORT_PATH: Path = STORAGE_PATH / "exports"

    LOG_PATH: Path = BASE_DIR / "logs"

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------
    DATABASE_URL: str = (
        f"sqlite:///{BASE_DIR / 'resume_optimizer.db'}"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
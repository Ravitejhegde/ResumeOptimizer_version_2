from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = "ResumeOptimizer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------
    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODEL: str = "deepseek/deepseek-chat-v3-0324"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    AI_PROVIDER: str = "openrouter"

    # ------------------------------------------------------------------
    # File Upload
    # ------------------------------------------------------------------
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS: tuple[str, ...] = (".docx",)

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------
    BASE_DIR: Path = Path(__file__).resolve().parents[2]

    STORAGE_DIR: Path = BASE_DIR / "storage"
    TEMP_DIR: Path = STORAGE_DIR / "temp"
    PROCESSED_DIR: Path = STORAGE_DIR / "processed"
    EXPORT_DIR: Path = STORAGE_DIR / "exports"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
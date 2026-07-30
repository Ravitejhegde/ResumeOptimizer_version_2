from __future__ import annotations


from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)



class StorageSettings(BaseSettings):
    """
    Storage configuration.

    Responsible only for filesystem paths
    used throughout the application.
    """


    # ======================================================
    # Base
    # ======================================================

    BASE_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3],
    )


    # ======================================================
    # Storage Root
    # ======================================================

    STORAGE_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage",
    )


    # ======================================================
    # Resume Files
    # ======================================================

    RESUME_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "resumes",
    )


    # Backward compatibility
    # Used by older storage services

    RESUME_STORAGE_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "resumes",
    )


    # ======================================================
    # Other Storage
    # ======================================================

    EXPORT_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "exports",
    )


    PREVIEW_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "previews",
    )


    TEMP_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "temp",
    )


    CACHE_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "cache",
    )


    REPORT_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "reports",
    )


    KNOWLEDGE_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "storage"
        / "knowledge",
    )


    LOG_DIR: Path = Field(
        default=Path(__file__).resolve().parents[3]
        / "logs",
    )


    # ======================================================
    # Environment
    # ======================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=True,
        extra="ignore",
    )


    # ======================================================
    # Directory Creation
    # ======================================================

    def create_directories(
        self,
    ) -> None:
        """
        Create required application directories.
        """


        directories = (

            self.STORAGE_DIR,

            self.RESUME_DIR,

            self.EXPORT_DIR,

            self.PREVIEW_DIR,

            self.TEMP_DIR,

            self.CACHE_DIR,

            self.REPORT_DIR,

            self.KNOWLEDGE_DIR,

            self.LOG_DIR,

        )


        for directory in directories:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )
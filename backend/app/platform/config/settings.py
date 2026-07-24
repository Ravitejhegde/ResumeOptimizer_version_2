from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformSettings:

    FREE_TRIAL_LIMIT = 3

    MAX_RESUME_SIZE_MB = 5

    SESSION_DAYS = 30

    DEFAULT_COUNTRY = "IN"

    DEFAULT_PLAN = "free"

    DEFAULT_LANGUAGE = "en"

    SUPPORTED_FILE_TYPES = (
        ".docx",
    )


SETTINGS = PlatformSettings()